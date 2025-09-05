import uuid, random, json
from django.core.management.base import BaseCommand
from apps.geo.models import Location, Facility

class Command(BaseCommand):
    help = "Seed 10 Locations and 10 Facilities. Use --fresh to delete existing first."

    def add_arguments(self, parser):
        parser.add_argument("--fresh", action="store_true")

    def handle(self, *args, **opts):
        if opts["fresh"]:
            Facility.objects.all().delete()
            Location.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared geo data"))

        random.seed(42)

        loc_specs = [
            ("Houston","Texas","United States","US","USHOU",29.76328,-95.36327,"America/Chicago"),
            ("Bremerhaven","Bremen","Germany","DE","DEBRV",53.53615,8.59298,"Europe/Berlin"),
            ("Rotterdam","", "Netherlands","NL","NLRTM",51.9244,4.4777,"Europe/Amsterdam"),
            ("Antwerp","", "Belgium","BE","BEANR",51.2194,4.4025,"Europe/Brussels"),
            ("New York","NY","United States","US","USNYC",40.7128,-74.0060,"America/New_York"),
            ("Los Angeles","CA","United States","US","USLAX",34.0522,-118.2437,"America/Los_Angeles"),
            ("Singapore","", "Singapore","SG","SGSIN",1.3521,103.8198,"Asia/Singapore"),
            ("Shanghai","", "China","CN","CNSHA",31.2304,121.4737,"Asia/Shanghai"),
            ("Dubai","", "UAE","AE","AEDXB",25.2048,55.2708,"Asia/Dubai"),
            ("Santos","", "Brazil","BR","BRSSZ",-23.9608,-46.3336,"America/Sao_Paulo"),
        ]
        locations = []
        for name, state, country, cc, lc, lat, lng, tz in loc_specs:
            obj, _ = Location.objects.get_or_create(
                name=name, country_code=cc,
                defaults=dict(state=state, country=country, locode=lc, lat=lat, lng=lng, timezone=tz)
            )
            locations.append(obj)

        by_name = {l.name: l for l in locations}
        fac_specs = [
            ("Houston Barbours Cut Terminal","US","USUQF","USUQFGDQQ",None,"Houston"),
            ("MSC Gate Bremerhaven Gmbh & Co. KG","DE",None,None,None,"Bremerhaven"),
            ("Port of Rotterdam Terminal A","NL","NLRTM-A","NLRTMAAAAA",None,"Rotterdam"),
            ("Antwerp PSA","BE","BEANR-PSA",None,None,"Antwerp"),
            ("NYNJ Port Newark","US","USNWK",None,None,"New York"),
            ("LA Pier 400","US","USLAX-400",None,None,"Los Angeles"),
            ("PSA Singapore","SG","SGSIN-PSA",None,None,"Singapore"),
            ("Yangshan Deep-Water","CN","CNSHA-YS",None,None,"Shanghai"),
            ("Jebel Ali Terminal 2","AE","AEDXB-T2","AEDXBT2XXX",None,"Dubai"),
            ("Santos Tecon","BR","BRSSZ-TC",None,None,"Santos"),
        ]
        for name, cc, lc, bic, smdg, loc_name in fac_specs:
            Facility.objects.get_or_create(
                name=name,
                defaults=dict(country_code=cc, locode=lc or "", bic_code=bic, smdg_code=smdg, location=by_name[loc_name])
            )

        self.stdout.write(self.style.SUCCESS("Seeded geo (10 Locations, 10 Facilities)."))
