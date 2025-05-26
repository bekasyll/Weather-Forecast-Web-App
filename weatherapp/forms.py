from django import forms

class CityForm(forms.Form):
    city = forms.CharField(label = "", max_length=30, required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter the city"}))