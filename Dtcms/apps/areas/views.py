from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from areas.models import Area
from areas.serializers import AreaSerializer, SubAreaSerializer


class AreasViewSet(ModelViewSet):
    """
    行政区划信息
    """
    pagination_class = None  # 区划信息不分页
    queryset = Area.objects.all()

    def get_queryset(self):
        """
        提供数据集
        """
        if self.action == 'list':
            # 当查询区域列表数据时, 只返回省份数据
            return Area.objects.filter(parent=None)
        else:
            return AreasViewSet.queryset

    def get_serializer_class(self):
        """
        提供序列化器
        """
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubAreaSerializer


