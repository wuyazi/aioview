import sys
import asyncio

from aiohttp import web

from routes import setup_routes


def init_app(argv):
    # setup application and extensions
    app = web.Application()

    # setup views and routes
    setup_routes(app)

    return app


def main(argv):
    app = init_app(argv)
    web.run_app(app)


if __name__ == '__main__':
    main(sys.argv[1:])
