import re

from django_redis import get_redis_connection
from rest_framework import serializers, mixins
from users.models import User, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    """
    创建用户序列化器
    """
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_allow(self, value):
        """检验用户是否同意协议"""
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate_sms_code(self, sms_code):
        # 判断短信验证码
        # initial_data: 用户传递过来的未经过校验的数据(字典数据)
        mobile = self.initial_data.get('mobile')

        # 获取保存在Redis中的正确的短信验证码
        strict_redis = get_redis_connection('verify_codes')
        real_sms_code = strict_redis.get('sms_%s' % mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('短信验证码已过期')

        # lower(): 转换成小写字母 (不区分大小写)
        if sms_code.lower() != real_sms_code.decode().lower():
            raise serializers.ValidationError('短信验证码错误')

    def validate(self, data):
        # 判断两次密码
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码不一致')
        return data

    def create(self, validated_data):
        """
        创建用户
        """
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),  # 方法内部会对密码加密
            mobile=validated_data.get('mobile'))
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2',
                  'sms_code', 'mobile', 'allow')
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }


class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址序列化器
    """
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)

    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)

    class Meta:
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def validate_mobile(self, value):
        """
        验证手机号
        """
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def create(self, validated_data):
        """
        保存
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
