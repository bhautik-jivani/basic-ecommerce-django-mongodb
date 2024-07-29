from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from user_app.models import Role, Permission, User


class Command(BaseCommand):
    help = "Create initial setup"

    def handle(self, *args, **options):
        if Permission.objects.count() == 0:
            # Admin Permission
            Permission.objects.create(name="*", description="Admin Permission")

            # Role Permissions
            Permission.objects.create(name="view_role", description="View Role Permission")
            Permission.objects.create(name="add_role", description="Add Role Permission")
            Permission.objects.create(name="update_role", description="Update Role Permission")
            Permission.objects.create(name="delete_role", description="Delete Role Permission")

            # Permission Permissions
            Permission.objects.create(name="view_permission", description="View Permission")
            Permission.objects.create(name="add_permission", description="Add Permission")
            Permission.objects.create(name="update_permission", description="Update Permission")
            Permission.objects.create(name="delete_permission", description="Delete Permission")
            
            # User Permissions
            Permission.objects.create(name="view_user", description="View User Permission")
            Permission.objects.create(name="add_user", description="Add User Permission")
            Permission.objects.create(name="update_user", description="Update User Permission")
            Permission.objects.create(name="delete_user", description="Delete User Permission")

            # Product Permissions
            Permission.objects.create(name="view_product", description="View Product Permission")
            Permission.objects.create(name="add_product", description="Add Product Permission")
            Permission.objects.create(name="update_product", description="Update Product Permission")
            Permission.objects.create(name="delete_product", description="Delete Product Permission")
            
            # Cart Permissions
            Permission.objects.create(name="view_cart", description="View Cart Permission")
            Permission.objects.create(name="add_cart", description="Add Cart Permission")
            Permission.objects.create(name="update_cart", description="Update Cart Permission")
            Permission.objects.create(name="delete_cart", description="Delete Cart Permission")
            
            # Order Permissions
            Permission.objects.create(name="view_order", description="View Order Permission")
            Permission.objects.create(name="add_order", description="Add Order Permission")
            Permission.objects.create(name="update_order", description="Update Order Permission")
            Permission.objects.create(name="delete_order", description="Delete Order Permission")
        
        if Role.objects.count() == 0:
            # Admin Role
            admin_permissions = Permission.objects.filter(name__in = ["*"])
            Role.objects.create(name="admin", permissions = admin_permissions)

            seller_permissions = Permission.objects.filter(name__in = ["view_user_profile", "update_user_profile", "view_product", "add_product", "update_product", "delete_product", "view_order", "add_order", "update_order"])
            Role.objects.create(name="seller", permissions = seller_permissions)
            
            buyer_permissions = Permission.objects.filter(name__in = ["view_user_profile", "update_user_profile", "view_product", "view_cart", "add_cart", "update_cart", "delete_cart", "view_order", "add_order"])
            Role.objects.create(name="buyer", permissions = buyer_permissions)

        if User.objects.count() == 0:
            admin_roles = Role.objects.filter(name="admin")
            User.objects.create(name="admin", email="admin@example.com", password=make_password("admin@1"), contact_number="", roles=admin_roles, user_type="1")

            self.stdout.write(
                self.style.SUCCESS('Initial Setup created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Initial Setup already exist')
            )
        self.stdout.write(
            self.style.WARNING("Initial Admin user created with below credentials:\nemail: admin@example.com\npassword: admin@1"),
        )