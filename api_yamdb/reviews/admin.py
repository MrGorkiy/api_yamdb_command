from django.contrib import admin

from .models import Category, Genre, Title, User, Comment, Review


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "description",
        "category",
        "year",
    )
    search_fields = (
        "pk",
        "name",
        "year",
    )
    list_editable = ("category",)
    list_filter = ("name", "year", "category", "genre")
    empty_value_display = "-пусто-"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",
    )
    search_fields = (
        "pk",
        "name",
        "slug",
    )
    list_filter = (
        "name",
        "slug",
    )
    empty_value_display = "-пусто-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",
    )
    search_fields = (
        "pk",
        "name",
        "slug",
    )
    list_filter = (
        "name",
        "slug",
    )
    empty_value_display = "-пусто-"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "role",
        "bio",
        "first_name",
        "last_name",
    )
    search_fields = (
        "pk",
        "username",
        "role",
        "email",
    )
    list_filter = (
        "username",
        "email",
    )
    empty_value_display = "-пусто-"


admin.site.register(Review)
admin.site.register(Comment)
