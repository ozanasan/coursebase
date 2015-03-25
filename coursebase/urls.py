from django.conf.urls import patterns, url
from coursebase import views
from coursebase.models import Topic

urlpatterns = patterns('', url(r'^$', views.index, name='index'), url(r'^about/', views.about, name='about'),  
	url(r'^topic/(?P<topic_name_slug>[\w\-]+)/$', views.topic, name='topic'),
	url(r'^add_topic/$', views.add_topic, name='add_topic'),
	url(r'^(?P<topic_name_slug>[\w\-]+)/add_lesson/$', views.add_lesson, name='add_lesson'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^topics/$', views.topics, name='topiclist'),
	url(r'^logout/$', views.user_logout, name='logout'),
	)

	
