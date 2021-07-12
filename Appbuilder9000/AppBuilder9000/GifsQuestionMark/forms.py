from django import forms
from django.forms import ModelForm, Textarea
from .models import *

# class QuotesForm(ModelForm):
#     class Meta:
#         model = Quotes
#         fields = '__all__'

class QuotesForm(ModelForm):
    class Meta:
        model = Quotes
        widgets = {
            "quote_content": Textarea(attrs={"id": "counter-input"}),
        }
        fields = '__all__'

class QuotesForm_Tags(ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuotesForm_Tags, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control test',
                'id': 'tag_input',
            })
    class Meta:
        model = Quotes
        fields = ['tags']

######################add widgets here/ type date picker

class TagsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TagsForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
                'id': 'tag_input',
            })

    class Meta:
        model = Tags
        fields = ('__all__')

class QuestionsForm(ModelForm):
    question_text = forms.CharField(required=False)
    author_text = forms.CharField(required=False)
    class Meta:
        model = Question
        fields = ('question_text', 'author_text')

#
# class QuotesForm(ModelForm):
#     class Meta:
#         model = Quotes
#         widgets = {
#             "quote_content": Textarea(attrs={"id": "counter-input"}),
#         }
#         fields = '__all__'