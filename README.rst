=======
aioview
=======

根据自己写 API 的习惯，封装的 view，适用于 aiohttp。

使用事例：

.. code-block:: python

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
