from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import ObtainJSONWebToken

from users import views

urlpatterns = [

    url(r'^users/$', views.UserView.as_view()),
    url(r'^sms_code/(?P<mobile>13\d{9})/$', views.SMSCodeView.as_view()),

    # 登录接口
    # ObtainJSONWebToken: drf内部封装的类视图,
    # 用于验证用户名和密码是否正确, 如果正确, 返回token
    url(r'^authorizations/$', ObtainJSONWebToken.as_view()),
]

# router = DefaultRouter()
# router.register(r'news', NewsView, base_name='news')
# urlpatterns += router.urls




