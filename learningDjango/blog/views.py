from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from blog.models import Article
from .forms import ContactForm, ArticleForm, ScriptForm, PythonForm
from bitcointransaction import *

def script(request):

    form = ScriptForm(request.POST or None)

    if form.is_valid():
        hauteur = form.cleaned_data['hauteur']
        file = open("testfile.txt","w+")
        file.write("blockheight " + str(hauteur) + "\n")
        file.close()

        ecriture = True
    return render(request, 'blog/script.html', locals())

def InputOutput(request):

    transactionid="0b05c03271f2170aa92870a598768414a92d131b06f80c4d0ccb8e711e689b11"
    rawtransaction=getrawtransactionfromtransactionid(transactionid)
    decodedtransaction=decoderawtransactionfromrawtransaction(rawtransaction)
    listofvoutaddresses=getVoutaddresses(decodedtransaction)
    listofvaluesout =getValuesOut(decodedtransaction)
    listofvinadresses=getVinaddresses(decodedtransaction)
    
    return render(request, 'blog/InputOutput.html', locals())


def testpython(request):
    
    hauteur = askheight()
    return render(request, 'blog/testpython.html', locals())

def bitcointransaction(request):
    hauteur = "125000"
    ecriture = True
    blockhash=getblockhashfromheight(hauteur)
    block=getblockfromblockhash(blockhash)
    listoftransaction=getlistoftransactionidfromblock(block)
    end=len(listoftransaction)    
        
    return render(request, 'blog/bitcointransaction.html', locals())


def creerarticle(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ArticleForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        titre = form.cleaned_data['titre']
        auteur = form.cleaned_data['auteur']
        slug = form.cleaned_data['slug']
        contenu = form.cleaned_data['contenu']
        categorie = form.cleaned_data['categorie']

        # Nous pourrions ici envoyer l'e-mail grâce aux données
        # que nous venons de récupérer
        envoi = True

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'blog/creerarticle.html', locals())

def contact(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ContactForm(request.POST or None)
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

    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'blog/contact.html', locals())

def home(request):
    articles = Article.objects.all() # Nous sélectionnons tous nos articles
    return render(request, 'blog/accueil.html', {'derniers_articles': articles})

def lire(request, id, slug):
    article = get_object_or_404(Article, id=id, slug=slug)
    return render(request, 'blog/lire.html', {'article':article})

def view_article(request, id_article):
    if id_article > 100:
        raise Http404

    return redirect(view_redirection)

def view_redirection(request):
    return HttpResponse("Vous avez été redirigé.")

def list_articles(request, month, year):
    """ Liste des articles d'un mois précis. """
    return HttpResponse(
        "Vous avez demandé les articles de {0} {1}.".format(month, year)
    )

def date_actuelle(request):
    return render(request, 'blog/date.html', {'date': datetime.now()})


def addition(request, nombre1, nombre2):
    total = nombre1 + nombre2

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'blog/addition.html', locals())
