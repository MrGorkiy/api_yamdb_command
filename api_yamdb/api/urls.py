from django.urls import include, path
from rest_framework import routers

from .views import (
    CaregoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    get_user_token,
    register_user_send_code,
)

app_name = "api"

router_v1 = routers.DefaultRouter()
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(r"categories", CaregoryViewSet, basename="categories")
router_v1.register(r"genres", GenreViewSet, basename="genres")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>"
    r"\d+)/comments/(?P<comment_id>\d+)",
    CommentViewSet,
    basename="comment",
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)",
    ReviewViewSet,
    basename="review",
)
router_v1.register(r"users", UserViewSet, basename="users")
urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", register_user_send_code, name="register"),
    path("v1/auth/token/", get_user_token, name="token"),
]
