from django.core.management.base import BaseCommand
from apps.rbac.seed import seed_rbac

class Command(BaseCommand):
    help = "Seed default RBAC groups and permissions."

    def handle(self, *args, **options):
        seed_rbac(stdout=self.stdout)
        self.stdout.write(self.style.SUCCESS("RBAC seeding done."))
