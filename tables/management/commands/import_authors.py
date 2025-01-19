import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction
from tables.models import Book, Author

class Command(BaseCommand):
    help = "Restore authors from an old SQLite database based on matching book titles."

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_db_path',
            type=str,
            help="Path to the backup SQLite database file."
        )

    def handle(self, *args, **options):
        backup_db_path = options['backup_db_path']
        
        self.stdout.write(self.style.NOTICE(f"Connecting to backup database: {backup_db_path}"))
        try:
            backup_conn = sqlite3.connect(backup_db_path)
        except sqlite3.Error as e:
            self.stderr.write(f"Error connecting to backup database: {e}")
            return
        
        try:
            with transaction.atomic():
                cursor = backup_conn.cursor()

                # Fetch all books from the old database
                cursor.execute("SELECT title, author_id FROM tables_book")
                backup_books = cursor.fetchall()

                for title, author_id in backup_books:
                    # Check for books with duplicate titles
                    matching_books = Book.objects.filter(title=title)
                    if matching_books.count() > 1:
                        self.stdout.write(
                            self.style.WARNING(f"Skipping '{title}' - multiple books share this title.")
                        )
                        continue
                    
                    # Proceed if there's exactly one match
                    try:
                        book = matching_books.get()
                    except Book.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Book not found in current DB: {title}"))
                        continue

                    # Fetch the Author object from the old database
                    cursor.execute("SELECT name FROM tables_author WHERE id = ?", (author_id,))
                    author_data = cursor.fetchone()
                    if not author_data:
                        self.stdout.write(self.style.WARNING(f"Author not found for title: {title}"))
                        continue
                    
                    author_name = author_data[0]

                    # Find or create the Author in the current database
                    author, created = Author.objects.get_or_create(name=author_name)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created new author: {author_name}"))

                    # Add the author to the book's many-to-many relationship
                    book.author.add(author)
                    self.stdout.write(self.style.SUCCESS(f"Restored author '{author_name}' to book '{title}'"))

                self.stdout.write(self.style.SUCCESS("Author restoration completed successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error during restoration: {e}"))
        finally:
            backup_conn.close()
            self.stdout.write(self.style.NOTICE("Backup database connection closed."))
