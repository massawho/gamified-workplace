from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url('^$', views.dashboard, name='dashboard'),
    url(r'^purchase/(?P<product_id>[0-9]+)/$', views.purchase_product, name='purchase_product'),
    url(r'^manager-to-collaborator/(?:(?P<user_id>[0-9]+)/)?$', views.ManagerToCollaboratorQuestionnaire.as_view(), name='manager_to_collaborator_questionnaire'),
    url(r'^task-feedback/(?:(?P<user_id>[0-9]+)/)?$', views.TaskQuestionnaire.as_view(), name='task_questionnaire'),
    url(r'^team-task-feedback/(?:(?P<team_id>[0-9]+)/)?$', views.TeamTaskQuestionnaire.as_view(), name='team_task_questionnaire'),
    url(r'^team-members-feedback/(?P<team_id>[0-9]+)/?$', views.TeamMembersQuestionnaire.as_view(), name='team_members_questionnaire'),
    url(r'^satisfaction/$', views.SatisfactionQuestionnaire.as_view(), name='satisfaction_questionnaire'),
    url(r'^profile/update/$', views.update_profile, name='update_profile'),
    url(r'^collaborators/$', views.collaborator_list, name='collaborator_list'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.profile, name='profile'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^team/(?P<pk>[0-9]+)/$', views.TeamDetail.as_view(), name='team_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
