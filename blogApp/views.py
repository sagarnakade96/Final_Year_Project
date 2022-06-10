from django.shortcuts import redirect, render
from django.views import View
from rest_framework.response import Response
from rest_framework import generics, status, exceptions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from rest_framework.permissions import AllowAny
from blogApp.models import Post,AuthorProfile,CategoryList
from django.contrib.auth.models import User

from blogApp.forms import(
    UpdateUserForm,
    UpdateProfileForm
)

from blogApp.serializers import (
    WritePostSerializer,
    RegistrationSerializer,
    CategorySerializer,
    TagSerializer
)

# Email imports

# Create your views here.
class BlogHomePageView(View):
    template_name = "storefront/index.html"

    def get(self, request, *args, **kwargs):                
        return render(request, self.template_name)
blog_home_page_view = BlogHomePageView.as_view()

class LoginView(generics.GenericAPIView):
    def get(self,request,*args, **kwargs):
        return render(request, self.template_name)
login_view = LoginView.as_view()

class RegistrationAPIView(generics.GenericAPIView):
    serializer = RegistrationSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        username = request.data["username"].lower()  # make username lowercase
        request.data["username"] = username  # update lowercased username
        if serializer.is_valid():
            user = serializer.save()
            profile = AuthorProfile.objects.create(author=user)
            return Response(
                {
                    "message": "User created successfully",                
                },
                status=status.HTTP_201_CREATED,
            )

        raise exceptions.ValidationError(serializer.errors)

class AboutUsView(View):
    template_name = "storefront/about.html"
    def get(self, request, *args, **kwargs):  
            return render(request, self.template_name)
about_us_view = AboutUsView.as_view()

class BlogView(View):
    template_name = "storefront/article.html"
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            author_first_post_info = Post.objects.filter(author=(AuthorProfile.objects.filter(author=request.user).first())).first()
            if author_first_post_info:
                author_next_post_info = Post.objects.filter(author=(AuthorProfile.objects.filter(author=request.user).first()))[1:2]
                author_rest_post_info = Post.objects.filter(author=(AuthorProfile.objects.filter(author=request.user).first()))[2:]        
                data = {
                    "author_first_post_info":author_first_post_info,
                    "author_next_post_info":author_next_post_info,
                    "author_rest_post_info":author_rest_post_info
                    }
                return render(request,self.template_name,data)
        author_first_post_info = Post.objects.filter().first()
        if author_first_post_info:
            author_next_post_info = Post.objects.all()[1:2]
            author_rest_post_info = Post.objects.all()[2:]
            data = {
                "author_first_post_info":author_first_post_info,
                "author_next_post_info":author_next_post_info,
                "author_rest_post_info":author_rest_post_info
                }
            return render(request,self.template_name,data)
        return render(request,self.template_name)
blog_view = BlogView.as_view()

class WriteView(LoginRequiredMixin,View):
    template_name = "storefront/write_page.html"
    def get(self, request, *args, **kwargs):
        category_list = CategoryList.objects.all()
        data={
            "category_list":category_list
        }
        return render(request, self.template_name,data)
    def post(self, request, *args, **kwargs):
            title = request.POST["title"]
            content = request.POST["content"]
            author = AuthorProfile.objects.filter(author=request.user).first()
            category = request.POST["category"]
            cover_img = request.POST["cover_img"]
            valid_category = CategoryList.objects.filter(category_name=category).first()
            if valid_category:
                post = Post(title=title,content=content,author=author,category=valid_category,cover_img=cover_img)
                post.save()
                data={
                    "message":"Post Successfully Saved!!!"
                }
                return render(request,self.template_name,data)
            return render(request,self.template_name)
write_post_view = WriteView.as_view()
    
class ProfileView(LoginRequiredMixin,View):
    template_name = "storefront/profile.html"    
    def get(self, request, *args, **kwargs):
        u_form = UpdateUserForm(instance=request.user)
        auth_profile = AuthorProfile.objects.filter(author=User.objects.filter(username=request.user).first()).first()
        p_form = UpdateProfileForm(instance=auth_profile)
        total_post = Post.objects.filter(author=auth_profile).count()
        if u_form and p_form:
            data={
                "p_form":p_form,
                "u_form":u_form,
                "auth_profile":auth_profile,
                "total_post":total_post
            }
            return render(request,self.template_name,data,status=status.HTTP_200_OK)
        return render(request,self.template_name,status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        auth_profile = AuthorProfile.objects.filter(author=User.objects.filter(username=request.user).first()).first()
        if auth_profile:
            username = request.POST["username"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            description = request.POST["description"]
            p_form = AuthorProfile.objects.filter(author=User.objects.filter(username=username).first()).first()
            u_form = User.objects.filter(username=username).first()
            if p_form and u_form:
                u_form.first_name = first_name
                u_form.last_name = last_name
                p_form.description = description
                u_form.save()
                p_form.save()
                messages.success(request,"Profile Updated Successfully!")
                return redirect(to='/api/v1/profile_page/',status=status.HTTP_201_CREATED)
            data={"message":"data failed to updated"}
            return render(request,self.template_name,data,status=status.HTTP_400_BAD_REQUEST)

        data={"message":"data failed to updated"}
        return render(request,self.template_name,data,status=status.HTTP_400_BAD_REQUEST)

class CategoryAPIView(LoginRequiredMixin,generics.GenericAPIView):
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category_name = serializer.save()
            return Response(
                {
                    "message": "new category added successfully",
                    "data":request.data               
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagAPIView(LoginRequiredMixin,generics.GenericAPIView):
    def post(self,request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(
                {
                    "message": "new tag added successfully",
                    "data":request.data               
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)