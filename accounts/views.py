from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail

from .forms import ParticipantRegistraionForm
from .models import Participant, Zone
from config.settings.base import EMAIL_HOST_USER


User = get_user_model()

def create_verification_link(user):
	token = default_token_generator.make_token(user)
	uid = urlsafe_base64_encode(force_bytes(user.pk))
	verification_link = f"http://127.0.0.1:8000{reverse('verify_email', kwargs={'uidb64': uid, 'token': token})}"
	return verification_link

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('<h1> verified</h1>')
    else:
        return HttpResponse('<h1> failled </h1>')

class RegistrationView(TemplateView):
	template_name = "accounts/reg_login.html"
	
	def get(self, request):
		form = ParticipantRegistraionForm()
		return render(request, self.template_name, {"form": form})

	def post(self, request):
		form = ParticipantRegistraionForm(request.POST, request.FILES)
		if form.is_valid():
			form_data = form.cleaned_data
			new_user = User.objects.create_user(
				full_name=form_data['name'],
				email=form_data['email'], 
				password=form_data['password'],
				is_active=False
			)
			new_user.save()

			Participant.objects.create(
				user=new_user,
				name=form_data['name'],
				email=form_data['email'],
				zone=Zone.objects.get(id=form_data['zone'].id),
				photo=request.FILES['photo']
			)
			send_mail(
    			subject="Sargam Application Verification",
    			message=f"Click this link to verify your Application: {create_verification_link(new_user)}",
    			from_email=EMAIL_HOST_USER,
    			recipient_list=[form_data['email']],
    			fail_silently=False,
			)
			return HttpResponse('<h1> Created Successfully </h1>')

		return render(request, self.template_name, {"form": form})

