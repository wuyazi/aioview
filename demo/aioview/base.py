import functools

from aiohttp import web
from aiohttp import hdrs


def _embed_params(func):
    """
    embed params from match_info
    """
    @functools.wraps(func)
    def new_func(self, *args, **kwargs):
        kwargs.update(self.request.match_info)
        return func(self, *args, **kwargs)
    return new_func


class BaseApi(web.View):

    def __new__(cls, request):
        if request.method in hdrs.METH_ALL:
            method = request.method.lower()
            if hasattr(cls, method):
                # embed params from match_info
                embed_method = _embed_params(getattr(cls, method))
                setattr(cls, method, embed_method)
        return super(BaseApi, cls).__new__(cls)

    def output(self, data):
        return web.Response(text=data)