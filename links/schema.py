import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

#1
''' define uma classe mutação, em seguida, definida a saída da mutação, 
    os dados que o servidor poderá retornar ao user. A saída é definida 
    campo a campo para fins de aprendizado. Na próxima mutação, serão definidos como apenas um.'''
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    #2
    '''Define os dados que podem ser enviados para o servidor, nesse caso, o URL e a descrição dos links.'''
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    #3
    '''O método de mutação: cria um link no banco de dados usando os dados enviados pelo usuário, através dos parâmetros
        url e description. Depois, o servidor retorna a classe CreateLink com os dados que acabaram de ser criados. Veja como 
        isso corresponde aos parâmetros definidos em # 1.'''
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )


'''Cria uma classe de mutação com um campo a ser resolvido, o que aponta para a nossa mutação definida anteriormente.'''
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
