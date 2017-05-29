from django import forms
from .models import Txostena,Espezialitatea,Atala
from django.forms.models import inlineformset_factory,BaseInlineFormSet

#class TxostenaForm(forms.Form):
    

class EspezialitateaForm(forms.ModelForm):
    
    class Meta:
        model = Espezialitatea
        fields = '__all__'

class AtalaForm(forms.ModelForm):
    class Meta:
        model = Atala


AtalaFormSet = inlineformset_factory(Espezialitatea,Atala)
#class EspezialitateaInlineForm(forms.BaseInlineFormSet):
    
