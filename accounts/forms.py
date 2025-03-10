from django import forms
from base.models import Item
from django.core.validators import FileExtensionValidator
from .models import Participant
class ParticipantRegistraionForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    ph_number = forms.CharField(required=True)
    name = forms.CharField(required=True)
    studentid = forms.CharField(required=True)
    photo = forms.ImageField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    id_card = forms.ImageField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    class Meta:
        model = Participant
        fields = [
            'name', 'studentid', 'password', 'confirm_password',
            'email', 'ph_number', 'zone', 'photo', 'id_card'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
        self.fields['name'].label = "Full Name"
        self.fields['password'].label = "Password"
        self.fields['confirm_password'].label = "Confirm Password"
        self.fields['email'].label = "E-Mail"
        self.fields['zone'].label = "Zone"
        self.fields['photo'].label = "Photo"
        self.fields['studentid'].label = "Student ID"
        self.fields['id_card'].label = "ID Card"
        self.fields['ph_number'].label = "Phone Number"

class ParticipationForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all(), label="Select Item", widget=forms.Select(attrs={'class': 'form-control'}))




