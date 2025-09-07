
from fastapi import Body, FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app= FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

    

# request get method url: "/"
@app.get("/")
def read_root():
    return {"Hello": "Liii"}

@app.get("/posts")
def get_posts():
    return {"data": "This is a post"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post.dict())
    return {"data": new_post} 
    # return {'new_post': f'This is a new post with title {payload["Title"]} and content {payload["Content"]}'}







