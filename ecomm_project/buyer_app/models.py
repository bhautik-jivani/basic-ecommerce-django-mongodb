from django.utils import timezone

from mongoengine import Document, fields


# Create your models here.
class CartItem(Document):
    product = fields.ReferenceField("seller_app.Product")
    quantity = fields.IntField(required=True, default=1)

class Cart(Document):
    items = fields.ListField(fields.ReferenceField(CartItem))
    total_price = fields.DecimalField(precision=2, default=0.00)
    created_by = fields.ReferenceField("user_app.User")

class OrderItem(Document):
    product = fields.ReferenceField("seller_app.Product")
    product_amount = fields.DecimalField(precision=2, default=0.00)
    quantity = fields.IntField(required=True, default=1)

class Order(Document):
    items = fields.ListField(fields.ReferenceField(OrderItem))
    total_price = fields.DecimalField(precision=2, default=0.00)
    order_date = fields.DateTimeField(default=timezone.now)
    created_by = fields.ReferenceField("user_app.User")