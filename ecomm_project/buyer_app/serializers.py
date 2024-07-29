from rest_framework import serializers

from buyer_app.models import Cart, CartItem, Order, OrderItem
from seller_app.models import Product, PRODUCT_STATUS
from seller_app.serializers import BasicProductSerializer

from bson import ObjectId
from bson.errors import InvalidId

class CartItemSerializer(serializers.Serializer):
    product = serializers.CharField(required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)

    def to_representation(self, instance):
       representation = super().to_representation(instance)
       representation['product'] = BasicProductSerializer(instance.product).data
       return representation

class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True, required=True, allow_empty=False)
    total_price = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)

    def validate_items(self, value):
        for item_detail in value:
            product_id = item_detail.get("product", "")
            product_quantity = item_detail.get("quantity", 0)

            try:
                ObjectId(product_id)
            except (TypeError, InvalidId):
                raise serializers.ValidationError(f"{product_id} invalid product.")
            try:
                product_obj = Product.objects.get(id=product_id, product_status="1")
                if product_obj.product_quantity < product_quantity:
                    raise serializers.ValidationError(f"{product_quantity} invalid product quantity, You are requested more than our stock, kindly change quantity.")
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"{product_id} invalid product.")
        return value

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        items = validated_data.pop("items")
        cart_items = []
        total_price = 0
        for cart_item in items:
            quantity = cart_item.get("quantity", 0)
            cart_item_obj = CartItem.objects.create(**cart_item)
            cart_items.append(str(cart_item_obj.id))
            total_price = total_price + (cart_item_obj.product.product_amount * quantity)

        try:
            cart_obj = Cart.objects.get(created_by = user_id)
            total_price = cart_obj.total_price + total_price
        except Cart.DoesNotExist:
            validated_data['created_by'] = user_id
            cart_obj = Cart.objects.create(items = cart_items, **validated_data)

        cart_obj.total_price = total_price
        cart_obj.save()
        return cart_obj
    
    def update(self, instance, validated_data):
        user_id = self.context.get('user_id')
        items = validated_data.pop("items")
        total_price = 0
        for cart_item in items:
            product_id = cart_item.get("product", "")
            quantity = cart_item.get("quantity", 0)
            try:
                ObjectId(product_id)
            except (TypeError, InvalidId):
                raise serializers.ValidationError(f"{product_id} invalid product.")
            
            try:
                cart_item_obj = CartItem.objects.get(product=product_id)
                cart_item_obj.quantity = quantity
                cart_item_obj.save()
                total_price = total_price + (cart_item_obj.product.product_amount * quantity)
            except CartItem.DoesNotExist:
                raise serializers.ValidationError(f"{product_id} not found in a cart.")
        
        cart_obj = Cart.objects.get(created_by = user_id)
        cart_obj.total_price = total_price
        cart_obj.save()
        return cart_obj
