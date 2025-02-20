import json
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from tables.models import (
    Author,
    Book,
    Category,
    Place,
    Publisher,
    Year
)


class Command(BaseCommand):
    help = 'Imports books from a JSON file'

    def handle(self, *args, **kwargs):
        # Load JSON data from file
        try:
            with open('bibliografija.json', 'r', encoding='utf-8-sig') as file:
                books_data = json.load(file)

            # Iterate over the data and create Book instances
            for item in books_data:
                try:

                    author, created = Author.objects.get_or_create(name=item['autor'])
                    publisher, created = Publisher.objects.get_or_create(name=item['izdavac'])
                    place, created = Place.objects.get_or_create(name=item['mesto'])
                    year = item['godina']
                    if year == '':
                        year = None
                    year, created = Year.objects.get_or_create(name=year)

                    book = Book(
                        author=author,
                        title=item['naziv'],
                        publisher=publisher,
                        place=place,
                        year=year,
                        created_by=User.objects.get(username='nemanja')
                    )
                    book.save()

                    category_objects = []
                    for category_name in item['tag']:
                        category, created = Category.objects.get_or_create(name=category_name)
                        category_objects.append(category)

                    book.category.set(category_objects)

                except ObjectDoesNotExist as e:
                    self.stderr.write(f"Error processing {item.get('naziv', 'Unknown')} - {e}")
                except Exception as e:
                    self.stderr.write(f"Unexpected error with {item.get('naziv', 'Unknown')} - {e}")

            self.stdout.write(self.style.SUCCESS('Books successfully imported!'))

        except FileNotFoundError as e:
            self.stderr.write(f"File not found: {e}")
        except json.JSONDecodeError as e:
            self.stderr.write(f"Error decoding JSON: {e}")
