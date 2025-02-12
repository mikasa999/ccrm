from django.shortcuts import render, HttpResponse


def leads_list(request):
    return render(request, "leads_list.html", {"title": "线索管理 列表"})

def leads_detail(request, id):
    return render(request, "leads_detail.html", {"title": "线索管理 详情", "id": id})

def leads_edit(request, id):
    return render(request, "leads_edit.html", {"title": "线索管理 编辑", "id": id})

def leads_delete(request, id):
    return render(request, "leads_delete.html", {"title": "线索管理 删除", "id": id})
