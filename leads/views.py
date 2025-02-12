from django.shortcuts import render, HttpResponse

# 线索列表
leads_list_content = {
    "title": "线索管理列表",
}


def leads_list(request):
    return render(request, "leads_list.html", leads_list_content)
