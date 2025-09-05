# # apps/geo/management/commands/seed_demo.py
# import json
# import random
# import uuid
# from datetime import timedelta

# from django.core.management.base import BaseCommand, CommandError
# from django.utils import timezone as tz

# # Import your models (string FKs are fine in models, but for seeding we import normally)
# from apps.geo.models import Location, Facility
# from apps.routes.models import Route, RouteSegment
# from apps.vehicles.models import Vehicle, VehicleIdentifier, VehiclePosition, PortCall
# from apps.shipments.models import Shipment, ShipmentMilestone, ShipmentVehicle, ShipmentContainer
# from apps.containers.models import Container, ContainerEvent
# from apps.alerts.models import Alert


# class Command(BaseCommand):
#     help = "Seed demo data for geo, routes, vehicles, shipments, containers, alerts (10 per model). Use --fresh to clear first."

#     def add_arguments(self, parser):
#         parser.add_argument(
#             "--fresh",
#             action="store_true",
#             help="Delete existing data for these apps before seeding."
#         )

#     # ---------- helpers ----------

#     def _geojson_line(self, coords):
#         # coords = [(lng, lat), ...]
#         return json.dumps({"type": "LineString", "coordinates": coords})

#     def _now(self, plus_hours=0):
#         return tz.now() + timedelta(hours=plus_hours)

#     # ---------- clearing in FK-safe order ----------
#     def _clear_all(self):
#         # Delete leaf nodes first (has FKs to others)
#         Alert.objects.all().delete()
#         ShipmentContainer.objects.all().delete()
#         ShipmentVehicle.objects.all().delete()
#         ShipmentMilestone.objects.all().delete()
#         Shipment.objects.all().delete()

#         ContainerEvent.objects.all().delete()
#         Container.objects.all().delete()

#         PortCall.objects.all().delete()
#         VehiclePosition.objects.all().delete()
#         VehicleIdentifier.objects.all().delete()
#         Vehicle.objects.all().delete()

#         RouteSegment.objects.all().delete()
#         Route.objects.all().delete()

#         Facility.objects.all().delete()
#         Location.objects.all().delete()

#     # ---------- seeding ----------
#     def handle(self, *args, **opts):
#         if opts["fresh"]:
#             self.stdout.write(self.style.WARNING("Clearing existing demo data…"))
#             self._clear_all()

#         random.seed(42)

#         # ===== GEO =====
#         self.stdout.write("Seeding geo…")
#         loc_specs = [
#             # name, state, country, country_code, locode, lat, lng, tz
#             ("Houston", "Texas", "United States", "US", "USHOU", 29.76328, -95.36327, "America/Chicago"),
#             ("Bremerhaven", "Bremen", "Germany", "DE", "DEBRV", 53.53615, 8.59298, "Europe/Berlin"),
#             ("Rotterdam", "", "Netherlands", "NL", "NLRTM", 51.9244, 4.4777, "Europe/Amsterdam"),
#             ("Antwerp", "", "Belgium", "BE", "BEANR", 51.2194, 4.4025, "Europe/Brussels"),
#             ("New York", "NY", "United States", "US", "USNYC", 40.7128, -74.0060, "America/New_York"),
#             ("Los Angeles", "CA", "United States", "US", "USLAX", 34.0522, -118.2437, "America/Los_Angeles"),
#             ("Singapore", "", "Singapore", "SG", "SGSIN", 1.3521, 103.8198, "Asia/Singapore"),
#             ("Shanghai", "", "China", "CN", "CNSHA", 31.2304, 121.4737, "Asia/Shanghai"),
#             ("Dubai", "", "UAE", "AE", "AEDXB", 25.2048, 55.2708, "Asia/Dubai"),
#             ("Santos", "", "Brazil", "BR", "BRSSZ", -23.9608, -46.3336, "America/Sao_Paulo"),
#         ]
#         locations = []
#         for name, state, country, cc, lc, lat, lng, z in loc_specs:
#             loc, _ = Location.objects.get_or_create(
#                 name=name, country_code=cc,
#                 defaults=dict(state=state, country=country, locode=lc, lat=lat, lng=lng, timezone=z)
#             )
#             locations.append(loc)

#         # Facilities (10)
#         fac_specs = [
#             ("Houston Barbours Cut Terminal", "US", "USUQF", "USUQFGDQQ", None, "Houston"),
#             ("MSC Gate Bremerhaven Gmbh & Co. KG", "DE", None, None, None, "Bremerhaven"),
#             ("Port of Rotterdam Terminal A", "NL", "NLRTM-A", "NLRTMAAAAA", Non
