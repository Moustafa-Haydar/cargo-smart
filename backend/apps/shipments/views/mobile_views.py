from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from apps.accounts.authentication import BearerTokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from django.utils import timezone
from .web_views import _serialize_shipment
from ..models import Shipment, ShipmentMilestone


@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def driver_shipments(request):
    """
    Get all shipments assigned to the authenticated driver
    """
    # Get shipments assigned to the current driver
    shipments = (
        Shipment.objects
        .filter(driver=request.user)
        .select_related(
            "origin",
            "destination", 
            "current_location",
            "route",
            "driver"
        )
        .prefetch_related(
            Prefetch(
                "milestones",
                queryset=ShipmentMilestone.objects.select_related("location")
            ),
            Prefetch(
                "shipment_vehicles",
                queryset=ShipmentVehicle.objects.select_related("vehicle")
            ),
            Prefetch(
                "shipment_containers",
                queryset=ShipmentContainer.objects.select_related("container")
            )
        )
        .order_by('-scheduled_at')
    )
    
    return Response({
        'shipments': [_serialize_shipment(shipment) for shipment in shipments]
    })


@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def driver_shipment_detail(request, shipment_id):
    """
    Get details of a specific shipment assigned to the authenticated driver
    """
    try:
        shipment = get_object_or_404(
            Shipment.objects
            .select_related(
                "origin",
                "destination",
                "current_location", 
                "route",
                "driver"
            )
            .prefetch_related(
                Prefetch(
                    "milestones",
                    queryset=ShipmentMilestone.objects.select_related("location")
                ),
                Prefetch(
                    "shipment_vehicles",
                    queryset=ShipmentVehicle.objects.select_related("vehicle")
                ),
                Prefetch(
                    "shipment_containers",
                    queryset=ShipmentContainer.objects.select_related("container")
                )
            ),
            id=shipment_id,
            driver=request.user  # Ensure the shipment belongs to this driver
        )
        
        return Response({
            'shipment': _serialize_shipment(shipment)
        })
        
    except Exception as e:
        return Response({
            'error': 'Shipment not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_shipment_delivered(request, shipment_id):
    """
    Mark a shipment as delivered
    Only the assigned driver can mark their shipments as delivered
    """
    try:
        shipment = get_object_or_404(
            Shipment,
            id=shipment_id,
            driver=request.user  # Ensure the shipment belongs to this driver
        )
        
        # Check if shipment is not already delivered
        if shipment.status == 'DELIVERED':
            return Response({
                'error': 'Shipment is already marked as delivered'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update shipment status and delivery time
        shipment.status = 'DELIVERED'
        shipment.delivered_at = timezone.now()
        shipment.save()
        
        return Response({
            'message': 'Shipment marked as delivered successfully',
            'shipment': _serialize_shipment(shipment)
        })
        
    except Exception as e:
        return Response({
            'error': 'Shipment not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def update_shipment_status(request, shipment_id):
    """
    Update shipment status (for other status changes besides delivered)
    Only the assigned driver can update their shipments
    """
    try:
        data = request.data
        new_status = data.get('status')
        
        if not new_status:
            return Response({
                'error': 'Status is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        shipment = get_object_or_404(
            Shipment,
            id=shipment_id,
            driver=request.user  # Ensure the shipment belongs to this driver
        )
        
        # Update shipment status
        old_status = shipment.status
        shipment.status = new_status
        
        # If marking as delivered, also set delivered_at
        if new_status == 'DELIVERED' and old_status != 'DELIVERED':
            shipment.delivered_at = timezone.now()
        
        shipment.save()
        
        return Response({
            'message': f'Shipment status updated from {old_status} to {new_status}',
            'shipment': _serialize_shipment(shipment)
        })
        
    except Exception as e:
        return Response({
            'error': 'Shipment not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)
