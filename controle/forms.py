from django import forms
from django.apps import apps
from .models import *
from django.conf import settings
from django.core.exceptions import ValidationError


def create_dynamic_titulo_form(model_name, fields=None, exclude=None):
    def clean_nome(self):
        return self.cleaned_data.get('nome').upper().strip()
    
    model = apps.get_model('controle', model_name)
    Meta = type('Meta', (), {'model':model, 'fields':fields, 'exclude':exclude})
    DynamicTituloForm = type(f'{model_name}Form', (forms.ModelForm,), {'Meta':Meta, 'clean_nome': clean_nome})
    if DynamicTituloForm.base_fields.get('nome'):
        DynamicTituloForm.base_fields['nome'].widget.attrs.update({'class': 'titulo', 'placeholder': model_name})
        DynamicTituloForm.base_fields['nome'].label = ''

    return DynamicTituloForm
        

class CompetenciaMensalForm(forms.ModelForm):
    tipo = forms.CharField(max_length=23, label='', widget=forms.TextInput(attrs={'class':'competencia', 'autocomplete': 'off'}))

    class  Meta:
        model = Competencia
        fields = ['tipo'] + Competencia.meses + ['obs']
        widgets = {field:forms.TextInput(attrs={'class': 'competencia', 'autocomplete':'off'}) for field in fields}
        widgets.update({'obs': forms.Textarea(attrs={
            'class': 'competencia',
            'rows': 1})})
        labels = {field:'' for field in fields}
    
    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo', None)
        if not kwargs.get('prefix'):
            kwargs['prefix'] = 'M'
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['id'] = field
            self.fields[field].widget.attrs['id'] = self.fields[field].widget.attrs['id'][:3] + self.fields[field].widget.attrs['id'][5:]

        if tipo:
            self.fields['tipo'].widget.attrs['value'] = tipo

    def clean_tipo(self):
        return self.cleaned_data.get('tipo').upper().strip()
        

class CompetenciaAnualForm(forms.ModelForm):
    tipo = forms.CharField(max_length=23, label='', widget=forms.TextInput(attrs={'class':'competencia', 'autocomplete': 'off'}))
    class Meta:
        model = Competencia
        fields = ['tipo', 'anual', 'obs']
        widgets = {field:forms.TextInput(attrs={'class': 'competencia', 'autocomplete':'off'}) for field in fields}
        widgets.update({'obs': forms.Textarea(attrs={
            'class': 'competencia',
            'rows': 1})})
        labels = {field:'' for field in fields}

    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo', None)
        if not kwargs.get('prefix'):
            kwargs['prefix'] = 'A'
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['id'] = field
        if tipo:
            self.fields['tipo'].widget.attrs['value'] = tipo

    def clean_tipo(self):
        return self.cleaned_data.get('tipo').upper().strip()


class DuplicarDadosForm(forms.Form):
    anos:dict = {str(ano):ano for ano in range(settings.ANO_INICIAL, settings.ANO_ATUAL+1)}
    de_ano:forms.ChoiceField = forms.ChoiceField(choices=anos, initial=str(settings.ANO_ATUAL-1))
    para_ano:forms.ChoiceField = forms.ChoiceField(choices=anos, initial=str(settings.ANO_ATUAL))

    def clean(self):
        if self.cleaned_data['de_ano'] == self.cleaned_data['para_ano']:
            raise ValidationError('Impossível duplicar dados para o mesmo ano')