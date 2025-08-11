# db/write.py

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.session import SessionLocal
from db.models import Article, EntityHit

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