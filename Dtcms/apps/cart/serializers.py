from rest_framework import serializers

from goods.models import Goods


class CartSerializer(serializers.Serializer):
    """
    列化器: 添加商品到购物车
    """
    goods_id = serializers.IntegerField(label='商品id', required=True, min_value=1)
    count = serializers.IntegerField(label='数量', required=True, min_value=1)

    def validate(self, data):
        try:
            goods = Goods.objects.get(id=data['goods_id'])
        except Goods.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        if data['count'] > goods.stock:
            raise serializers.ValidationError('商品库存不足')

        return data


class CartGoodsSerializer(serializers.ModelSerializer):
    """
    序列化器: 显示购物车的中商品
    """
    count = serializers.IntegerField(label='数量')
    # 此变量标识商品是否勾选
    selected = serializers.BooleanField(default=True, label='是否勾选', read_only=True)

    class Meta:
        model = Goods
        fields = ('id', 'title', 'img_url', 'sell_price', 'count', 'selected')


class CartDeleteSerializer(serializers.Serializer):
    """
    序列化器: 删除购物车中的商品
    """
    goods_id = serializers.IntegerField(min_value=1)

    def validate_goods_id(self, value):
        try:
            Goods.objects.get(id=value)
        except Goods.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return value