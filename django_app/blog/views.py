from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from .models import Post


# Create your views here.

class HomeView(View, LoginRequiredMixin):

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('login')
        posts = Post.objects.order_by('-pub_date')
        return render(request, "feed.html", {"posts": posts})
