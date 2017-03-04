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


""" Not used anymore - always threw an integrity issue when adding adding
    a beer that already existed.
class BeerForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the beer.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Beer
        fields = ('title',)
        exclude = ('pub',)
"""


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class BeerForm(forms.Form):
    name = forms.CharField(max_length=128,
                            help_text="Please enter the name of the beer.")

    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        fields = ('name')


class CarrierForm(forms.Form):
    name = forms.CharField(max_length=128, help_text="Please enter the title of the beer carrier.")

    class Meta:
        fields = ('name')
