
from fastapi import Body, FastAPI, Response, status, HTTPException  
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
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

# request get method url: "/"
@app.get("/")
def read_root():
    return {"data":my_posts}

#retrieve all posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)  
    return {"data": post_dict} 
    # return {'new_post': f'This is a new post with title {payload["Title"]} and content {payload["Content"]}'}

#retrieve last post
@app.get("/posts/latest")
def get_latest_post():
    post= my_posts[len(my_posts)-1] 
    return {"latest_post": post}    

#retrieve a specific post
@app.get("/posts/{id:int}")
def get_post(id,response: Response):
    post= find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    return post
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find the index in the array that has the required id
    #my_posts.pop(index)
    index= find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")             
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index= find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
    post_dict= post.dict()
    post_dict['id'] = id
    my_posts[index]= post_dict
    return {"data": my_posts[index]}    