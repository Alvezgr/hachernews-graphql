import graphene
from graphene_django import DjangoObjectType

from links.models import Link


class LinkType(DjangoObjectType):
    """DjangoObjectType for GraphQL type"""

    class Meta:
        model = Link


class Query(graphene.ObjectType):
    """Class query for the GraphQL server"""

    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        """Function for resolver for Link"""

        return Link.objects.all()
