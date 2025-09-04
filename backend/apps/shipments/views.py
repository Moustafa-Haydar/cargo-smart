import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.db import transaction

@require_GET
@csrf_protect
def groups(request, id=None):

    
    
    if id is not None:
        group = Group.objects.filter(pk=id).first()
        return JsonResponse({"group" : _group_payload(group)})

    gs = Group.objects.all().order_by("name")
    return JsonResponse({"groups": [_group_payload(g) for g in gs]})