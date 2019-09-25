from django.conf.urls import url, include

from goods import views

urlpatterns = [

    # 首页:推荐商品
    url(r'^goods/recommend/$', views.GoodsRecommendView.as_view()),
    # 首页:类别商品
    url(r'^goods/category/$', views.CategoryGoodsView.as_view()),
    # 列表页: 面包屑导航
    url(r'^category/(?P<pk>\d+)/$', views.CategoryDetailView.as_view()),

]
