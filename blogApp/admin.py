from django.contrib import admin
from blogApp.models import IpModel,AuthorProfile,CategoryList,TagName,Post

# Register your models here.

admin.site.site_header = "Blog Admin Section"
admin.site.index_title = "Admin Portal"

admin.site.register(AuthorProfile)
admin.site.register(CategoryList)
admin.site.register(TagName)
admin.site.register(Post)
admin.site.register(IpModel)