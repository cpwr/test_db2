import graphene

from graphene_django.types import DjangoObjectType

from .models import Category
from .models import Comment
from .models import Post


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class Query(graphene.ObjectType):

    all_categories = graphene.List(CategoryType)
    all_comments = graphene.List(CommentType)
    all_posts = graphene.List(PostType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_comments(self, info, **kwargs):
        return Comment.objects.all()

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.all()
