from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from apps.accounts.authentication import BearerTokenAuthentication
from rest_framework.response import Response
from rest_framework import status, serializers
from django.db.models import Prefetch
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .web_views import _serialize_shipment
from ..models import Shipment, ShipmentMilestone


# Serializers for shipments
class ShipmentStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=['PENDING', 'IN_TRANSIT', 'DELIVERED', 'CANCELLED'],
        help_text="New status for the shipment"
    )

@swagger_auto_schema(
    method='get',
    operation_description="Get all shipments assigned to the authenticated driver",
    responses={
        200: openapi.Response(
            description="List of shipments retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'shipments': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT)
                    )
                }
            )
        ),
        401: openapi.Response(
            description="Authentication required",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['Mobile Shipments'],
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def driver_shipments(request):
    """
    Get all shipments assigned to the authenticated driver
    """
    # Get all shipments (since there's no driver field in the current model)
    shipments = (
        Shipment.objects
        .select_related(
            "origin",
            "destination", 
            "current_location",
            "route",
            "vehicle"
        )
        .prefetch_related(
            Prefetch(
                "milestones",
                queryset=ShipmentMilestone.objects.select_related("location")
            )
        )
        .order_by('-scheduled_at')
    )
    
    return Response({
        'shipments': [_serialize_shipment(shipment) for shipment in shipments]
    })


@swagger_auto_schema(
    method='get',
    operation_description="Get detailed information about a specific shipment",
    manual_parameters=[
        openapi.Parameter(
            'shipment_id',
            openapi.IN_PATH,
            description="UUID of the shipment",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_UUID
        )
    ],
    responses={
        200: openapi.Response(
            description="Shipment details retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'shipment': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        404: openapi.Response(
            description="Shipment not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(
            description="Authentication required",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['Mobile Shipments'],
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def driver_shipment_detail(request, shipment_id):
    """
    Get details of a specific shipment
    """
    try:
        shipment = get_object_or_404(
            Shipment.objects
            .select_related(
                "origin",
                "destination",
                "current_location", 
                "route",
                "vehicle"
            )
            .prefetch_related(
                Prefetch(
                    "milestones",
                    queryset=ShipmentMilestone.objects.select_related("location")
                )
            ),
            id=shipment_id
        )
        
        return Response({
            'shipment': _serialize_shipment(shipment)
        })
        
    except Exception as e:
        return Response({
            'error': 'Shipment not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='post',
    operation_description="Mark a shipment as delivered",
    manual_parameters=[
        openapi.Parameter(
            'shipment_id',
            openapi.IN_PATH,
            description="UUID of the shipment to mark as delivered",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_UUID
        )
    ],
    responses={
        200: openapi.Response(
            description="Shipment marked as delivered successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'shipment': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        400: openapi.Response(
            description="Bad request - shipment already delivered",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        404: openapi.Response(
            description="Shipment not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(
            description="Authentication required",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['Mobile Shipments'],
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_shipment_delivered(request, shipment_id):
    """
    Mark a shipment as delivered
    """
    try:
        shipment = get_object_or_404(
            Shipment,
            id=shipment_id
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


@swagger_auto_schema(
    method='post',
    operation_description="Update shipment status (for status changes like IN_TRANSIT, CANCELLED, etc.)",
    manual_parameters=[
        openapi.Parameter(
            'shipment_id',
            openapi.IN_PATH,
            description="UUID of the shipment to update",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_UUID
        )
    ],
    request_body=ShipmentStatusUpdateSerializer,
    responses={
        200: openapi.Response(
            description="Shipment status updated successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'shipment': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        400: openapi.Response(
            description="Bad request - missing status or invalid status",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        404: openapi.Response(
            description="Shipment not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        401: openapi.Response(
            description="Authentication required",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    tags=['Mobile Shipments'],
    security=[{'Bearer': []}]
)
@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def update_shipment_status(request, shipment_id):
    """
    Update shipment status (for other status changes besides delivered)
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
            id=shipment_id
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
