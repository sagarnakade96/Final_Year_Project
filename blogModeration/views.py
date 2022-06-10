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
# Create your views here.

class ModerationView(LoginRequiredMixin,View):
    template_name = "dashboard/index.html"

    def get(self, request, *args, **kwargs):                
        return render(request, self.template_name)
moderation_home_page_view = ModerationView.as_view()
