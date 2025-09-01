from django.core.management.base import BaseCommand
from apps.accounts.seed import seed_accounts

class Command(BaseCommand):
    help = "Seed default accounts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--silent",
            action="store_true",
            help="Suppress progress output.",
        )

    def handle(self, *args, **options):
        stdout = None if options.get("silent") else self.stdout
        seed_accounts(stdout=stdout)
        if stdout:
            self.stdout.write(self.style.SUCCESS("Accounts seeding done."))
