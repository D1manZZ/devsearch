from django.forms import ModelForm
from .models import Project, Review
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'tags', 'image', 'description', 'source_link']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class AddReview(forms.ModelForm):
    choices = [
        ('up', 'vote up'),
        ('down', 'vote down')
    ]
    vote = forms.ChoiceField(choices=choices, widget=forms.RadioSelect(), label='')
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'leave your comment here...'}),
        label='')

    class Meta:
        model = Review
        fields = ['vote', 'text']
