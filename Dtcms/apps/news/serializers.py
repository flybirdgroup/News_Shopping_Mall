from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from news.models import Category, News, NewsCategory


class SubNewsCategorySerializer(serializers.ModelSerializer):

    class Meta(object):
        # Cannot use ModelSerializer with Abstract Models.
        # model = Category
        model = NewsCategory
        fields = ('id', 'title')


class NewsCategorySerializer(serializers.ModelSerializer):

    # 子类别的序列化
    newscategory_set = SubNewsCategorySerializer(
        label='子类别', read_only=True, many=True)

    class Meta(object):
        model = NewsCategory
        exclude = ('parent',)


class NewsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = News
        fields = '__all__'

