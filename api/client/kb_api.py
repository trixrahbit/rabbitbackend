from fastapi import Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.clientModel.kbArticle_model import KnowledgeBaseArticle
from root.root_elements import router
from schemas.organizations.kbArticle_schema import KbArticleSchema



@router.get("/{client_id}/kbarticles", response_model=List[KbArticleSchema])
def read_kb_articles(client_id: int, db: Session = Depends(get_db)):
    kb_articles = db.query(KnowledgeBaseArticle).filter(KnowledgeBaseArticle.client_id == client_id).all()
    return kb_articles

@router.get("/{client_id}/kbarticles/{kb_article_id}", response_model=KbArticleSchema)
def read_kb_article(client_id: int, kb_article_id: int, db: Session = Depends(get_db)):
    kb_article = db.query(KnowledgeBaseArticle).filter(KnowledgeBaseArticle.client_id == client_id).filter(KnowledgeBaseArticle.id == kb_article_id).first()
    if kb_article is None:
        raise HTTPException(status_code=404, detail="Knowledge Base Article not found")
    return kb_article

@router.post("/{client_id}/kbarticles", response_model=KbArticleSchema)
def create_kb_article(client_id: int, kb_article: KbArticleSchema, db: Session = Depends(get_db)):
    kb_article = KnowledgeBaseArticle(**kb_article.dict(), client_id=client_id)
    db.add(kb_article)
    db.commit()
    db.refresh(kb_article)
    return kb_article

@router.patch("/{client_id}/kbarticles/{kb_article_id}", response_model=KbArticleSchema)
def update_kb_article(client_id: int, kb_article_id: int, kb_article: KbArticleSchema, db: Session = Depends(get_db)):
    kb_article = db.query(KnowledgeBaseArticle).filter(KnowledgeBaseArticle.client_id == client_id).filter(KnowledgeBaseArticle.id == kb_article_id).first()
    if kb_article is None:
        raise HTTPException(status_code=404, detail="Knowledge Base Article not found")
    update_data = kb_article.dict(exclude_unset=True)
    updated_kb_article = KnowledgeBaseArticle(**update_data)
    db.add(updated_kb_article)
    db.commit()
    db.refresh(updated_kb_article)
    return updated_kb_article

@router.delete("/{client_id}/kbarticles/{kb_article_id}", response_model=KbArticleSchema)
def delete_kb_article(client_id: int, kb_article_id: int, db: Session = Depends(get_db)):
    kb_article = db.query(KnowledgeBaseArticle).filter(KnowledgeBaseArticle.client_id == client_id).filter(KnowledgeBaseArticle.id == kb_article_id).first()
    if kb_article is None:
        raise HTTPException(status_code=404, detail="Knowledge Base Article not found")
    db.delete(kb_article)
    db.commit()
    return kb_article