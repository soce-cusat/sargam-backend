"""
organisation/urls.py
"""

from django.urls import path, include
from base.views import ResultView, ResultDetailView, update_results


urlpatterns = [
    path('', include('accounts.urls')),
    path('results/', ResultView.as_view(), name="result_view"),
    path('results/<str:itmtype>/<str:pk>/', ResultDetailView.as_view(), name="result_detail_view"),
    path('results/update/', update_results, name="update_results"),
]
