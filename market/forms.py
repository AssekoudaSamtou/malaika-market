from django import forms
from django.contrib.auth.models import User

from .models import Image

class NewImageForm(forms.Form):
	photo = forms.ImageField()

class LoginForm(forms.Form):
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={"class":"form-control"}
			)
		)

	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={"class":"form-control"}
			)
		)

class RegisterForm(forms.Form):
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={"class":"form-control"}
			)
		)

	email = forms.EmailField(
		widget=forms.EmailInput(
			attrs={"class":"form-control", "placeholder":"example@gmail.com"}
			)
		)

	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={"class":"form-control"}
			)
		)

	password2 = forms.CharField(label="Confirm Password",
		widget=forms.PasswordInput(
			attrs={"class":"form-control"}
			)
		)

	def clean_username(self):
		username = self.cleaned_data.get("username")
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("Username is taken.")
		return username

	def clean_email(self):
		email = self.cleaned_data.get("email")
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("Email is taken.")
		return email

	def clean(self):
		data = self.cleaned_data
		password = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if password2 != password:
			raise forms.ValidationError("Posswords must match.")
		return data