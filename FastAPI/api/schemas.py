from pydantic import BaseModel


class ArticleSchema(BaseModel):
    # id:int  -- no need for this since the db models has it as PK and will autoincrement
    title:str
    description:str

class MyArticleSchema(ArticleSchema): #use as response model to specify which of the fields alone should be returned
    title:str
    description:str
    class Config:
        orm_mode = True
