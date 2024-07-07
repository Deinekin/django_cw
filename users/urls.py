from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UpdatePassword, UserListView, UserUpdateView, \
    UserDeleteView, UserDetailView, change_user_activity_status

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("update_password/", UpdatePassword.as_view(), name="update_password"),
    path("users-<int:pk>/", UserDetailView.as_view(), name="view_user"),
    path("users/", UserListView.as_view(), name="view_all_users"),
    path("users/edit/<int:pk>/", UserUpdateView.as_view(), name="edit_user"),
    path("users/delete/<int:pk>", UserDeleteView.as_view(), name="delete_user"),
    path("users/change-activity/<int:pk>", change_user_activity_status, name="change-activity"),
]
