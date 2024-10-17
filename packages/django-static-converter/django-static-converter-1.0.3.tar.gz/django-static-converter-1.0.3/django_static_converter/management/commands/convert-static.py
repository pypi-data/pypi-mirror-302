from django.core.management.base import BaseCommand
import os
from django.conf import settings
from django_static_converter.converter import convert_html_files

class Command(BaseCommand):
    help = 'Convert src and href attributes in Django HTML templates to static tags.'

    def handle(self, *args, **options):
        # Get the templates directory
        templates_dir = os.path.join(settings.BASE_DIR, 'templates')

        # Check if templates directory exists
        if not os.path.exists(templates_dir):
            self.stdout.write(self.style.ERROR('The templates folder does not exist in the root project.'))
            return  # Exit the command if the directory does not exist

        # Convert HTML files
        convert_html_files(templates_dir)

        self.stdout.write(self.style.SUCCESS('Static tags converted successfully!'))
