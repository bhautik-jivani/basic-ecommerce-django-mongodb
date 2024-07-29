from django.core.cache import cache

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from buyer_app.models import Cart, CartItem, Order, OrderItem
from buyer_app.serializers import CartSerializer
from seller_app.models import Product
from seller_app.serializers import BasicProductSerializer
from user_app.permissions import HasPermission

from bson import ObjectId
from bson.errors import InvalidId

# Create your views here.
class ProductListViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    authentication_classes = [JWTTokenUserAuthentication]
    serializer_class = BasicProductSerializer
    permission_required = ["*", "view_product"]
    lookup_field = 'id'

    def get_queryset(self):
        cache.clear()
        queryset = Product.objects.filter(product_status="1")
        return queryset
    
    def get_object(self):
        cache.clear()
        id = self.kwargs.get('id')
        try:
            ObjectId(id)
        except (TypeError, InvalidId):
            raise NotFound(f"{id} invalid product.")
        try:
            product_obj = Product.objects.get(id=id, product_status="1")
            return product_obj
        except Product.DoesNotExist:
            raise NotFound('Product does not found')
        
# class CartListViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated, HasPermission]
#     authentication_classes = [JWTTokenUserAuthentication]
#     permission_required = ["view_cart", "add_cart", "update_cart", "delete_cart"]
#     serializer_class = CartSerializer

#     def get_queryset(self):
#         cache.clear()
#         return Cart.objects.filter(created_by=self.request.user.id)

class CartCreateOrUpdateViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    authentication_classes = [JWTTokenUserAuthentication]
    permission_required = ["view_cart", "add_cart", "update_cart", "delete_cart"]
    serializer_class = CartSerializer

    def get_queryset(self):
        cache.clear()
        return Cart.objects.filter(created_by=self.request.user.id)
    
    def get_object(self):
        cache.clear()
        try:
            return Cart.objects.get(created_by=self.request.user.id)
        except Cart.DoesNotExist:
            raise NotFound('Cart does not found')
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user_id": self.request.user.id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data, context={"user_id": self.request.user.id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
