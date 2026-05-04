from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context = {'val': "Menu Accueil"}
    return render(request, 'magasin/acceuil.html', context)