# apps/rbac/management/commands/run_seeds.py
from django.core.management.base import BaseCommand
from django.core.management import call_command

# python manage.py run_seeds

SEED_COMMANDS = [
    "seed_rbac",
    "seed_accounts",
    "seed_geo",
    "seed_routes",
    "seed_vehicles",
    "seed_shipments",
    "seed_alerts",
]

class Command(BaseCommand):
    help = "Run all seed commands."

    def handle(self, *args, **options):
        for cmd in SEED_COMMANDS:
            self.stdout.write(f"Seeding: {cmd}")
            try:
                call_command(cmd)
            except Exception as e:
                self.stderr.write(f"Skip {cmd}: {e}")
        self.stdout.write(self.style.SUCCESS("All seeds done."))
