import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User
from .validators import validate_year


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")

    def validate_slug(self, value):
        if re.match(pattern=r"^[-a-zA-Z0-9_]+$", string=value):
            return value
        raise serializers.ValidationError(
            "Поле Slug содержит запрещенные символы"
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")

    def validate_slug(self, value):
        if re.match(pattern=r"^[-a-zA-Z0-9_]+$", string=value):
            return value
        raise serializers.ValidationError(
            "Поле Slug содержит запрещенные символы"
        )


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def get_rating(self, obj):
        rating = self.context["rating"]
        if obj in rating:
            return rating.get(pk=obj.pk).rating


class TitleCreatySerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )

    def validate_year(self, value):
        return validate_year(value)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("author", "title", "review")
        model = Comment

    def create(self, validated_data):
        review = validated_data['review']
        title = validated_data['title']
        if review.title_id != title.id:
            raise serializers.ValidationError(
                "Комментарий оставлен не на тот отзыв"
            )
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        fields = ("id", "author", "text", "score", "pub_date")
        read_only_fields = ("author", "title")
        model = Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User


class UserNotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)
        model = User


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Нельзя использовать me как username"
            )
        return value

    class Meta:
        fields = (
            "username",
            "email",
        )
        model = User


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        fields = (
            "username",
            "confirmation_code",
        )
        model = User
