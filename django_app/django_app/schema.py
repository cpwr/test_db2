import graphene

from register.schema import Query as RegisterQuery
from register.schema import Mutation as RegisterMutation
from blog.schema import Query as BlogQuery


class Query(RegisterQuery, BlogQuery, graphene.ObjectType):
    pass


class Mutation(RegisterMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
