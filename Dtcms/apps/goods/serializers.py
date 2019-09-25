from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsAlbum


class ASerializer(serializers.ModelSerializer):
    """商品子类别"""

    class Meta(object):
        model = GoodsCategory
        fields = ('id', 'title')


class SubGoodsCategorySerializer(serializers.ModelSerializer):
    """商品子类别"""

    # 关联对象（一个）： 父类别
    parent = ASerializer(read_only=True)

    class Meta(object):
        model = GoodsCategory
        fields = ('id', 'title', 'parent')


class GoodsCategorySerializer(serializers.ModelSerializer):
    """商品类别"""

    # 关联对象（多个）： 子类别
    goodscategory_set = SubGoodsCategorySerializer(
        label='子类别', read_only=True, many=True)
    # 关联对象（一个）： 父类别
    parent = ASerializer(read_only=True)

    class Meta(object):
        model = GoodsCategory
        fields = ('id', 'title', 'goodscategory_set', 'parent')


class AlbumSerializer(serializers.ModelSerializer):
    """商品图片（Album： 图库）"""

    class Meta(object):
        model = GoodsAlbum
        fields = ('id', 'thumb_path', 'original_path')


class GoodsSerializer(serializers.ModelSerializer):
    # 关联对象（多个）： 商品图片
    goodsalbum_set = AlbumSerializer(many=True, read_only=True)
    # 关联对象（一个）： 商品所属类别
    category = SubGoodsCategorySerializer(read_only=True)

    class Meta(object):
        model = Goods
        fields = '__all__'



