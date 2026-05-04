from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vitrine/', views.vitrine, name='vitrine'),
    path('categories/', views.categories_produits, name='categories_produits'),
    path('categorie/<int:categorie_id>/', views.produits_par_categorie, name='produits_par_categorie'),
    path('nouvFournisseur/', views.nouveauFournisseur, name='nouveauFour'),
    path('nouvProduit/', views.nouveauProduit, name='nouveauProduit'),
    path('register/', views.register, name='register'),

]