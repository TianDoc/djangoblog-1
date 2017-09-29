#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import uuid
import json
from qiniu import Auth,put_data
import qiniu.config

@csrf_exempt
def upload_image(request, dir_name):
    
    ##################
    #  kindeditor图片上传返回数据格式说明：
    # {"error": 1, "message": "出错信息"}
    # {"error": 0, "url": "图片地址"}
    ##################
    #接收图片文件
    files = request.FILES.get("imgFile", None)
    if files:
        result = upload_image_to_qiniu(files,dir_name)
    else:
        result = {"error": 1, "message": "上传失败"}
    return HttpResponse(json.dumps(result), content_type="application/json")

def upload_image_to_qiniu(files,dir_name):
    allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.split(".")[-1]
    if file_suffix.lower() not in allow_suffix:
        return  {"error": 1, "message": "图片格式不正确"}
        #return HttpResponse(json.dumps(result), content_type="application/json")
    ACCESS_KEY = settings.QINIU_ACCESS_KEY
    SECRET_KEY = settings.QINIU_SECRET_KEY
    BUCKET_NAME = settings.QINIU_BUCKET_NAME
    PREFIX_URL = settings.PREFIX_URL
    QINIU_BUCKET_DOMAIN = settings.QINIU_BUCKET_DOMAIN
    #要保存在七牛服务器的图片名称
    qiniu_file_name = dir_name+ '/' + str(uuid.uuid1()) + "." + file_suffix
    #进行七牛上传
    q = Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME, qiniu_file_name, 3600)
    ret, info = put_data(token, qiniu_file_name, files)
    if ret:
        return {"error": 0, "url":  PREFIX_URL + QINIU_BUCKET_DOMAIN+'/'+qiniu_file_name}
    else:
        return {"error": 1, "message": "上传失败"}


