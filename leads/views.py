from django.shortcuts import render, HttpResponse


# 线索列表
leads_list_content = {
    "page_title": "线索池列表",
    "page_heading": "线索",
}


def leads_list(request):
    return render(request, "leads_list.html", leads_list_content)
