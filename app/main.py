
from fastapi import Body, FastAPI, Response, status, HTTPException  
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app= FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
while True:

    try:
        conn=psycopg2.connect(
        host="127.0.0.1",   # use the exact host from pgAdmin; try 127.0.0.1 instead of "localhost"
        port=5433,          # set the exact port from pgAdmin (often 5432, sometimes 5433)
        database="fastapi",
        user="postgres",    # the username shown in pgAdmin
        password="steve81",
        cursor_factory=RealDictCursor)
        
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
         print("Connecting to database failed")
         print("Error:", error)
         time.sleep(3)

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
    cursor.execute("SELECT * FROM posts")
    posts= cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                   (post.title, post.content, post.published))
    new_post= cursor.fetchone()
    conn.commit() #conect with the database and save the change
    return {"data": new_post}


    #post_dict = post.dict()
    #post_dict['id'] = randrange(0,1000000)
    #my_posts.append(post_dict)  
    #return {"data": post_dict} 
    # return {'new_post': f'This is a new post with title {payload["Title"]} and content {payload["Content"]}'}

#retrieve last post
@app.get("/posts/latest")
def get_latest_post():
    post= my_posts[len(my_posts)-1] 
    return {"latest_post": post}    

#retrieve a specific post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    return post

#@app.get("/posts/{id}")
#def get_post(id:int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id),)
    post= cursor.fetchone()
    #print(post)
    #post= find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
    return {"post_detail": post}
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    # find the index in the array that has the required id
    #my_posts.pop(index)
    #index= find_index_post(id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")             
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit() #conect with the database and save the change
    #index= find_index_post(id)
    #if index == None:
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found") 
    return {"data": updated_post}
    #post_dict= post.dict()
    #post_dict['id'] = id
    #my_posts[index]= post_dict
    #return {"data": my_posts[index]}    

@app.get("/_debug")
def debug():
    cursor.execute("SELECT inet_server_port() AS port")
    port = cursor.fetchone()["port"]
    cursor.execute("SELECT id FROM posts ORDER BY id")
    ids = [r["id"] for r in cursor.fetchall()]
    return {"db_port": port, "ids": ids}
