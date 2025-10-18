
from fastapi import Body, FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app= FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts=[{"Title": "title of post 1", "Content": "content of post 1", "id": 1},{"Title": "favorite foods", "Content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# request get method url: "/"
@app.get("/")
def read_root():
    return {"data":my_posts}

#retrieve all posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)  
    return {"data": post_dict} 
    # return {'new_post': f'This is a new post with title {payload["Title"]} and content {payload["Content"]}'}

#retrieve a specific post
@app.get("/posts/{id}")
def get_post(id):
    print(id)
    return {"post_detail": f"Here is post number {id}"}
    





