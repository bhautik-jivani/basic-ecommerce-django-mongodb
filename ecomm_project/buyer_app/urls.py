from django.urls import path

from buyer_app import views

urlpatterns = [
    path('products/', views.ProductListViewSet.as_view({'get': 'list'})),
    path('products/<str:id>/', views.ProductListViewSet.as_view({'get': 'retrieve'})),

    path('cart/', views.CartCreateOrUpdateViewSet.as_view({'get': 'retrieve'}), name="cart-detail"),
    path('cart/add', views.CartCreateOrUpdateViewSet.as_view({'post': 'create'}), name="cart-create"),
    path('cart/update', views.CartCreateOrUpdateViewSet.as_view({'put': 'update'}), name="cart-update"),
]