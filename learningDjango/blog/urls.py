from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='accueil'),  # achanger pour rediriger vers la page html de l'affichage des Input/Output
    path('InputOutput', views.InputOutput, name='InputOutput'),# achanger pour rediriger vers la page html de l'affichage des Input/Output
    path('article/<int:id>-<slug:slug>$', views.lire, name='lire'),
    path('accueil', views.home),
    path('articles/<int:year>/<int:month>', views.list_articles),
    path('redirection', views.view_redirection),
    path('date', views.date_actuelle),
    path('addition/<int:nombre1>/<int:nombre2>/', views.addition),
    path('contact/', views.contact, name='contact'),
    path('creerarticle/', views.creerarticle, name='creationarticle'),
    path('script/', views.script, name='script'),
    path('testpython/', views.testpython, name='testpython'),
    path('bitcointransaction/', views.bitcointransaction, name='bitcointransaction')
]
