"""Users Schema"""

import graphene

# Django imports
from django.contrib.auth import get_user_model

# Externals imports
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    """Type class for User"""

    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    """Query class for Users"""
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        """Function for resolver for Users"""
        return get_user_model().objects.all()

    def resolve_me(self, info, **kwargs):
        """Method for resolveing me"""
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")

        return user


class CreateUser(graphene.Mutation):
    """This mutation will create Users
    a password, email and username it's required
    """

    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)


    def mutate(self, info, username, password, email):
        """mutate method for User"""

        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    """Mutation class"""
    create_user = CreateUser.Field()
