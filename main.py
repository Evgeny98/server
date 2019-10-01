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
    number = await request.text()
    try:
        parsed_number = int(number, 10)
    except ValueError:
        logging.warning('number parsing error')
        return web.Response(body='number parsing error', status=400)

    if parsed_number < 0:
        logging.warning('number must be positive')
        return web.Response(body='number must be positive', status=400)

    if r.sismember(DB_NAME, number):
        logging.warning('number already exists')
        return web.Response(body='number already exists', status=400)

    incremented_number = f'{parsed_number + 1}'
    if r.sismember(DB_NAME, incremented_number):
        logging.warning('incremented number already exists')
        return web.Response(body='incremented number already exists', status=400)

    r.sadd(DB_NAME, parsed_number)

    return web.Response(body=incremented_number)


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, host=APP_HOST, port=APP_PORT)
