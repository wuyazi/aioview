from aiohttp.web import view

from user import UserApi


def setup_routes(app):
    app.router.add_routes([
        view('/user/{name:\w+}', UserApi),
    ])
