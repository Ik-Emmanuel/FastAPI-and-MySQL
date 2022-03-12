from typing import Optional, List
from fastapi import Depends, FastAPI, status, HTTPException
from pydantic import BaseModel
from .database import engine, SessionLocal
from . import models
from .schemas import * 
from sqlalchemy.orm import Session
##########################################################################################

models.Base.metadata.create_all(bind=engine)
   
app = FastAPI()

#
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


###################################################################

# @app.get('/articles/{id}') #path with path parameter inside PATH OPERATOR DECORATOR
# def get_articles(id:int):  #PATH OPERATOR FUNCTION 
#     return {"message": {'id': id}}

# @app.get('/articles/')
# def get_articles(skip:int = 0, limit:int=20, q:Optional[str] =None): 
#     #Query parameters same as http://localhost:8000/articles/?skip=0&limit=20
#     return {"message": {'data': data[skip: skip + limit], 'Query':q }}


@app.get('/') 
def Index(): 
    return {"message": "Hello from FASTAPI!"}

@app.get('/articles/', response_model=List[MyArticleSchema])
def get_articles(db: Session = Depends(get_db)):
    my_articles = db.query(models.Article).all()
    return my_articles

@app.get('/articles/{id}', response_model=MyArticleSchema, status_code=status.HTTP_200_OK)
def article_detail(id:int, db: Session = Depends(get_db)):
    # my_article = db.query(models.Article).filter(models.Article.id == id).first()
    my_article = db.query(models.Article).get(id)

    if my_article:
        return my_article 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error":f"No article with id: {id}"})

@app.post('/articles/', status_code=status.HTTP_201_CREATED)
def add_article(article:ArticleSchema, db: Session = Depends(get_db)):
    new_article = models.Article(title=article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@app.put('/articles/{id}',  status_code=status.HTTP_202_ACCEPTED)
def update_article(id:int, article:ArticleSchema, db: Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).update({'title':article.title, 'description':article.description})
    db.commit()
    return {"message":"Article entry updated"}
    #  # my_article = db.query(models.Article).filter(models.Article.id == id).first()
    # if my_article:
    #     my_article.update({'title':article.title, 'description':article.description})
    #     db.commit()
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error":f"No article with id: {id}"})

@app.delete('/articles/{id}',  status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id:int, db: Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).delete(synchronize_session=False)
    db.commit()




