from django import forms
from .models import Article

class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail")
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class ScriptForm(forms.Form):
    hauteur = forms.DecimalField(max_digits=7, decimal_places=0)

    
class PythonForm(forms.Form):
    hauteur = forms.DecimalField(max_digits=7, decimal_places=0)
    #transaction = forms.DecimalField(max_digits=7, decimal_places=0)
    
#, widget=forms.HiddenInput(),required = False  , widget=forms.HiddenInput()