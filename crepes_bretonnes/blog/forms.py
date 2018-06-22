from django import forms
from .models import Article


class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail")
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)
    
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        sujet = cleaned_data.get('sujet')
        message = cleaned_data.get('message')

        if sujet and message:  # Est-ce que sujet et message sont valides ?
            if "pizza" in sujet and "pizza" in message:
                raise forms.ValidationError(
                    "Vous parlez de pizzas dans le sujet ET le message ? Non mais ho !"
                )

            return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK
    

    
class TestForm(forms.Form):
    nom = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea)
    height =forms.CharField(max_length=150)
    
    def clean(self):
        #cleaned_data = super(ContactForm, self).clean()
        #nom = cleaned_data.get('nom')
       #message = cleaned_data.get('message')
       # height = cleaned_data.get('height')

    #if nom and message:  # Est-ce que sujet et message sont valides ?
        return self.nom 
    

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ('auteur','categorie','slug')  # Exclura les champs nommés « auteur », « categorie » et « slug »