from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import render
from .models import GroupItem 
from django.shortcuts import redirect
from accounts.models import Participant
from .models import GroupItem, Item


class BaseWorkerViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', ]
    permission_classes = [permissions.IsAuthenticated]


class PointDataBaseViewSet(BaseWorkerViewSet):
    def get_queryset(self):
        return self.queryset.filter(added_by=self.request.user)


class WorkerBaseViewSet(PointDataBaseViewSet):
    pass


class PrivacyView(TemplateView):
    template_name = 'privacy.html'

class ResultView(TemplateView):
    template_name = "base/result.html"

    def get(self, request):
        group_items = list(GroupItem.objects.all()) 
        individual_items = list(Item.objects.all())
        return render(request, self.template_name, {"context": {
                            "group": group_items,
                            "individual": individual_items
                            }})

class ResultDetailView(TemplateView):
    template_name = "base/result_detail.html"

    def get(self, request, pk, itmtype):
        if itmtype == "individual":
            item = Item.objects.get(id=pk)
        elif itmtype == "group":
            item = GroupItem.objects.get(id=pk)
        else:
            # render 404
            pass
        return render(request, self.template_name, {"item": item})

# def update_results(request):
#     individual_items = IndividualItem.objects.all()
#     participants = Participant.objects.all()
#     context = {
#         'individual_items': individual_items,
#         'participants': participants,
#     }
#     return render(request, 'base/staff_page.html', context)


# # Check if user is StageStaff
# def is_stage_staff(user):
#     return user.groups.filter(name='StageStaff').exists()

