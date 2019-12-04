from django.shortcuts import render


def home_screen(request):
    return render(request, "base.html", {})