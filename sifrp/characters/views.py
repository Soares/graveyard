from django.shortcuts import render

def new(request):
    return render(request, 'characters/character.html')

def edit(request, id):
    return render(request, 'characters/character.html', {'id': id})
