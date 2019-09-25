from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from goods.models import Goods, GoodsCategory
from goods.serializers import GoodsSerializer, GoodsCategorySerializer


class CategoryDetailView(RetrieveAPIView):
    """
    查询一个类别信息[面包屑导航]
    """
    serializer_class = GoodsCategorySerializer
    queryset = GoodsCategory.objects.all()


class GoodsRecommendView(APIView):
    # /goods/recommend/
    def get(self, request):
        """
        首页: 获取商品首页右侧的推荐商品
        """
        goods = Goods.objects.filter(is_red=1).order_by('-create_time')[0:4]
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)


class CategoryGoodsView(APIView):
    # /goods/category/
    def get(self, request):
        """首页: 获取首页的类别商品"""
        '''
        返回的数据格式如下:
        [
            {   # 第1个大类别
                'id': 3,
                'title': '互联网媒体',
                'category_set': [{'id':x1, 'title': '子类别1'}, {'id':x2, 'title': '子类别2'}],
                'goods': [{商品1},{商品2}...]
            },
            {   # 第2个大类别
                'id': 4,
                'title': '科技财经',
                'category_set': [{'id':x1, 'title': '子类别1'}, {'id':x2, 'title': '子类别2'}] 
                'goods': [{商品1},{商品2}...]                
            },
            ...
        ]
        '''
        list_data = []
        # 获取一级大类别  频道2为商城
        categories = GoodsCategory.objects.filter(parent_id=0)
        # 遍历每一个大类别
        for category in categories:
            dict_category = GoodsCategorySerializer(category).data
            # 设置二级子类别
            child_category_set = category.goodscategory_set.all()
            # 设置类别新闻
            child_category_ids = [category.id]
            for category in child_category_set:
                child_category_ids.append(category.id)

            # 一个大类别下的显示在首页的5个商品
            news_set = Goods.objects.filter(category_id__in=child_category_ids) \
                           .order_by('-create_time')[0:5]
            goods_list = GoodsSerializer(news_set, many=True).data
            dict_category['goods'] = goods_list

            list_data.append(dict_category)

        return Response(list_data)


class MyDjangoFilterBackend(DjangoFilterBackend):
    """自定义过滤管理器"""

    def filter_queryset(self, request, queryset, view):
        # 获取请求参数: 商品类别id
        category_id = request.query_params.get('category', None)
        if category_id is not None:
            category_ids = [category_id]
            try:  # 查询二级级类别
                category = GoodsCategory.objects.get(id=category_id)
                sub_category_set = category.goodscategory_set.all()
                for category in sub_category_set:
                    category_ids.append(category.id)

                # 只要属于这些二级类别的商品,都过滤出来返回
                return queryset.filter(category__in=category_ids)
            except:
                pass
        return queryset


class GoodsViewSet(ReadOnlyModelViewSet):
    """
    1. 商品列表界面: 查询所有的商品(过滤一个类别下的所有商品)
       http://127.0.0.1:8000/books/?ordering=-bread
    2. 商品详情界面: 查询一个商品的详细信息
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    # 指定过滤后台和排序字段
    filter_backends = [MyDjangoFilterBackend, OrderingFilter]
    filter_fields = ('category',)
    ordering_fields = ('create_time', 'sell_price', 'sales')
