from django.urls import path
from .views import ReportOpportunityView, arbitrage_opportunities_json

urlpatterns = [
    path("api/arbitrage_situation/report/", ReportOpportunityView.as_view(), name="report-arbitrage"),
     path("api/arbitrage_situation/list/", arbitrage_opportunities_json, name="arbitrage-list-json"),
    
    
]