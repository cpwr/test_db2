from rest_framework.serializers import ModelSerializer

from blog.models import Post, Comment, Category
from register.models import CustomUser as User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'last_name',
            'birthday', 'is_active', 'is_superuser',
            'groups', 'user_permissions', 'country',
            'city', 'date_created', 'updated',
        )
