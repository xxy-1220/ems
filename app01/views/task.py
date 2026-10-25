from django.shortcuts import render


# 任务管理列表
def task_list(request):
    return render(request, "task_list.html")
