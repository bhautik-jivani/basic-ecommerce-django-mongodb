from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from rest_framework import serializers

from seller_app.models import Product, PRODUCT_STATUS

import os
from decimal import Decimal


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    product_name = serializers.CharField(required=True)
    product_description = serializers.CharField()
    product_img = serializers.ImageField(source='product_img_url', required=False)
    product_img_url = serializers.CharField(read_only=True)
    product_amount = serializers.DecimalField(max_digits=9, decimal_places=2, min_value=Decimal(0.0))
    product_quantity = serializers.IntegerField(default=1, min_value=1)
    product_status = serializers.ChoiceField(choices=PRODUCT_STATUS)

    def create(self, validated_data):
        image_file = validated_data.pop('product_img_url', None)
        user_id = self.context.get('user_id')
        validated_data['product_created_by'] = user_id

        if image_file:
            file_name = default_storage.save(image_file.name, ContentFile(image_file.read()))
            product_img_url = os.path.join(settings.MEDIA_URL, file_name)
            validated_data['product_img_url'] = product_img_url

        product_obj = Product.objects.create(**validated_data)
        return product_obj

    def update(self, instance, validated_data):
        image_file = validated_data.pop('product_img_url', None)

        if image_file:
            instance.remove_img(instance.product_img_url)

            file_name = default_storage.save(image_file.name, ContentFile(image_file.read()))
            product_img_url = os.path.join(settings.MEDIA_URL, file_name)
            validated_data['product_img_url'] = product_img_url

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class BasicProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    product_name = serializers.CharField(read_only=True)
    product_description = serializers.CharField(read_only=True)
    product_img_url = serializers.CharField(read_only=True)
    product_amount = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)
    product_quantity = serializers.IntegerField(read_only=True)