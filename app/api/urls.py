from django.urls import path

from .views import GetUserView, CreateUserView


urlpatterns = [
    path('get_user', GetUserView.as_view()),
    path('create_user', CreateUserView.as_view()),
    # path('delete_user', DeleteUserView.as_view()),
]