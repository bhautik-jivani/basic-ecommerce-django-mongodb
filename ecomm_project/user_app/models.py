from django.utils import timezone

from mongoengine import Document, fields, ValidationError

from bson import ObjectId

USER_TYPES = [
    ('1', 'admin'),
    ('2', 'supplier'),
    ('3', 'buyer'),
]

class Permission(Document):
    name = fields.StringField(max_length=50, required=True)
    description = fields.StringField()

class Role(Document):
    name = fields.StringField(required=True, unique=True)
    permissions = fields.ListField(fields.ReferenceField(Permission), default=[])

class User(Document):
    email = fields.EmailField(unique=True, required=True)
    password = fields.StringField(required=True)
    name = fields.StringField(max_length=100, blank=True, default='')
    date_joined = fields.DateTimeField(default=timezone.now)
    bio = fields.StringField()
    profile_picture = fields.ImageField()
    contact_number = fields.StringField(required=True, max_length=15)
    roles = fields.ListField(fields.ReferenceField("user_app.Role"), default=[])
    user_type = fields.StringField(default="3")
    is_active = fields.BooleanField(default=True)

    def validate_user_type(self):
        if self.user_type not in dict(USER_TYPES).keys():
            raise ValidationError(f"Invalid choice for user_type: '{self.user_type}'. Allowed choices are: {USER_TYPES}")


