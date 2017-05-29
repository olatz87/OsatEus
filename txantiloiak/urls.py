from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^([0-9]+)/aldatu/berria/analiza/$', views.analizatzailea, name='analiza'),
    url(r'^([0-9]+)/berria/analiza/$', views.analizatzailea, name='analiza'),
    url(r'^([0-9]+)/fsnLortu/$',views.sct4text, name='sct4Text'),
    url(r'^([0-9]+)/aldatu/fsnLortu/$',views.sct4text, name='sct4Text'),
    #url(r'^txantiloiak/analizatzailea/$', views.analizatzailea),
    url(r'^(?P<pk>[0-9]+)/berria$', views.EspezialitateaView.as_view(), name='espezialitatea'),
    url(r'^(?P<pk>[0-9]+)/aldatu/(?P<txosten_id>[0-9]+)$', views.EspezialitateaView.as_view(), name='espezialitateaEdit'),
    url(r'^(?P<espezialitatea_id>[0-9]+)/gorde/$', views.gorde, name='gorde'),
    url(r'^(?P<txostena_id>[0-9]+)/gordeAld/$', views.gordeAldatua, name='gordeAldatua'),
    url(r'^laburpena/(?P<pk>[0-9]+)/$', views.LaburpenaView.as_view(), name='laburpena'),
#    url(r'^(?P<espezialitatea_id>[0-9]+)/proba/$', views.probaform_view, name='proba'),
#    url(r'^(?P<pk>[0-9]+)/gehitua/$', views.gehitua, name='gehitua'),
    #url(r'^analiza/^$', views.analizatzailea, name='analiza'), 
]


# urlpatterns = [
#     url(r'^$', views.IndexView.as_view(), name='index'),
#     url(r'^(?P<pk>[0-9]+)/$', views.EspezialitateaView.as_view(), name='espezialitatea'),
#     #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#     #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]
