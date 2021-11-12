# from fastapi import FastAPI, status 
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from fastapi.params import Body

# import psycopg
# from psycopg.rows import dict_row
# import time

# from . import schemas


# app = FastAPI()


# while True:
#     try:
#         conn = psycopg.connect("host=localhost dbname=fastapi user=postgres password=king1997", row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error) 
#         time.sleep(2)

# @app.get("/")
# async def root():
#     return {"message": "Hello World!"}

# @app.post("/posts")
# def create_post(payload: schemas.Post):
#     cursor.execute(""" INSERT INTO posts (title, content, published)  VALUES (%s, %s, %s) RETURNING * """, (payload.title, payload.content, payload.published))
#     post = cursor.fetchone()
#     conn.commit() 

#     return get_response("post created successfully", status.HTTP_201_CREATED, post)

# @app.get("/posts")
# def get_posts():
#     cursor.execute(""" SELECT * FROM posts """)
#     posts = cursor.fetchall()

#     return get_response("posts retrieved successfully", status.HTTP_200_OK, posts)

# @app.get("/posts/{id}", response_model=schemas.Response)
# def get_post(id: int):
#     cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
#     post = cursor.fetchone()

#     if not post: 
#         return get_response(f"post with id: {id} was not found", status.HTTP_404_NOT_FOUND, None) 

#     return get_response("post retrieved successfully", status.HTTP_200_OK, post)

# @app.put("/posts/{id}")
# def update_post(id: int, payload: schemas.Post):
#     cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (payload.title, payload.content, payload.published, id,))
#     post = cursor.fetchone()
#     conn.commit()

#     if not post: 
#         return get_response(f"post with id: {id} was not found", status.HTTP_404_NOT_FOUND, None) 

#     return get_response("post updated successfully", status.HTTP_205_RESET_CONTENT, post)

# @app.delete("/posts/{id}")
# def delete_post(id: int,  ):
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
#     post = cursor.fetchone()
#     conn.commit()

#     if not post:
#         return get_response(f"post with id: {id} does not exist", status.HTTP_404_NOT_FOUND, None)

#     return get_response("post deleted successfully", status.HTTP_204_NO_CONTENT, post)


# def get_response(msg: str, code: int, data: any):  
#     return JSONResponse(
#         status_code=code,
#         content=jsonable_encoder({
#             "message": msg,
#             "status_code": str(code),
#             "data": data
#         })
#     )