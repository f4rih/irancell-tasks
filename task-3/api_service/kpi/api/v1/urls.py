from django.urls import path
from kpi.api.v1.views import KPIView


urlpatterns = [
   path('kpi/', KPIView.as_view(), name='kpi'),
]

