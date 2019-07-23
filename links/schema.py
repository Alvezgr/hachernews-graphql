import graphene
from graphene_django import DjangoObjectType

from links.models import Link


class LinkType(DjangoObjectType):
    """Type class for Link"""

    class Meta:
        model = Link


class Query(graphene.ObjectType):
    """Class query for the GraphQL server"""

    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        """Function for resolver for Link"""

        return Link.objects.all()


class CreateLink(graphene.Mutation):
    """This mutation will create Links
    an url and a description it's required
    """

    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()


    class Arguments:
        url = graphene.String()
        description = graphene.String()


    def mutate(self, info, url, description):
        """mutate method for Link"""
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )


class Mutation(graphene.ObjectType):
    """Mutation Class"""
    create_link = CreateLink.Field()
