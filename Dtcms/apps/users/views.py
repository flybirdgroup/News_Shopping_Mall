import random

from coreapi.auth import SessionAuthentication
from django_redis import get_redis_connection
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from users import serializers
from users.models import User
from libs.yuntongxun.sms import CCP


class SMSCodeView(APIView):
    """
    短信验证码
    """
    def get(self, request, mobile):
        """
        创建短信验证码
        """
        sms_code_redis_expires = 60 * 5  # 短信验证码的有效期为5分钟
        sms_code_expires = str(sms_code_redis_expires // 60)

        # 1. 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)

        # 2. 保存短信验证码与发送记录
        redis_conn = get_redis_connection('verify_codes')
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, sms_code_redis_expires, sms_code)
        pl.setex("send_flag_%s" % mobile, 60, 1)
        pl.execute()

        # 3. 发送短信验证码
        print('发送短信验证码:', sms_code)
        # ccp = CCP()
        # # 参数1: 接收的电话号码
        # # 参数2: [验证码, 过期时时间5分钟]
        # # 参数3: 使用编号为1的短信模板
        # ccp.send_template_sms(mobile, [sms_code, sms_code_expires], 1)

        return Response({"message": "OK"})


class UserView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializers.CreateUserSerializer


class AddressViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, GenericViewSet):
    """
    用户地址新增与修改
    """
    serializer_class = serializers.UserAddressSerializer

    # 注意: 已经在dev配置文件中配置了支持哪些认证方式
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    # GET /addresses/
    def list(self, request, *args, **kwargs):
        """
        用户地址列表数据
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'addresses': serializer.data,
        })

    # POST /addresses/
    def create(self, request, *args, **kwargs):
        """
        保存用户地址数据
        """
        # 检查用户地址数据数目不能超过上限
        count = request.user.addresses.count()
        if count >= 10:
            return Response({'message': '保存地址数据已达到上限'}, status=400)

        return super().create(request, *args, **kwargs)

    # delete /addresses/<pk>/
    def destroy(self, request, pk, *args, **kwargs):
        """
        处理删除
        """
        address = self.get_object()
        # 进行逻辑删除
        address.is_deleted = True
        address.save()
        return Response(status=204)

    @action(methods=['put'], detail=True)
    def status(self, request, pk=None, address_id=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=200)

