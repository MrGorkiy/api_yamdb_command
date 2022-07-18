from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator

from api.validators import validate_year


class User(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLES = [
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    ]
    username = models.CharField(
        max_length=150, null=False, blank=False, unique=True
    )
    email = models.EmailField(
        max_length=254, unique=True, null=False, blank=False
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default=USER)
    confirmation_code = models.CharField(
        max_length=150, blank=False, null=True
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or (self.role == self.ADMIN)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Category(models.Model):
    name = models.TextField("Наименование", max_length=256)
    slug = models.TextField("Ссылка", max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField("Наименование", max_length=256)
    slug = models.CharField("Ссылка", max_length=50, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.slug


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
        db_index=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        blank=True,
        db_index=True,
    )
    name = models.TextField("Название")
    year = models.IntegerField("Год", validators=[validate_year])
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10, "Оценка не может быть больше 10."),
            MinValueValidator(1, "Оценка не может быть меньше 1."),
        ],
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("pub_date",)
        constraints = [
            UniqueConstraint(fields=["title", "author"], name="unique_author")
        ]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("pub_date",)
