from django import forms
from django.contrib.auth.models import User
from taps_oan.models import Pub, Beer, UserProfile


class PubForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the pub name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Pub
        fields = ('name',)


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class BeerForm(forms.Form):
    name = forms.CharField(max_length=128,
                            help_text="Please enter the name of the beer.")

    class Meta:
        fields = ('name')


class CarrierForm(forms.Form):
    name = forms.CharField(max_length=128, help_text="Please enter the name of the pub.")

    class Meta:
        fields = ('name')


class UpdateProfile(forms.ModelForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        return email