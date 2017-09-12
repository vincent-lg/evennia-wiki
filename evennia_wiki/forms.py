from django import forms

class PageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    content = forms.CharField(widget=forms.Textarea)
