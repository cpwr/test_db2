from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer
from register.models import CustomUser as User

# Create your views here.


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
