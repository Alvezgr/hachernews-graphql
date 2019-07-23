import graphene
from graphene_django import DjangoObjectType

from links.models import Link


class LinkType(DjangoObjectType):
    """DjangoObjectType for GraphQL"""

    class Meta:
        model = Link


class Query(graphene.ObjectType):
    """Class query for the GraphQL server"""

    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        """Function for resolver for Link"""

        return Link.objects.all()


class CreateLink(graphene.Mutation):
    """Class for mutation in GraphQL"""

    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()


    class Arguments:
        url = graphene.String()
        description = graphene.String()


    def mutate(self, info, url, description):
        """Fuction that will mutate data"""
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )


class Mutation(graphene.ObjectType):
    """Class Mutation from graphene ObjectType"""
    create_link = CreateLink.Field()
