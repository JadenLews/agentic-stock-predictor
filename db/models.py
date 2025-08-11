# db/models.py

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Text, DateTime, Float, Integer, ForeignKey, UniqueConstraint, Index

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    article_id = Column(String, primary_key=True)
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    source = Column(String)
    language = Column(String)
    published_at = Column(DateTime, nullable=False)

    # relationship
    entity_hits = relationship("EntityHit", back_populates="article", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("url", name="uq_articles_url"),    #avoid dups
        Index("ix_articles_publiched_at", "published_at"),  #fast load
        Index("ix_articles_source", "source")
    )


class EntityHit(Base):
    __tablename__ = "entity_hits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(String, ForeignKey("articles.article_id", ondelete="CASCADE"), nullable=False)
    symbol = Column(String, nullable=False)
    company = Column(String)
    match_score = Column(Float)
    sentiment_score = Column(Float)

    article = relationship("Article", back_populates="entity_hits")

    __table_args__ = (
        UniqueConstraint("article_id", "symbol", name="uq_entityhit_article_symbol"),
        Index("ix_entity_hits_symbol", "symbol")
    )