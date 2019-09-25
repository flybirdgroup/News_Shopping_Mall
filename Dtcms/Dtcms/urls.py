"""DTcms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from areas import views
from areas.views import AreasViewSet
from goods.views import GoodsViewSet
from news.views import NewsView
from users.views import AddressViewSet

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 富文本编辑器
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^', include('news.urls')),
    url(r'^', include('goods.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include('cart.urls')),
    url(r'^', include('areas.urls')),
]


router = DefaultRouter()
router.register(r'news', NewsView, base_name='news')
router.register(r'goods', GoodsViewSet, base_name='goods')
router.register(r'areas', AreasViewSet, base_name='areas')
router.register(r'addresses', AddressViewSet, base_name='addresses')
urlpatterns += router.urls


