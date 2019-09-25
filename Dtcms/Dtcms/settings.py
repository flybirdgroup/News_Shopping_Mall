"""
Django settings for DTcms project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j4g5fazv&831k^z+fooajm*t=yiz0%8w_@jj-^f4d0ydcg1&@a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition
import sys
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',          # 实现跨域请求的第三方库
    'django_filters',       # 数据过滤功能

    # 'news.NewsConfig',            # 新闻模块
    # 'goods.GoodsConfig',          # 商品模块
    # 'users.UsersConfig',          # 用户模块
    # 'areas.AreasConfig',          # 区域管理

    'users',
    'cart',
    'goods',
    'news',
    'areas',
]

# 注册自定义的用户模型类
AUTH_USER_MODEL = 'users.User'

# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,      # 编辑器高度
        # 'width': 300,     # 编辑器宽
    },
}

CKEDITOR_UPLOAD_PATH = ''  # 上传图片保存路径，使用了FastDFS，所以此处设为''


# 可以通过哪些ip或域名访问当前服务器
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

MIDDLEWARE = [

    # 实现跨域请求添加的中间件类
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Dtcms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Dtcms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    # 连接远程的数据库
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_cms01',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'mysql',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# 认证后台: 使用此backend, 可以使用用户账号或电话号码进行登录
# AUTHENTICATION_BACKENDS = [
#     'users.utils.UsernameMobileAuthBackend',
# ]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_codes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# JWT
JWT_AUTH = {
    # token有效期1天
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 指定一个函数, 用来决定登录成功后需要返回哪些数据
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}




