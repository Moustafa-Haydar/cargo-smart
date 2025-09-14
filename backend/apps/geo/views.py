from .models import Location
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def locations(request):
    locations_qs = Location.objects.all().values(
        "id", "name", "state", "country", "country_code",
        "lat", "lng", "timezone"
    )
    return JsonResponse({"locations": list(locations_qs)}, safe=False)
