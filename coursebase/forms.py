from django import forms
from django.contrib.auth.models import User
from coursebase.models import Lesson, Topic, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class TopicForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Topic name.")
    likecount = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Topic
        fields = ('name',)

class LessonForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Title of the lesson")
    url = forms.URLField(max_length=200, help_text="URL of the lesson.")

    #I am attemting to override clean function to correct http:// prefix, which will usually be wrong.
    def clean(self):
    	cleaned_data = self.cleaned_data
    	url  =cleaned_data.get('url')

    	if url and not url.startswith('http://'):
    		url = 'http://' + url
    		cleaned_data['url'] = url
    	return cleaned_data

    class Meta:
        model = Lesson
        exclude = ('topic',)