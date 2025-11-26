from django import forms


class Bootstrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": 'form-control', "placeholder": field.label}

class BootstrapForm(Bootstrap,forms.Form):
    pass

class BootstrapModelform(Bootstrap,forms.ModelForm):
    pass