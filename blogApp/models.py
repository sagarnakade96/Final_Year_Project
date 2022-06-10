from django.db import models
# Create your models here.
from blogApp.model_utils import TimestampModel, ModerationModel
from django.db.models import JSONField
from django.contrib.auth.models import User
from blogAdmin.choices import PostTypes, WelcomeTypes

class IpModel(models.Model):
    ip = models.CharField(max_length=200)

    def __str__(self):
        return self.ip

class AuthorProfile(TimestampModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogApp_users", unique=True)
    description = models.TextField( null=True, blank=True, default=WelcomeTypes.I_AM_USER)
    tagline = models.CharField(null=True,blank=True,default="I am blog user",max_length=200)
    extra_data = JSONField(default=dict, null=True, blank=True)
    class Meta:
        app_label = "blogApp"
        verbose_name = "author"
        verbose_name_plural = "authors"
        db_table = "blogApp_authors"
    def __str__(self):
        return f'{self.author}'

class CategoryList(TimestampModel):
    category_name=models.CharField(max_length=200)
    def __str__(self):
        return self.category_name    

class TagName(TimestampModel):
    tag_name = models.CharField(max_length=200)
    category_name = models.ForeignKey(CategoryList, on_delete=models.CASCADE, related_name="tag_category_name")
    def __str__(self):
        return self.tag_name   
    
class Post(TimestampModel,ModerationModel):   
    title = models.CharField(max_length=200)
    content = models.TextField(null=False,blank=False)
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=2, choices=PostTypes.choices, default=PostTypes.PUBLIC)
    category = models.ForeignKey(CategoryList, on_delete=models.CASCADE, related_name="post_category_list", default=1)
    cover_img = models.ImageField(null=True,blank=True)
    extra_data = JSONField(default=dict, null=True, blank=True)

    
    def __str__(self):
        return self.title



