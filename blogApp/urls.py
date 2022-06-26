from django.urls import path
from django.views.generic import TemplateView
from blogApp.views import (
    WriteView,
    RegistrationAPIView,
    CategoryAPIView,
    TagAPIView,
    ProfileView

)
from django.conf.urls.static import static
from blogAdmin import settings

from blogApp.views import (
    blog_home_page_view,
    about_us_view,
    blog_view,
)

app_name = "blogApp"
API_VERSION = "v1"

urlpatterns = [
    path("", view=blog_home_page_view, name="user_feed_list_view"),
    path("homepage/", view=blog_home_page_view, name="user_feed_list_view"),
    path("about_us/",view=about_us_view, name="about_us_view"),
    path("blog/",view=blog_view, name="blog_view"),
    path(f"api/{API_VERSION}/write/",WriteView.as_view(), name="write_view"),
    path(f"api/{API_VERSION}/profile_page/",ProfileView.as_view(), name="profile_view"),
    path("blog/",view=blog_view, name="blog_view"),
    path(f"api/{API_VERSION}/register/",RegistrationAPIView.as_view(), name="register"),
    path(f"api/{API_VERSION}/add_category/",CategoryAPIView.as_view(), name="add_category"),
    path(f"api/{API_VERSION}/add_tag/",TagAPIView.as_view(), name="add_tag"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)