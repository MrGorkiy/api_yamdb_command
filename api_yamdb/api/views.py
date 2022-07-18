from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import ModelFilter
from .pagination import CommentPagination
from .permissions import IsAdminOnly, IsAdminOrReadOnly, IsOwnerAdminModerator
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    RegisterSerializer,
    ReviewSerializer,
    TitleCreatySerializer,
    TitleSerializer,
    TokenSerializer,
    UserNotAdminSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=username",)
    lookup_field = "username"

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def profile_users(self, request):
        user = request.user
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PATCH":
            if user.is_admin or user.is_superuser:
                serializer = UserSerializer(
                    user, data=request.data, partial=True
                )
            else:
                serializer = UserNotAdminSerializer(
                    user, data=request.data, partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ModelFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleSerializer
        return TitleCreatySerializer

    def get_serializer_context(self):
        context = super(TitleViewSet, self).get_serializer_context()
        reviews = Title.objects.annotate(rating=Avg("reviews__score"))
        context.update({"rating": reviews})
        return context


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CaregoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerAdminModerator,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        if Review.objects.filter(
            title=title.id, author=self.request.user
        ).exists():
            raise serializers.ValidationError("Вы уже оставили отзыв")
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = (IsOwnerAdminModerator,)

    def get_queryset(self):
        review = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("title_id"))
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, review=review, title=title)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user_send_code(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"],
        email=serializer.validated_data["email"],
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Registration in YaMDb",
        f"Your confirmation code is {confirmation_code}",
        f"{settings.CONTACT_EMAIL}",
        [user.email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_user_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user = get_object_or_404(
            User, username=serializer.validated_data["username"]
        )
    except User.DoesNotExist:
        return Response(
            {"username": "Invalid username."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    access = AccessToken.for_user(user)
    return Response({"access": str(access)}, status=status.HTTP_201_CREATED)
