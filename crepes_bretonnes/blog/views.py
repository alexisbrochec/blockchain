from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render
from blog.models import Article
from django.shortcuts import render, get_object_or_404
from .forms import ContactForm
from .forms import TestForm
from .forms import ArticleForm
from django.core import management
import testpython


# Create your views here.

def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue sur mon blog !</h1>
        <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>
    """)



def date_actuelle(request):
    """ Afficher tous les articles de notre blog """
    articles = Article.objects.all() # Nous sélectionnons tous nos article
    #exec(open('test.py').read())
    #management.call_command('test.py', 1, 125000)
    return render(request, 'blog/accueil.html', {'derniers_articles': articles})

def accueil(request):
    """ Afficher tous les articles de notre blog """
    articles = Article.objects.all() # Nous sélectionnons tous nos articles
    return render(request, 'blog/accueil.html', {'derniers_articles': articles})

def test(request):
    """ Afficher tous les articles de notre blog """
    form = TestForm(request.POST or None)
    height = ['height']
    print(height)
    testpython.getblockhash(height)
    if form.is_valid():
        nom = form.cleaned_data['nom']
        message = form.cleaned_data['message']
        fichier=open("estuntest.txt", "w")
        fichier.write("voici le nom du gitan "+nom+"est il dit:"+message+"a la hauteur"+height)
        fichier.close()
        envoi = True
        
    return render(request, 'blog/test.html', locals())


def contact(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ContactForm(request.POST, instance =test)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        envoyeur = form.cleaned_data['envoyeur']
        renvoi = form.cleaned_data['renvoi']
        
        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        
        envoi = True
        form.save()
        
    # Quoiqu'il arrive, on affiche la page du formulaire.
    
    return render(request, 'blog/contact.html', locals())

def article(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    #form = ArticleForm(instance = Article) 
    form = ArticleForm(request.POST, instance=Article())        
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        titre = form.cleaned_data['titre']
        auteur  = form.cleaned_data['auteur']
        slug = form.cleaned_data['slug']
        contenu = form.cleaned_data['contenu']
        categorie = form.cleaned_data['categorie']

        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
        form.save()
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'blog/article.html', locals())



def lire(request, id, slug):
    try:
        article = get_object_or_404(Article, id=id, slug=slug)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'blog/lire.html', {'article': article})



def addition(request, nombre1, nombre2):    
    total = nombre1 + nombre2

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'blog/addition.html', locals())

def base(request):
    return render(request, 'blog/base.html')

def extends(request):
    return render(request, 'blog/extends.html')
