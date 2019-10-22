from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'message': 'This message is from Student app'
    }
    return render(request, 'base.html', context)
