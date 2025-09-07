import random
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone as tz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from apps.shipments.models import Shipment, ShipmentMilestone, ShipmentVehicle, ShipmentContainer
from apps.geo.models import Location
from apps.routes.models import Route
from apps.vehicles.models import Vehicle
from apps.containers.models import Container

class Command(BaseCommand):
    help = "Seed 10 Shipments + 10 Milestones + 10 ShipmentVehicles + 10 ShipmentContainers. Requires geo, routes, vehicles, containers."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def handle(self, *args, **opts):
        try:
            if opts["fresh"]:
                ShipmentContainer.objects.all().delete()
                ShipmentVehicle.objects.all().delete()
                ShipmentMilestone.objects.all().delete()
                Shipment.objects.all().delete()
                self.stdout.write(self.style.WARNING("Cleared shipments data"))

            if Location.objects.count() < 2 or Route.objects.count() == 0:
                raise CommandError("Need Locations (>=2) and Routes. Run: seed_geo, seed_routes.")

            # Get available drivers
            User = get_user_model()
            self.stdout.write(f"Available groups: {', '.join([g.name for g in Group.objects.all()])}")
            
            driver_group = Group.objects.get(name="Driver")
            drivers = list(User.objects.filter(groups=driver_group))
            
            self.stdout.write(f"Found {len(drivers)} drivers: {', '.join([d.username for d in drivers])}")
            
            if not drivers:
                raise CommandError("No drivers found in auth group. Run: seed_rbac, seed_accounts first.")

            # Get and print available data
            locs = list(Location.objects.all())
            self.stdout.write(f"Found {len(locs)} locations")
            
            routes = list(Route.objects.all())
            self.stdout.write(f"Found {len(routes)} routes")
            
            vehicles = list(Vehicle.objects.all())
            self.stdout.write(f"Found {len(vehicles)} vehicles")
            
            containers = list(Container.objects.all())
            self.stdout.write(f"Found {len(containers)} containers")

            random.seed(42)
            shipments = []

            # Create shipments with try/except for each one
            for i in range(1, 11):
                try:
                    a, b = random.sample(locs, 2)
                    self.stdout.write(f"Creating shipment {i} with origin: {a.name}, destination: {b.name}")
                    
                    driver = random.choice(drivers)
                    self.stdout.write(f"Selected driver: {driver.username}")
                    
                    route = random.choice(routes)
                    self.stdout.write(f"Selected route: {route.id}")
                    
                    s = Shipment.objects.create(
                        ref_no=f"SHP{i:04d}",
                        shipment_type=random.choice(["CT","BBK","LCL"]),
                        status=random.choice(["IN_TRANSIT","CREATED","DELIVERED"]),
                        carrier_code=random.choice(["MAEU","MSCU","CMA"]),
                        carrier_name=random.choice(["Maersk","MSC","CMA CGM"]),
                        api_updated_at=tz.now() - timedelta(hours=2),
                        origin=a,
                        destination=b,
                        current_location=random.choice([a,b] + locs),
                        route=route,
                        driver=driver,
                        scheduled_at=tz.now() - timedelta(hours=96 - i*8),
                        delivered_at=None if i < 8 else (tz.now() - timedelta(hours=24 - i)),
                    )
                    shipments.append(s)
                    self.stdout.write(f"Created shipment {s.ref_no}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating shipment {i}: {str(e)}"))
                    raise

            # Create milestones
            kinds = ["PREPOL","POL","POD","POSTPOD"]
            for i, s in enumerate(shipments):
                try:
                    milestone = ShipmentMilestone.objects.create(
                        shipment=s,
                        kind=random.choice(kinds),
                        location=random.choice([s.origin, s.destination] + locs),
                        date=tz.now() - timedelta(hours=72 - i*5),
                        actual=(i % 2 == 0),
                        predictive_eta=None if (i % 2 == 0) else tz.now() + timedelta(hours=i*3 + 12),
                    )
                    self.stdout.write(f"Created milestone for shipment {s.ref_no}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating milestone for shipment {s.ref_no}: {str(e)}"))
                    raise

            # Link vehicles
            for i, s in enumerate(shipments):
                try:
                    v = vehicles[i] if i < len(vehicles) else random.choice(vehicles) if vehicles else None
                    if v:
                        ShipmentVehicle.objects.create(
                            shipment=s, vehicle=v, voyage=f"{330+i}E", role=random.choice(["MAIN","FEEDER"])
                        )
                        self.stdout.write(f"Linked vehicle to shipment {s.ref_no}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error linking vehicle to shipment {s.ref_no}: {str(e)}"))
                    raise

            # Link containers
            used_pairs = set()
            for i, s in enumerate(shipments):
                try:
                    if not containers: break
                    c = containers[i] if i < len(containers) else random.choice(containers)
                    if (s.id, c.id) in used_pairs:
                        continue
                    ShipmentContainer.objects.create(
                        shipment=s, container=c,
                        is_active=True,
                        loaded_at=tz.now() - timedelta(hours=48 - i),
                        discharged_at=None if i < 8 else tz.now() - timedelta(hours=12 - i),
                    )
                    used_pairs.add((s.id, c.id))
                    self.stdout.write(f"Linked container to shipment {s.ref_no}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error linking container to shipment {s.ref_no}: {str(e)}"))
                    raise

            self.stdout.write(
                self.style.SUCCESS(
                    f"Seeded {len(shipments)} shipments (+milestones, +links to vehicles/containers)"
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in seed_shipments: {str(e)}"))
            raise