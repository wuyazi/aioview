
from aioview.validate import validate_params
from aioview.validate import StringValidator
from aioview.validate import EmailValidator
from aioview.api import BaseApi


class UserApi(BaseApi):

    get_params = {
        "email": EmailValidator(required=True, null=False),
        "ref": StringValidator(required=True, null=False),
    }

    @validate_params(get_params)
    async def get(self, name, params=None):
        text = "Hello, " + name
        return self.output(text)
