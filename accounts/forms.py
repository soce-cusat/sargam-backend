from django import forms

from accounts import models

class ParticipantRegistraionForm(forms.ModelForm):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.required = True

	class Meta:
		model = models.Participant

		fields = ['name', 'studentid', 'password', 'confirm_password', 'email', 'zone', 'photo']
		labels = {
			'name': "Full Name",
			'password': "Password",
			'confirm_password': "Confirm Password",
			'email': "E-Mail",
			'zone': "Zone",
			'photo': 'Photo',
			'studentid': 'Student ID'
		}
