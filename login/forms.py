from django import forms


class usuarioForm(forms.Form):

    usuario = forms.CharField(widget=forms.TextInput(attrs={'required': True,
                               'id':'userName',
                               'type':'text',
                               'placeholder':'Usuario',
                               'autocomplete' : "off",
                               'autofocus' : "true",
                              }),
                            label='Usuario', max_length=50
    )

    clave = forms.CharField(widget=forms.PasswordInput(render_value=False,
                            attrs={'required': True,
                                  'id':'pwd',
                                  'type':'password',
                                  'placeholder':'Contraseña',
                                  'autocomplete': "off",
                                  }),
                            label='Clave', max_length=30
    )