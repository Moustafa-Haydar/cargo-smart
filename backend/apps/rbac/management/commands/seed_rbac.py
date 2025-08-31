from django.core.management.base import BaseCommand
from apps.rbac.seed import seed_rbac

class Command(BaseCommand):
    help = "Seed default RBAC groups and permissions."

    def add_arguments(self, parser):
        parser.add_argument(
            "--silent",
            action="store_true",
            help="Suppress progress output.",
        )

    def handle(self, *args, **options):
        stdout = None if options.get("silent") else self.stdout
        seed_rbac(stdout=stdout)
        if stdout:
            self.stdout.write(self.style.SUCCESS("RBAC seeding done."))
