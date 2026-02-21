
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view),
    path("profile/", views.profile_view),
    path("projects/", views.project_list),
    path("projects/update/<int:id>/", views.update_project),
    path("projects/submit/", views.submit_project),
]
