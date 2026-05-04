from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Produit, Fournisseur, Categorie
from .forms import ProduitForm, FournisseurForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
def index(request):
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/magasin')
    else:
        form = ProduitForm()
    
    products = Produit.objects.all()
    context = {'products': products, 'form': form}
    return render(request, 'magasin/mesProduits.html', context)

def nouveauFournisseur(request):
    if request.method == "POST":
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/magasin')
    else:
        form = FournisseurForm()
    
    fournisseurs = Fournisseur.objects.all()
    context = {'form': form, 'fournisseurs': fournisseurs}
    return render(request, 'magasin/fournisseur.html', context)

def nouveauProduit(request):
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/magasin')
    else:
        form = ProduitForm()
    
    produits = Produit.objects.all()
    context = {'form': form, 'produits': produits}
    return render(request, 'magasin/produits.html', context)
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def vitrine(request):
    liste = Produit.objects.all()
    return render(request, 'magasin/vitrine.html', {'list': liste})


def categories_produits(request):
    categories = Categorie.objects.all()
    produits = Produit.objects.all()

    return render(request, 'magasin/categories_produits.html', {
        'categories': categories,
        'produits': produits
    })


def produits_par_categorie(request, categorie_id):
    categories = Categorie.objects.all()
    categorie = get_object_or_404(Categorie, id=categorie_id)
    produits = Produit.objects.filter(categorie=categorie)

    return render(request, 'magasin/categories_produits.html', {
        'categories': categories,
        'produits': produits,
        'categorie_selectionnee': categorie
    })

def logout_view(request):
    logout(request)
    return redirect('home')