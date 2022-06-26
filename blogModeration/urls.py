from django.urls import path,include
from blogModeration.views import(
    ModerationView,
    AllPostView,
    AcceptPostView,
    RejectPostView,
    )

app_name = "blogModeration"
urlpatterns = [
    path('',ModerationView.as_view(),name="moderation_home_page_view"),
    path('dashboard/',ModerationView.as_view(),name="moderation_home_page_view"),
    path('all_post/',AllPostView.as_view(),name="moderation_all_post_view"),
    path('accept_post/',AcceptPostView.as_view(),name="moderation_accept_post_view"),
    path('reject_post/',RejectPostView.as_view(),name="moderation_reject_post_view"),

]

