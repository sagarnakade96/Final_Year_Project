import imp
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework import generics, status, exceptions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from rest_framework.permissions import AllowAny
from blogApp.models import Post,AuthorProfile,CategoryList
from django.contrib.auth.models import User
from blogApp.models import Post
# Create your views here.

class ModerationView(LoginRequiredMixin,View):
    template_name = "dashboard/index.html"

    def get(self, request, *args, **kwargs):                
        return render(request, self.template_name)
moderation_home_page_view = ModerationView.as_view()
class AllPostView(LoginRequiredMixin,View):
    template_name = "dashboard/docs.html"
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.filter(status='UR').first()
        data = {
            'mod_data' : post_data
        }

        return render(request, self.template_name,data)
moderation_all_post_view = AllPostView.as_view()

class AcceptPostView(LoginRequiredMixin,View):
    template_name = "dashboard/docs.html"
    def post(self, request, *args, **kwargs):
        post_id = request.data['post_id']
        print(post_id)
        post_data = Post.objects.filter(status='UR').first()
        data = {
            'mod_data' : post_data
        }

        return render(request, self.template_name,data)
moderation_accept_post_view = AcceptPostView.as_view()


class RejectPostView(LoginRequiredMixin,View):
    template_name = "dashboard/docs.html"
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.filter(status='UR').first()
        data = {
            'mod_data' : post_data
        }

        return render(request, self.template_name,data)
moderation_all_post_view = RejectPostView.as_view()
