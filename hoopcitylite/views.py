from django.shortcuts import render

# Create your views here.


def hoopCityLite(request):
    return render(request,"hoopcitylite/base.html")