# db/write.py

from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.session import SessionLocal
from db.models import Article, EntityHit, FearGreedDaily, StockValueDaily
import pandas as pd

def save_articles_to_db(items: list[dict]):
    """
    Each row like:
    {
      "article_id": "...", "published_at": "2025-08-09T16:30:37Z",
      "title": "...", "url": "...", "source": "...", "language": "en",
      "symbol": "TSLA", "company": "Tesla", "match_score": 12.3, "sentiment_score": 0.42
    }
    """

    if not items:
        return 0, 0 # (articles, hits)
    
    art_new = 0
    hit_new = 0


    with SessionLocal() as session:
        for row in items:
            uuid = row.get("uuid")
            if not uuid:
                # skip, broken
                continue
            # Upsert Article
            art = session.get(Article, uuid)
            if not art:
                art = Article(
                    article_id = uuid,
                    title      = row.get("title") or "",
                    url        = row.get("url") or "",
                    source     = row.get("source"),
                    language   = row.get("language"),
                    published_at = datetime.fromisoformat(
                        row.get("published_at", "").replace("Z","+00:00")
                    ),
                )
                session.add(art)
                art_new += 1

                # Insert EntityHit (one per (article, symbol))
                for ent in (row.get("entities") or []):
                    hit = EntityHit(
                    article_id      = uuid,
                    symbol          = ent.get("symbol"),
                    company         = ent.get("name"), 
                    match_score     = ent.get("match_score"),
                    sentiment_score = ent.get("sentiment_score"),
                    )
                    session.add(hit)

                    try:
                        session.flush()  # validate unique constraints early
                        hit_new += 1
                    except IntegrityError:
                        session.rollback()
                        # already exists

                        if ent.get("sentiment_score") is not None:
                            existing = session.execute(
                            select(EntityHit).where(
                                EntityHit.article_id == uuid,
                                EntityHit.symbol == ent.get("symbol")
                            )
                            ).scalar_one_or_none()
                            if existing:
                                existing.sentiment_score = ent["sentiment_score"]
                                session.add(existing)
                                session.flush()

            session.commit()
        return art_new, hit_new
    


def save_fgi_to_db(items: list[dict]) -> int:
    if not items:
        return 0

    # 1) Collapse to one row per date
    by_date = {}  # {date: value}
    for pt in items:
        d = datetime.fromtimestamp(float(pt["x"]) / 1000.0, tz=timezone.utc).date()
        v = int(round(float(pt["y"])))
        by_date[d] = v  # last wins

    added = 0
    with SessionLocal() as s:
        for d, v in by_date.items():
            row = s.get(FearGreedDaily, d)
            if not row:
                s.add(FearGreedDaily(date=d, value=v))
                added += 1
            else:
                # upsert: update existing
                row.value = v
                s.add(row)
        s.commit()
    return added

def save_stock_values_to_db(items: pd.DataFrame) -> int:
    def none_or_float(x): return None if pd.isna(x) else float(x)
    new_rows = 0
    with SessionLocal() as session:
        for idx, row in items.iterrows():
            date = pd.to_datetime(idx).date() if "date" not in items.columns else pd.to_datetime(row["date"]).date()

            existing = session.get(StockValueDaily, {"ticker": row["ticker"], "date": date})
            if not existing:
                new_rows += 1
                rec = StockValueDaily(
                    ticker=row["ticker"],
                    date=date,
                    open_=float(row["open_"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close_=float(row["close_"]),
                    volume=int(row["volume"]),
                    rsi=none_or_float(row.get("rsi")),
                    macd=none_or_float(row.get("macd")),
                    macd_signal=none_or_float(row.get("macd_signal")),
                )
                session.add(rec)
            else:
                # update fields if you want to refresh indicators
                existing.open_ = float(row["open_"])
                existing.high = float(row["high"])
                existing.low = float(row["low"])
                existing.close_ = float(row["close_"])
                existing.volume = int(row["volume"])
                existing.rsi = none_or_float(row.get("rsi"))
                existing.macd = none_or_float(row.get("macd"))
                existing.macd_signal = none_or_float(row.get("macd_signal"))
                session.add(existing)
        session.commit()   # <-- you were missing parentheses
    return new_rows