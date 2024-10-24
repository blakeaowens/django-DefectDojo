from crum import get_current_user
from django.db.models import Exists, OuterRef, Q

from dojo.authorization.authorization import (
    get_roles_for_permission,
    role_has_permission,
    user_has_global_permission,
    user_has_permission,
)
from dojo.authorization.roles_permissions import Permissions
from dojo.group.queries import get_authorized_groups
from dojo.models import Global_Role, Product_Type, Product_Type_Group, Product_Type_Member


def get_authorized_product_types(permission):
    user = get_current_user()

    if user is None:
        return Product_Type.objects.none()

    if user.is_superuser:
        return Product_Type.objects.all().order_by("name")

    if user_has_global_permission(user, permission):
        return Product_Type.objects.all().order_by("name")

    roles = get_roles_for_permission(permission)
    authorized_roles = Product_Type_Member.objects.filter(product_type=OuterRef("pk"),
        user=user,
        role__in=roles)
    authorized_groups = Product_Type_Group.objects.filter(
        product_type=OuterRef("pk"),
        group__users=user,
        role__in=roles)
    product_types = Product_Type.objects.annotate(
        member=Exists(authorized_roles),
        authorized_group=Exists(authorized_groups)).order_by("name")
    return product_types.filter(Q(member=True) | Q(authorized_group=True))


def get_authorized_members_for_product_type(product_type, permission):
    user = get_current_user()

    if user.is_superuser or user_has_permission(user, product_type, permission):
        return Product_Type_Member.objects.filter(product_type=product_type).order_by("user__first_name", "user__last_name").select_related("role", "product_type", "user")
    return Product_Type_Member.objects.none()


def get_authorized_global_members_for_product_type(product_type, permission):
    user = get_current_user()

    if user.is_superuser or user_has_permission(user, product_type, permission):
        return Global_Role.objects.filter(group=None, role__isnull=False).order_by("user__first_name", "user__last_name").select_related("role", "user")
    return Global_Role.objects.none()


def get_authorized_groups_for_product_type(product_type, permission):
    user = get_current_user()

    if user.is_superuser or user_has_permission(user, product_type, permission):
        authorized_groups = get_authorized_groups(Permissions.Group_View)
        return Product_Type_Group.objects.filter(product_type=product_type, group__in=authorized_groups).order_by("group__name").select_related("role", "group")
    return Product_Type_Group.objects.none()


def get_authorized_global_groups_for_product_type(product_type, permission):
    user = get_current_user()

    if user.is_superuser or user_has_permission(user, product_type, permission):
        return Global_Role.objects.filter(user=None, role__isnull=False).order_by("group__name").select_related("role", "group")
    return Global_Role.objects.none()


def get_authorized_product_type_members(permission):
    user = get_current_user()

    if user is None:
        return Product_Type_Member.objects.none()

    if user.is_superuser:
        return Product_Type_Member.objects.all().order_by("id").select_related("role")

    if user_has_global_permission(user, permission):
        return Product_Type_Member.objects.all().order_by("id").select_related("role")

    product_types = get_authorized_product_types(permission)
    return Product_Type_Member.objects.filter(product_type__in=product_types).order_by("id").select_related("role")


def get_authorized_product_type_members_for_user(user, permission):
    request_user = get_current_user()

    if request_user is None:
        return Product_Type_Member.objects.none()

    if request_user.is_superuser:
        return Product_Type_Member.objects.filter(user=user).select_related("role", "product_type")

    if hasattr(request_user, "global_role") and request_user.global_role.role is not None and role_has_permission(request_user.global_role.role.id, permission):
        return Product_Type_Member.objects.filter(user=user).select_related("role", "product_type")

    product_types = get_authorized_product_types(permission)
    return Product_Type_Member.objects.filter(user=user, product_type__in=product_types).select_related("role", "product_type")


def get_authorized_product_type_groups(permission):
    user = get_current_user()

    if user is None:
        return Product_Type_Group.objects.none()

    if user.is_superuser:
        return Product_Type_Group.objects.all().order_by("id").select_related("role")

    product_types = get_authorized_product_types(permission)
    return Product_Type_Group.objects.filter(product_type__in=product_types).order_by("id").select_related("role")
