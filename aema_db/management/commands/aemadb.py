from django.core.management.base import BaseCommand, CommandError

# from django.conf.urls.defaults import *

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('action', nargs=1, type=str)

    def handle(self, *args, **options):
        action = args[0]
        print(action)
