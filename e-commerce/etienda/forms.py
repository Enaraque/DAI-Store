from django import forms


class ProductoForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100, )
    precio = forms.DecimalField(label="Precio")
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label='Descripción'
    )
    categoria = forms.CharField(max_length=100)
    # imagen = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
