from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel      # use to strict the requested data type
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


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
    return {'data': my_posts}


# @app.get('/post/latest')
# async def get_post():
#     post = my_posts[len(my_posts)-1]
#     return {'data': post}


@app.get('/post/{id}')
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'msg': f'Post with ID: {id} was not found'}
        # OR
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID: {id} was not found')
    return {'data': post}


@app.post('/createposts')
async def create_posts(payload: dict = Body(...)):
    # There is the body function will convert the post data into dect and insert into payload
    return {'data': payload}


@app.post('/post', status_code=status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    # There is Post class will validate the parameters post by client
    print(new_post)     # pydentic always give the value in this format
    post_dict = new_post.dict()
    print(post_dict)
    post_dict['id'] = randrange(0, 100)
    my_posts.append(post_dict)
    return {'data': post_dict}


@app.put('/post/{id}', status_code=status.HTTP_201_CREATED)
def update_post(id: int, changable_post: Post):
    print(changable_post)
    index = find_index_post(id)

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post found with ID {id}')
    
    post_dict = changable_post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {'detail': f'Post with ID: {id} Updated successfully.'}



@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)

    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No post found with ID {id}')

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)