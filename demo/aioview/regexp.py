
import re


"""邮箱正则表达式"""
K_EMAIL_REG = r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'

"""手机号正则表达式"""
K_MOBILE_REG = r'^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^14[579]\d{8}$'

class Regexp(object):
    """
    正则表达式基类
    """
    def __init__(self, regex, flags=re.IGNORECASE):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)

        self.regex = regex

    def __call__(self, data):
        return self.regex.match(data or '')


class EmailRegexp(Regexp):
    """
    邮箱正则表达式
    """
    def __init__(self):
        # TODO：邮箱正则修改
        super(EmailRegexp, self).__init__(K_EMAIL_REG)

    def __call__(self, email=None):
        return super(EmailRegexp, self).__call__(email)


class MobileRegexp(Regexp):
    """
    手机号正则表达式
    """
    def __init__(self):
        super(MobileRegexp, self).__init__(K_MOBILE_REG)

    def __call__(self, mobile=None):
        return super(MobileRegexp, self).__call__(mobile)
