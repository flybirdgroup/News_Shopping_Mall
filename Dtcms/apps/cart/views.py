from django.shortcuts import render

from django_redis import get_redis_connection
from redis.client import StrictRedis
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from cart.serializers import CartGoodsSerializer, CartSerializer, CartDeleteSerializer
from goods.models import Goods


def get_cart_count(request, strict_redis: StrictRedis):
    """获取购物车商品总数量"""
    count_list = strict_redis.hvals('cart_%s' % request.user.id)
    total_count = 0
    for count in count_list:
        total_count += int(count)
    return total_count


class CartCountView(APIView):

    def get(self, request):
        """获取购物车商品总数量"""
        redis_conn = get_redis_connection('cart')  # type: StrictRedis
        count = get_cart_count(request, redis_conn)
        return Response({'total_count': count})


class CartView(APIView):
    """
    购物车
    """
    def perform_authentication(self, request):
        """
        重写父类的用户验证方法，不在进入视图前就检查JWT
        """
        pass

    def post(self, request):
        """
        添加购物车
        """
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        goods_id = serializer.data.get('goods_id')
        count = serializer.data.get('count')

        # 尝试对请求的用户进行验证
        user = request.user
        # 用户已登录，在redis中保存
        redis_conn = get_redis_connection('cart')   # type: StrictRedis
        # 记录购物车商品数量
        redis_conn.hincrby('cart_%s' % user.id, goods_id, count)

        datas = {   # 返回购物车总条数
            'total_count': get_cart_count(request, redis_conn)
        }
        return Response(datas)

    def get(self, request):
        """
        获取购物车商品数据:
        cart_<user_id> : {
            'goods_id_1': count1,
            'goods_id_2': count2,
        }
        例如:
        cart_1 : {
            '1': 2,
            '2': 2,
        }
        """
        user = request.user  # 用户已经登录
        redis_conn = get_redis_connection('cart')   # type: StrictRedis
        cart_dict = redis_conn.hgetall('cart_%s' % user.id)

        goods_list = []
        for (key, val) in cart_dict.items():
            goods_id = int(key)
            count = int(val)
            goods = Goods.objects.get(id=goods_id)
            goods.count = count
            goods_list.append(goods)

        serializer = CartGoodsSerializer(goods_list, many=True)
        return Response(serializer.data)

    def put(self, request):
        """
        修改购物车数据
        """
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        goods_id = serializer.data.get('goods_id')
        count = serializer.data.get('count')

        # 尝试对请求的用户进行验证
        user = request.user
        redis_conn = get_redis_connection('cart')
        redis_conn.hset('cart_%s' % user.id, goods_id, count)

        datas = {  # 返回购物车总条数
            'total_count': get_cart_count(request, redis_conn)
        }
        return Response(datas)

    def delete(self, request):
        """
        删除购物车数据
        """
        serializer = CartDeleteSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        goods_id = serializer.data['goods_id']

        user = request.user
        redis_conn = get_redis_connection('cart')
        redis_conn.hdel('cart_%s' % user.id, goods_id)
        # return Response(status=status.HTTP_204_NO_CONTENT)

        datas = {  # 返回购物车总条数
            'total_count': get_cart_count(request, redis_conn)
        }
        return Response(datas)





