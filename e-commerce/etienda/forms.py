from typing import Any
from django import forms
from django.core.validators import MinValueValidator

class ProductoForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100,
                             error_messages={'required': 'Inserte un nombre correcto.'})
    precio = forms.DecimalField(label="Precio", 
                                validators=[MinValueValidator(0, message='El número debe ser igual o mayor que 0')])
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label='Descripción'
    )
    categoria = forms.CharField(max_length=100)
    imagen = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if nombre and not nombre[0].isupper():
            raise forms.ValidationError("El nombre debe comenzar con mayúscula.")
        return nombre
