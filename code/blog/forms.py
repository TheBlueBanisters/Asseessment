from django import forms

class PublishBlogForm(forms.Form):
    title = forms.CharField(max_length=200,min_length=3,required=True)
    category =forms.IntegerField()
    content = forms.CharField(min_length=2)

