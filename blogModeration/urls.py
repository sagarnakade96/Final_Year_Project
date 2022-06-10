from django.urls import path,include
from blogModeration.views import(ModerationView)

app_name = "blogModeration"
urlpatterns = [
    path('',ModerationView.as_view(),name="moderation_home_page_view")
]

