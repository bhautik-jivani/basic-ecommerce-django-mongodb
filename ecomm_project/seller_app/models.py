from mongoengine import Document, fields, ValidationError

from pathlib import Path


# Create your models here.
PRODUCT_STATUS = [
    ('0', 'Draft'),
    ('1', 'Publish'),
]

class Product(Document):
    product_name = fields.StringField(required=True)
    product_description = fields.StringField()
    product_img_url = fields.StringField(required=False)
    product_amount = fields.DecimalField(precision=2, default=0.00)
    product_quantity = fields.IntField(default=1)
    product_status = fields.StringField(default='0')
    product_created_by = fields.ReferenceField('user_app.User')

    def validate_product_status(self):
        if self.product_status not in dict(PRODUCT_STATUS).keys():
            raise ValidationError(f"Invalid choice for poduct_status: '{self.product_status}'. Allowed choices are: {PRODUCT_STATUS}")
    
    def remove_img(self, product_img_url, *args, **kwargs):
        if product_img_url:
            relative_file_path = self.product_img_url.lstrip('/')
            file_path = Path(relative_file_path)

            if file_path.exists():
                file_path.unlink()

    def delete(self, *args, **kwargs):
        self.remove_img(self.product_img_url)
        super().delete(*args, **kwargs)
