from django import forms
<<<<<<< HEAD
from base.models import IndividualItem, Result
=======
from base.models import Item
>>>>>>> origin/main
from django.core.validators import FileExtensionValidator
from .models import Participant, Application

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
    item = forms.ModelChoiceField(queryset=IndividualItem.objects.all(), label="Select Item", widget=forms.Select(attrs={'class': 'form-control'}))



class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['item_name', 'first', 'second', 'third']

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        self.fields['first'].queryset = Participant.objects.none()
        self.fields['second'].queryset = Participant.objects.none()
        self.fields['third'].queryset = Participant.objects.none()

        print("Initializing ResultForm")
        if 'item' in self.data:
            try:
                event_id = int(self.data.get('item'))
                print(f"Event ID from data: {event_id}")
                accepted_applications = Application.objects.filter(
                    item_id=event_id, status='accepted'
                ).values_list('participant_id', flat=True)
                print(f"Accepted Applications: {list(accepted_applications)}")
                registered_participants = Participant.objects.filter(
                    id__in=accepted_applications
                )
                print(f"Registered Participants: {registered_participants}")
                self.fields['first'].queryset = registered_participants
                self.fields['second'].queryset = registered_participants
                self.fields['third'].queryset = registered_participants
            except (ValueError, TypeError) as e:
                print(f"Error processing item_name from data: {e}")
        elif self.instance.pk:
            event_id = self.instance.item_name.id
            print(f"Event ID from instance: {event_id}")
            accepted_applications = Application.objects.filter(
                item_id=event_id, status='accepted'
            ).values_list('participant_id', flat=True)
            print(f"Accepted Applications: {list(accepted_applications)}")
            registered_participants = Participant.objects.filter(
                id__in=accepted_applications
            )
            print(f"Registered Participants: {registered_participants}")
            self.fields['first'].queryset = registered_participants
            self.fields['second'].queryset = registered_participants
            self.fields['third'].queryset = registered_participants
        else:
            print("No item_name in data and no instance.pk")


    item = forms.ModelChoiceField(queryset=Item.objects.all(), label="Select Item", widget=forms.Select(attrs={'class': 'form-control'}))
