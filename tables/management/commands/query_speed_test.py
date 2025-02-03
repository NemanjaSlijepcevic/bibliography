from django.db import connection
from django.core.management.base import BaseCommand
from tables.models import Book
import time

class Command(BaseCommand):
    help = 'Start speed test'

    def handle(self, *args, **kwargs):
        start_time = time.time()
        books = list(Book.objects.all())
        end_time = time.time()

        print(f"Query execution time: {end_time - start_time:.4f} seconds")
        print(f"Total queries executed: {len(connection.queries)}")