import re
from encodings.base64_codec import base64_decode

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回的数据
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


class UsernameMobileAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        校验用户名和密码是否正确
        :param username: 可以是用户名,也可以是电话号码
        :return: 登录成功的用户对象
        """
        try:
            # where mobile='xxx' or username='xxx'
            user = User.objects.get(Q(mobile=username)|Q(username=username))
        except User.DoesNotExist: # 用户名或电话号码不对
            user = None

        if user and user.check_password(password):
            # 用户名和密码正确
            return user

