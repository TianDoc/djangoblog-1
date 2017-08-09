# -*- coding: utf-8 -*-
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(wns==u5m6xvngooq^s(!r+&awhvk-98'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.xiuxiaowo.com','xiuxiaowo.com']

ADMINS = (
    ('zhanglei','akcj_zl@163.com'),
)


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'blog',
    'haystack',
    'django_crontab',
]

#定时任务
CRONJOBS = [
    ('00 02 * * *', 'django.core.management.call_command', ['mycommand'],{},'>> /var/run.log'),
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
             os.path.join(BASE_DIR,  'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'djangoblog.context_processor.get_setting',
                'djangoblog.context_processor.get_all_category',
                'djangoblog.context_processor.get_all_tag',
                'djangoblog.context_processor.get_contcats',
                'djangoblog.context_processor.art_list_by_view',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
#数据库配置
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myblog',
        'USER':'你的账户',
        'PASSWORD':'你的密码',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}

#redis缓存配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "你的redis密码"
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
#全文索引配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
#自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# MEDIA_URL = '/static/uploads/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'static/uploads').replace('\\', '/')

PAGE_SIZE = 8  #分页数

SITE_URL = 'https://www.xiuxiaowo.com/'
SITE_NAME = '朽小蜗'
SITE_DESC = '追求极简之美'
SITE_SEO_DESCRIPTION = '小站主要用来分享和记录学习经验,教程,记录个人生活的点滴以及一些随笔.欢迎大家访问小站'
SITE_SEO_KEYWORDS = '朽小蜗,个人博客,linux,apache,mysql,nginx,ubuntu,python,django,随笔,生活,爱心'
#七牛云配置
QINIU_ACCESS_KEY = '你的七牛账号'
QINIU_SECRET_KEY = '你的七牛密码'
QINIU_BUCKET_NAME = 'djangoblog'
QINIU_BUCKET_DOMAIN = 'images.xiuxiaowo.com'
QINIU_SECURE_URL = False      #使用http 

PREFIX_URL = 'https://'
MEDIA_URL = PREFIX_URL + QINIU_BUCKET_DOMAIN + '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage' 

ARTICLE_THUMB = '?imageView2/2/w/308'

#自定义日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
