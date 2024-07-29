from django.urls import path

from seller_app import views

urlpatterns = [
    path('products/', views.ProductListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('products/<str:id>/', views.ProductListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]

