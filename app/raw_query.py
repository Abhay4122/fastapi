from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel      # use to strict the requested data type
from random import randrange
import psycopg2, time
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    name: str
    price: int
    # published: bool = True
    # rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='fastapi', user='abhay4122', password='aaaaaaaa',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()

        print('Database connection Done')
        break
    except Exception as e:
        print('Connection to database is failed')
        print(f'Error : {e}')
        time.sleep(10)


my_posts = [
    {
        'title': 'This is the first title for blog',
        'content': 'This is the first blog detail',
        'published': True,
        'id': 1
    },
    {
        'title': 'This is the second title for blog',
        'content': 'This is the second blog detail',
        'published': True,
        'id': 2
    }
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get('/')
async def root():
    return {'msg': 'Welcome to the fastapi'}


@app.get('/post')
async def get_posts():
    query = '''
        select * from products
    '''

    cursor.execute(query)
    data = cursor.fetchall()

    return {'data': data}


# @app.get('/post/latest')
# async def get_post():
#     post = my_posts[len(my_posts)-1]
#     return {'data': post}


@app.get('/post/{id}')
async def get_post(id: int, response: Response):
    query = f'''
        select * from products where id={id}
    '''
    cursor.execute(query)
    data = cursor.fetchone()

    post = data

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID: {id} was not found')
    return {'data': post}


@app.post('/createposts')
async def create_posts(payload: dict = Body(...)):
    # There is the body function will convert the post data into dect and insert into payload
    return {'data': payload}


@app.post('/post', status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    query = '''
        insert into products (name, price) values(%s, %s) returning *;
    '''
    
    cursor.execute(query, (new_post.name, new_post.price))
    data = cursor.fetchone()

    conn.commit()

    return {'data': data}


@app.put('/post/{id}', status_code=status.HTTP_200_OK )
def update_post(id: int, changable_post: Post):
    update_query = f'''
        update products set name='{changable_post.name}', price={changable_post.price}
        where id={id} returning *;
    '''
    cursor.execute(update_query)
    data = cursor.fetchone()

    conn.commit()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post found with ID {id}')

    return {'detail': f'Post with ID: {id} Updated successfully.'}



@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    query = f'''
        delete from products where id = {id} returning *;
    '''

    cursor.execute(query)
    data = cursor.fetchone()

    conn.commit()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post found with ID {id}')

    return Response(status_code=status.HTTP_204_NO_CONTENT)