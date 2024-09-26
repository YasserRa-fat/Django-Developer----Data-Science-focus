from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Author, Book, Favorite
from faker import Faker
import random
from datetime import datetime

class Command(BaseCommand):
    help = 'Inserts 30 test authors, 30 test books, and some favorite entries'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create 30 authors
        authors = []
        for _ in range(30):
            author = Author.objects.create(
                id=fake.uuid4(),
                name=fake.name(),
                gender=random.choice(['Male', 'Female']),
                image_url=fake.image_url(),
                about=fake.text(),
                ratings_count=random.randint(0, 1000),
                average_rating=round(random.uniform(1.0, 5.0), 1),
                text_reviews_count=random.randint(0, 500),
                works_count=random.randint(1, 100),
                fans_count=random.randint(0, 1000),
                work_ids=[],
                book_ids=[]
            )
            authors.append(author)

        self.stdout.write(self.style.SUCCESS(f'Inserted 30 authors.'))

        # Create 200 books
        books = []
        for _ in range(200):
            book = Book.objects.create(
                id=fake.uuid4(),
                title=fake.sentence(nb_words=4),
                author_name=random.choice(authors).name,
                author_id=random.choice(authors).id,
                work_id=fake.uuid4(),
                isbn=fake.isbn10(),
                isbn13=fake.isbn13(),
                asin=fake.isbn10(),
                language='en',
                average_rating=round(random.uniform(1.0, 5.0), 1),
                rating_dist=f'5:{random.randint(0, 100)}, 4:{random.randint(0, 100)}, 3:{random.randint(0, 100)}, 2:{random.randint(0, 100)}, 1:{random.randint(0, 100)}',
                ratings_count=random.randint(100, 1000),
                text_reviews_count=random.randint(50, 500),
                publication_date=datetime.now().date(),
                original_publication_date=datetime.now().date(),
                format=random.choice(['Paperback', 'Hardcover', 'eBook']),
                edition_information='1st Edition',
                image_url=fake.image_url(),
                publisher=fake.company(),
                num_pages=random.randint(100, 1000),
                series_id=fake.uuid4(),
                series_name=fake.sentence(nb_words=3),
                series_position=str(random.randint(1, 5)),
                description=fake.text()
            )
            # Assign random authors to books
            book.authors.add(random.choice(authors))
            books.append(book)

        self.stdout.write(self.style.SUCCESS(f'Inserted 200 books.'))

        # Create a test user
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(username='testuser', password='testpassword')
            self.stdout.write(self.style.SUCCESS(f'Created test user "testuser".'))
        else:
            user = User.objects.get(username='testuser')

        # Check current favorite books count
        current_favorites_count = Favorite.objects.filter(user=user).count()
        books_to_add = min(15 - current_favorites_count, len(books))

        if books_to_add > 0:
            # Add favorites ensuring no more than 15 favorite books for the user
            favorite_books = random.sample(books, books_to_add)  # Limit to remaining slots
            for book in favorite_books:
                if Favorite.objects.filter(user=user, book=book).exists():
                    continue  # Skip if the book is already in favorites
                Favorite.objects.create(user=user, book=book)

            self.stdout.write(self.style.SUCCESS(f'Added {len(favorite_books)} favorite books for user "testuser".'))
        else:
            self.stdout.write(self.style.WARNING('User already has 15 favorite books. No new books were added.'))
