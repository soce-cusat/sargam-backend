from django import forms

from accounts import models

class ParticipantRegistraionForm(forms.ModelForm):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = models.Participant

		fields = ['name', 'password', 'confirm_password', 'email', 'zone', 'photo']
		labels = {
			'name': "Full Name",
			'password': "Password",
			'confirm_password': "Confirm Password",
			'email': "E-Mail",
			'zone': "Zone",
			'photo': 'Photo'
		}
