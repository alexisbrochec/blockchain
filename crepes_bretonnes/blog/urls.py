from django.urls import path
from . import views


urlpatterns = [
    path('accueil2', views.home),
    path('date', views.date_actuelle),
    path('addition/<int:nombre1>/<int:nombre2>/', views.addition),
    path('base', views.base),
    path('extends', views.extends),
    path('accueil', views.accueil, name='accueil'),
    path('article/<int:id>-<slug:slug>$', views.lire, name='lire'),
    path('contact/', views.contact, name='contact'),
    path('article2/', views.article, name='article'),
    path('test', views.test, name='test')
]