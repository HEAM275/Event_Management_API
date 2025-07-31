from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.exceptions import PermissionDenied

from drf_yasg import openapi as oa
from drf_yasg.utils import swagger_auto_schema

from modules.events.models.models import Category
from modules.events.serializers.category_serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer
)

from modules.common.utils import get_user_fullname


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.exclude(is_active=False)
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryListSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action in ['list']:
            return self.serializer_class
        if self.action in ['retrieve']:
            return CategoryDetailSerializer
        if self.action in ['create']:
            return CategoryCreateSerializer
        if self.action in ['partial_update', 'update']:
            return CategoryUpdateSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def perform_create(self, serializer):
        request = self.request
        user = request.user

        if user.is_authenticated:
            full_name = get_user_fullname(user)
            serializer.save(created_by=full_name, created_date=timezone.now())
        else:
            raise PermissionDenied(
                detail="You do not have permission to perform this action."
            )

    def perform_update(self, serializer):
        request = self.request
        user = request.user

        if user.is_authenticated:
            full_name = get_user_fullname(user)
            serializer.save(updated_by=full_name, updated_date=timezone.now())
        else:
            raise PermissionDenied(
                detail="You do not have permission to perform this action."
            )

    def perform_destroy(self, instance):
        request = self.request
        user = request.user

        if user.is_authenticated:
            full_name = get_user_fullname(user)
            instance.is_active = False
            instance.deleted_by = full_name
            instance.deleted_date = timezone.now()
            instance.save()
        else:
            instance.deleted_by = "Desconocido"
            instance.deleted_date = timezone.now()
            instance.is_active = False
            instance.save()

    @swagger_auto_schema(
        operation_description="List all active categories.",
        manual_parameters=[
            oa.Parameter(
                name="Authorization",
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: oa.Response(
                description="List of categories", schema=CategoryListSerializer(many=True)
            ),
            403: oa.Response(
                description="Forbidden",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={"detail": oa.Schema(type=oa.TYPE_STRING)},
                ),
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific category.",
        manual_parameters=[
            oa.Parameter(
                name="Authorization",
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: oa.Response(description="Category details", schema=CategoryDetailSerializer),
            403: oa.Response(
                description="Forbidden",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={"detail": oa.Schema(type=oa.TYPE_STRING)},
                ),
            ),
            404: oa.Response(
                description="Category not found",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={"detail": oa.Schema(type=oa.TYPE_STRING)},
                ),
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new category.",
        request_body=CategoryCreateSerializer,
        manual_parameters=[
            oa.Parameter(
                name="Authorization",
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            201: oa.Response(
                description="Category created successfully", schema=CategoryListSerializer
            ),
            400: oa.Response(
                description="Bad request",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        "message": oa.Schema(type=oa.TYPE_STRING),
                        "error": oa.Schema(type=oa.TYPE_OBJECT),
                    },
                ),
            ),
            403: oa.Response(
                description="Forbidden",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={"detail": oa.Schema(type=oa.TYPE_STRING)},
                ),
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {"message": _("Category created successfully"),
                 "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": _("Category could not be created"),
             "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_description="Update a category.",
        request_body=CategoryUpdateSerializer,
        manual_parameters=[
            oa.Parameter(
                name="Authorization",
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: oa.Response(
                description="Category updated successfully", schema=CategoryListSerializer
            ),
            400: oa.Response(
                description="Bad request",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={
                        "message": oa.Schema(type=oa.TYPE_STRING),
                        "error": oa.Schema(type=oa.TYPE_OBJECT),
                    },
                ),
            ),
            403: oa.Response(
                description="Forbidden",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={"detail": oa.Schema(type=oa.TYPE_STRING)},
                ),
            ),
            404: oa.Response(
                description="Category not found",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={"detail": oa.Schema(type=oa.TYPE_STRING)},
                ),
            ),
        },
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {"message": _("Category updated successfully"),
                 "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": _("Category could not be updated"),
             "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_description="Delete a category (soft delete: is_active=False).",
        manual_parameters=[
            oa.Parameter(
                name="Authorization",
                in_=oa.IN_HEADER,
                description="Bearer <access_token>",
                type=oa.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: oa.Response(
                description="Category deleted successfully",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={"message": oa.Schema(type=oa.TYPE_STRING)},
                ),
            ),
            403: oa.Response(
                description="Forbidden",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={"detail": oa.Schema(type=oa.TYPE_STRING)},
                ),
            ),
            404: oa.Response(
                description="Category not found",
                schema=oa.Schema(
                    type=oa.TYPE_OBJECT,
                    properties={"detail": oa.Schema(type=oa.TYPE_STRING)},
                ),
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"message": _("Category deleted successfully")},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": _("Category could not be deleted"),
                 "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
