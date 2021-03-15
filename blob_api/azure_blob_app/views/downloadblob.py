from django.shortcuts import render

def view_a(request):
    return render(request, 'view_a.html')

def view_b(request):
    return render(request, 'view_b.html')