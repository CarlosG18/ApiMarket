from django.contrib.auth import get_user_model
from Apps.users.models import Role, Permission, UserRole, RolePermission

def create_users():
    # Define the roles and permissions
    roles_permissions = {
        'admin': [],
        'gerente': [],
        'operator': [],
    }

    # Create permissions
    for permission_name in {perm for perms in roles_permissions.values() for perm in perms}:
        permission, created = Permission.objects.get_or_create(name=permission_name)
        if created:
            print(f'Permission "{permission_name}" created')

    # Create roles and assign permissions
    for role_name, permissions in roles_permissions.items():
        role, created = Role.objects.get_or_create(name=role_name)
        if created:
            print(f'Role "{role_name}" created')

        for permission_name in permissions:
            permission = Permission.objects.get(name=permission_name)
            RolePermission.objects.get_or_create(role=role, permission=permission)

    # Create users for each role
    User = get_user_model()

    users_data = [
        {"email": "admin@example.com", "first_name": "Admin", "role": "admin"},
        {"email": "gerente@example.com", "first_name": "Gerente", "role": "Gerente"},
        {"email": "Operator@example.com", "first_name": "Operator", "role": "Operator"},
    ]

    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'first_name': user_data['first_name'],
                'password': User.objects.make_random_password(),
                'is_active': True,
                'is_staff': True if user_data['role'] == 'admin' else False,
            }
        )
        if created:
            print(f'User "{user.email}" created')

        role = Role.objects.get(name=user_data['role'])
        UserRole.objects.get_or_create(user=user, role=role)

    print('Roles, permissions, and users successfully created.')

create_users()