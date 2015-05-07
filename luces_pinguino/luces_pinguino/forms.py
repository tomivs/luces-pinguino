from django import forms

class LucesForm(forms.Form):
    estado = forms.CharField(max_length=2)
    
    def clean(self):
        return self.cleaned_data
