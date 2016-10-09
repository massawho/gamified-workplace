from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url('^$', views.dashboard, name='dashboard'),
    url(r'^purchase/(?P<product_id>[0-9]+)/$', views.purchase_product, name='purchase_product'),
    url(r'^manager-to-collaborator/(?:(?P<user_id>[0-9]+)/)?$', views.manager_to_collaborator_questionnaire, name='manager_to_collaborator_questionnaire'),
    url(r'^task-feedback/(?:(?P<user_id>[0-9]+)/)?$', views.task_questionnaire, name='task_questionnaire'),
    url(r'^satisfaction/$', views.satisfaction_questionnaire, name='satisfaction_questionnaire'),
    url(r'^profile/update/$', views.update_profile, name='update_profile'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
