from json import JSONDecodeError

from aiohttp import web
import logging
import redis
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')

logging.basicConfig()

r = redis.Redis(host=DB_HOST, port=DB_PORT, db=0)

routes = web.RouteTableDef()


@routes.post('/increment')
async def handle(request: web.Request):
    try:
        request_json = await request.json()
    except JSONDecodeError:
        logging.warning('request must be json')
        return web.json_response(
            data={
                'error': 'request must be json',
                'type': 3,
            },
            status=400,
        )

    try:
        number = request_json['number']
    except KeyError:
        logging.warning('field "number" missing')
        return web.json_response(
            data={
                'error': 'field "number" missing',
                'type': 3,
            },
            status=400,
        )

    if not isinstance(number, int) or number < 0:
        logging.warning('field "number" must be positive int')
        return web.json_response(
            data={
                'error': 'field "number" must be positive int',
                'type': 3,
            },
            status=400,
        )

    if r.sismember(DB_NAME, number):
        logging.warning('number already exists')
        return web.json_response(
            data={
                'error': 'number already exists',
                'type': 1,
            },
            status=400,
        )

    incremented_number = f'{number + 1}'
    if r.sismember(DB_NAME, incremented_number):
        logging.warning('incremented number already exists')
        return web.json_response(
            data={
                'error': 'incremented number already exists',
                'type': 2,
            },
            status=400,
        )

    r.sadd(DB_NAME, number)

    return web.json_response({
        'result': incremented_number,
    })


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, host=APP_HOST, port=APP_PORT)
