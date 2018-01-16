import graphene

from graphene_django.types import DjangoObjectType
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):

    all_users = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()


class CreateUser(graphene.Mutation):

    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, password, email):
        user = User.objects.create_user(email, password)

        return CreateUser(user=user)


class LoginUser(graphene.Mutation):

    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, password, email):
        user = authenticate(password=password, email=email)
        if not user:
            raise Exception('Invalid username or password!')

        return LoginUser(user=user)


class ActivateUser(graphene.Mutation):

    user = graphene.Field(UserType)

    class Arguments:
        token = graphene.String(required=True)

    def mutate(self, info, token):
        qs = User.objects.filter(activation_key=token)
        if qs.exists() and qs.count() == 1:
            user = qs.first()
            if not user.confirmed:
                user.confirm(token)
                user.activation_key = None
                user.save()
        else:
            raise Exception('Valid user was not found.')
        return ActivateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    activate_user = ActivateUser.Field()
