from django.shortcuts import render, HttpResponse
from .models import Cow
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

"""
说明：要替换的内容
appName 替换为当前app的名称
ModelName 替换为当前app的名称，首字母大写
"""

# 页面标题
title = {
    "page_title": "员工列表",
    "page_heading": "员工",
    "modal_app_name": "cow",
    "modal_add_name": "cow_modal_add.html",
    "modal_update_name": "cow_modal_update.html",
    "modal_fetch_ajax_js_name": "cow_fetch_ajax_js.html"
}


def index(request):
    return render(request, "cow_index.html", title)
