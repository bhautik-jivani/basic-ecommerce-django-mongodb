from django.urls import path

from user_app import views

urlpatterns = [
    path('roles/', views.RoleCreateOrUpdateViewSet.as_view({'get': 'list', 'post': 'create'}), name="role-list-create"),
    path('role/<str:id>/', views.RoleCreateOrUpdateViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name="role-update"),

    path('permissions/', views.PermissionCreateOrUpdateViewSet.as_view({'get': 'list', 'post': 'create'}), name="permission-list-create"),
    path('permission/<str:id>/', views.PermissionCreateOrUpdateViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name="permission-update"),

    path('login/', views.LoginViewSet.as_view({'post': 'create'}), name="login"),
    path('register/', views.RegistrationViewSet.as_view({'post': 'create'}), name="registration"),

    path('user-profiles/', views.UserProfileViewSet.as_view({'get': 'list'}), name="user-profile-list"),
    path('user-profile/<str:id>/', views.UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name="user-profile-update"),
    path('profile/', views.ProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name="profile-update"),
]