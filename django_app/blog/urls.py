from django.conf.urls import url
from .views import HomeView
from .views import CreatePostView

app_name = 'blog'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^create/$', CreatePostView.as_view(), name='home'),
]
