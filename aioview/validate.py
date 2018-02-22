import functools

from aiohttp.web import HTTPBadRequest

from .regexp import Regexp
from .regexp import EmailRegexp
from .regexp import MobileRegexp


def validate_params(validators=None, **options):

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not validators:
                return await func(self, *args, **kwargs)

            # get params
            pre_params = {k: v for k , v in self.request.query.items()}
            if self.request.method.lower() != "get":
                post_data = await self.request.post()
                pre_params.update(post_data)
            # validate params
            params = dict()
            for key, field in validators.items():
                field.validate(key=key, value=pre_params.get(key))
                params[key] = field.get_value()

            kwargs = dict({"params": params}, **kwargs)

            return await func(self, *args, **kwargs)
        return wrapper
    return decorator


class BaseValidator(object):

    def __init__(self, required=True, default=None, null=False, empty=False,
                choice=None, **kwargs):
        self.required = required
        self.default = default
        self.null = null
        self.empty = empty
        self.choice = choice

    def _value_to_str(self):
        if isinstance(self.value, bytes):
            self.value = self.value.decode('utf-8')
        try:
            self.value = str(self.value)
        except:
            raise HTTPBadRequest(text="")

    def _validate_null(self):
        if self.value is None:
            raise HTTPBadRequest(text="%s字段不能为空!" % self.key)

    def _validate_empty(self):
        if self.value in ("", {}, []):
            raise HTTPBadRequest(text="%s字段不能为空!" % self.key)

    def _validate_choice(self):
        if self.value not in self.choice:
            raise HTTPBadRequest(text="%s字段的取值只能是以下几种%s!" % (self.key, str(self.choice)))

    def validate(self, key, value):
        self.key = key
        self.value = value
        if isinstance(self.value, str):
            self.value = self.value.strip()
        if self.default and self.value is None:
            self.value = self.default
        if not self.null:
            self._validate_null()
        if not self.empty:
            self._validate_null()
            self._validate_empty()
        if self.choice:
            self._validate_choice()

    def get_value(self):
        return self.value


class StringValidator(BaseValidator):

    def __init__(self, min_length=None, max_length=None, **kwargs):
        super(StringValidator, self).__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length

    def _validate_min_length(self):
        if len(self.value) < self.min_length:
            raise HTTPBadRequest(text="%s字段长度不足!" % self.key)

    def _validate_max_length(self):
        if len(self.value) > self.max_length:
            raise HTTPBadRequest(text="%s字段长度太长!" % self.key)

    def validate(self, *args, **kwargs):
        super(StringValidator, self).validate(*args, **kwargs)
        self._value_to_str()
        if self.min_length:
            self._validate_min_length()
        if self.max_length:
            self._validate_max_length()


class IntValidator(BaseValidator):

    def __init__(self, min_num=None, max_num=None, **kwargs):
        super(IntValidator, self).__init__(**kwargs)
        self.min_num = min_num
        self.max_num = max_num

    def _value_to_int(self):
        if isinstance(self.value, bytes):
            self.value = self.value.decode('utf-8')
        try:
            self.value = int(self.value)
        except:
            raise HTTPBadRequest(text="%s不是int!" % self.key)

    def _validate_min_num(self):
        if self.value < self.min_num:
            raise HTTPBadRequest(text="%s小于最小值!" % self.key)

    def _validate_max_num(self):
        if self.value > self.max_num:
            raise HTTPBadRequest(text="%s大与最大值!" % self.key)

    def validate(self, *args, **kwargs):
        super(IntValidator, self).validate(*args, **kwargs)
        self._value_to_int()
        if self.min_num:
            self._validate_min_num()
        if self.max_num:
            self._validate_max_num()


class BoolValidator(BaseValidator):

    _false_str_list = ["False", "false", "No", "no", "0", "None",
                        "", "[]", "()", "{}", "0.0"]

    def __init__(self, *args, **kwargs):
        super(BoolValidator, self).__init__(*args, **kwargs)

    def _value_to_bool(self):
        self.value = self.value not in _false_str_list

    def validate(self, *args, **kwargs):
        super(BoolValidator, self).validate(*args, **kwargs)
        self._value_to_str()
        self._value_to_bool()


class RegexpValidator(BaseValidator):

    def __init__(self, reg=None, **kwargs):
        super(RegexpValidator, self).__init__(**kwargs)
        self.reg = reg

    def validate(self, *args, **kwargs):
        super(RegexpValidator, self).validate(*args, **kwargs)
        self._value_to_str()
        if self.reg:
            if not isinstance(self.reg, str):
                raise HTTPBadRequest(text="")
            if not Regexp(self.reg)(self.value):
                raise HTTPBadRequest(text="%s字段不符合格式要求!" % self.key)


class EmailValidator(BaseValidator):

    def __init__(self, *args, **kwargs):
        super(EmailValidator, self).__init__(*args, **kwargs)

    def validate(self, *args, **kwargs):
        super(EmailValidator, self).validate(*args, **kwargs)
        self._value_to_str()
        if not EmailRegexp()(self.value):
            raise HTTPBadRequest(text="%s字段不符合邮件格式!" % self.key)


class PhoneValidator(BaseValidator):

    def __init__(self, *args, **kwargs):
        super(PhoneValidator, self).__init__(*args, **kwargs)

    def validate(self, *args, **kwargs):
        super(PhoneValidator, self).validate(*args, **kwargs)
        self._value_to_str()
        if not MobileRegexp()(self.value):
            raise HTTPBadRequest(text="%s字段不符合手机号格式!" % self.key)
