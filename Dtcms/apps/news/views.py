from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import action

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from news.models import Category, News, NewsCategory
from news.serializers import NewsCategorySerializer, NewsSerializer, SubNewsCategorySerializer

# 用不到
# class NewsCategoryView(ListAPIView):
#     serializer_class = NewsCategorySerializer
#     queryset = NewsCategory.objects.all()


class NewsView(ViewSet):

    @action(methods=['get'], detail=False)
    def top(self, request):
        """获取界面顶部的新闻: 轮播图, 推荐新闻, 图片新闻"""
        '''
        返回的数据格式如下:
        {
            'slide_news': [{第1条新闻}, {第2条新闻}, ...],
            'top_news': [{第1条新闻}, {第2条新闻}, ...],
            'image_news': [{第1条新闻}, {第2条新闻}, ...]
        }
        '''
        # 轮播图新闻
        news_slide = News.objects.filter(is_slide=True).exclude(img_url='')
        # 推荐新闻
        news_top = News.objects.order_by('-create_time')[0:10]
        # 图片新闻
        news_image = News.objects.exclude(img_url='').order_by('-click')[0:4]

        serializer_slide = NewsSerializer(news_slide, many=True)
        serializer_top = NewsSerializer(news_top, many=True)
        serializer_imgs = NewsSerializer(news_image, many=True)

        context = {
            'slide_news': serializer_slide.data,
            'top_news': serializer_top.data,
            'image_news': serializer_imgs.data,
        }
        return Response(context)

    @action(methods=['get'], detail=False)
    def category(self, request):
        """获取类别新闻"""
        '''
        返回的数据格式如下:
        [
            {   # 第1个大类别
                'id': 3,
                'title': '互联网媒体',
                'category_set': [{'id':x1, 'title': '子类别1'}, {'id':x2, 'title': '子类别2'}],
                'news': [],
                'top8': [],
            },
            {   # 第2个大类别
                'id': 4,
                'title': '科技财经',
                'category_set': [{'id':x1, 'title': '子类别1'}, {'id':x2, 'title': '子类别2'}] 
                'news': [{新闻1},{新闻2}...],
                'top8': [{新闻1},{新闻2}...]                
            },
            ...
        ]
        '''
        list_data = []
        # 获取一级大类别
        categories = NewsCategory.objects.filter(parent_id=0)
        # 遍历每一个大类别
        for category in categories:
            dict_category = NewsCategorySerializer(category).data

            # 设置类别新闻
            child_category_ids = [category.id]
            # 设置二级子类别
            child_category_set = category.newscategory_set.all()
            for category in child_category_set:
                child_category_ids.append(category.id)

            news_set = News.objects.filter(category_id__in=child_category_ids)\
                           .order_by('-create_time').exclude(img_url='')[0:4]
            news_list = NewsSerializer(news_set, many=True).data
            dict_category['news'] = news_list

            # 设置最热门的8条新闻
            top8 = News.objects.filter(category_id__in=child_category_ids).order_by('-click')[0:8]
            news_list = NewsSerializer(top8, many=True).data
            dict_category['top8'] = news_list

            # 把一个大类别添加到列表中
            list_data.append(dict_category)

        return Response(list_data)

