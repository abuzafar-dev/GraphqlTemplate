# GraphQL Template

Django + graphene-django asosidagi GraphQL API shablon. Misol: mualliflar va kitoblar.

## Quick start

```bash
make run     # creates .venv and .env, installs deps, starts the app
make test    # checks + tests
```

## Ishga tushirish

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

GraphiQL: http://127.0.0.1:8000/graphql/

## So'rov namunalari

```graphql
mutation {
  createAuthor(name: "Abdulla Qodiriy") {
    author { id name }
  }
}
```

```graphql
mutation {
  createBook(title: "O'tgan kunlar", year: 1926, authorId: 1) {
    book { id title }
  }
}
```

```graphql
query {
  allBooks(search: "kun") {
    id
    title
    year
    author { name }
  }
}
```

Boshqa mutatsiyalar: `updateBook`, `deleteBook`. Bitta kitob: `book(id: 1)`, mualliflar: `allAuthors`.

## Testlar

```bash
python manage.py test
```
