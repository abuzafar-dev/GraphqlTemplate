import json

from graphene_django.utils.testing import GraphQLTestCase

from library.models import Author, Book


class LibraryGraphQLTests(GraphQLTestCase):
    GRAPHQL_URL = '/graphql/'

    def setUp(self):
        self.author = Author.objects.create(name="Abdulla Qodiriy")
        self.book = Book.objects.create(title="O'tgan kunlar", year=1926, author=self.author)

    def test_all_books(self):
        response = self.query('{ allBooks { title year author { name } } }')
        self.assertResponseNoErrors(response)
        data = json.loads(response.content)['data']['allBooks']
        self.assertEqual(data[0]['author']['name'], 'Abdulla Qodiriy')

    def test_search_books(self):
        response = self.query('{ allBooks(search: "kun") { title } }')
        self.assertEqual(len(json.loads(response.content)['data']['allBooks']), 1)

    def test_create_book(self):
        response = self.query(
            'mutation ($authorId: ID!) { createBook(title: "Mehrobdan chayon", year: 1929, authorId: $authorId) { book { id title } } }',
            variables={'authorId': self.author.id},
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        response = self.query(
            'mutation ($id: ID!) { updateBook(id: $id, year: 1925) { book { year } } }',
            variables={'id': self.book.id},
        )
        self.assertResponseNoErrors(response)
        self.book.refresh_from_db()
        self.assertEqual(self.book.year, 1925)

    def test_delete_book(self):
        response = self.query(
            'mutation ($id: ID!) { deleteBook(id: $id) { ok } }',
            variables={'id': self.book.id},
        )
        self.assertTrue(json.loads(response.content)['data']['deleteBook']['ok'])
        self.assertFalse(Book.objects.exists())

    def test_create_book_wrong_author(self):
        response = self.query('mutation { createBook(title: "X", year: 2000, authorId: 999) { book { id } } }')
        self.assertResponseHasErrors(response)
