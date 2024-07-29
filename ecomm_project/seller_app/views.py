from django.core.cache import cache

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from seller_app.serializers import ProductSerializer
from seller_app.models import Product
from user_app.permissions import HasPermission

class ProductListViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = ProductSerializer
    permission_required = ["*", "view_product", "add_product", "update_product", "delete_product"]
    lookup_field = 'id'

    def get_queryset(self):
        cache.clear()
        queryset = Product.objects.filter(product_created_by=self.request.user.id)
        return queryset
    
    def get_object(self):
        cache.clear()
        id = self.kwargs.get('id')
        try:
            product_obj = Product.objects.get(id=id, product_created_by=self.request.user.id)
            return product_obj
        except Exception:
            raise NotFound('Product does not found')
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user_id": self.request.user.id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)