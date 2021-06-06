from django.urls import path
from . import views
from django.contrib.auth import views as v

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail, name="post_detail"),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('exit/', v.LogoutView.as_view(next_page="/authorization/"), name='exit'),
]
