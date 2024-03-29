import graphene
from graphene_django import DjangoObjectType

from django.db.models import Q

from links.models import Link, Vote
from users.schema import UserType

class LinkType(DjangoObjectType):
    """Type class for Link"""

    class Meta:
        model = Link


class VoteType(DjangoObjectType):
    """Type class for Vote"""

    class Meta:
        model = Vote


class Query(graphene.ObjectType):
    """Class query for the GraphQL server"""

    links = graphene.List(
        LinkType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
        )
    votes = graphene.List(VoteType)

    def resolve_links(self, info, search=None, first=None, skip=None, **kwargs):
        """Function for resolver for Link"""
        qs = Link.objects.all()

        if search:
            filter = (
                Q(url__icontains=search) |
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs

    def resolve_votes(self, info, **kwargs):
        """Function for resolver votes"""

        return Vote.objects.all()

class CreateLink(graphene.Mutation):
    """This mutation will create Links
    an url and a description it's required
    """

    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        url = graphene.String()
        description = graphene.String()


    def mutate(self, info, url, description):
        """mutate method for Link"""
        user = info.context.user or None
        link = Link(
            url=url,
            description=description,
            posted_by=user,
            )
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('You must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    """Mutation Class"""
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
