from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
	url(r'^main/$' , views.main , name = "main")  ,
	url(r'^feature/(?P<company_name>[-\w]+)/$', views.feature , name = "feature") ,
	#url(r'^chart/(?P<company_name>[-\w]+)/$' , views.chart , name = "chart"),
	url(r'^simple_chart/(?P<company_name>[-\w]+)/$' , views.simple_chart , name = "simple_chart"),
	url(r'^detail_chart/(?P<company_name>[-\w]+)/$' , views.detail_chart , name = "detail_chart"),
	url(r'^feature_wise_chart/(?P<company_name>[-\w]+)/(?P<feature_name>[-\w]+)/$' , views.feature_wise_chart , name = "feature_wise_chart"),
	url(r'^main/(?P<company_name>[-\w]+)/$' , views.main1, name = "main1"),
	url(r'^reviews/(?P<company_name>[-\w]+)/$' , views.reviews, name = "reviews"),
	url(r'^specify_sentiment/(?P<company_name>[-\w]+)/(?P<sentiment_name>[-\w]+)/$' , views.specify_sentiment, name = "specify_sentiment")
	
]