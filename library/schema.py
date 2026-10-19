import graphene
from graphene_django import DjangoObjectType

from library.models import Author, Book


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ['id', 'title', 'year', 'author']


class Query(graphene.ObjectType):
    all_books = graphene.List(BookType, search=graphene.String())
    book = graphene.Field(BookType, id=graphene.ID(required=True))
    all_authors = graphene.List(AuthorType)

    def resolve_all_books(root, info, search=None):
        books = Book.objects.select_related('author')
        if search:
            books = books.filter(title__icontains=search)
        return books

    def resolve_book(root, info, id):
        return Book.objects.filter(pk=id).first()

    def resolve_all_authors(root, info):
        return Author.objects.prefetch_related('books')


class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    author = graphene.Field(AuthorType)

    def mutate(root, info, name):
        author = Author.objects.create(name=name)
        return CreateAuthor(author=author)


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)
        author_id = graphene.ID(required=True)

    book = graphene.Field(BookType)

    def mutate(root, info, title, year, author_id):
        author = Author.objects.filter(pk=author_id).first()
        if author is None:
            raise Exception('Muallif topilmadi')
        book = Book.objects.create(title=title, year=year, author=author)
        return CreateBook(book=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        year = graphene.Int()

    book = graphene.Field(BookType)

    def mutate(root, info, id, title=None, year=None):
        book = Book.objects.filter(pk=id).first()
        if book is None:
            raise Exception('Kitob topilmadi')
        if title is not None:
            book.title = title
        if year is not None:
            book.year = year
        book.save()
        return UpdateBook(book=book)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, id):
        deleted, _ = Book.objects.filter(pk=id).delete()
        return DeleteBook(ok=deleted > 0)


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
