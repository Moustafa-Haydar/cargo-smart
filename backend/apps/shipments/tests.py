from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.shipments.models import Shipment, ShipmentMilestone
from apps.geo.models import Location
from apps.routes.models import Route
from apps.vehicles.models import Vehicle
from datetime import datetime, timezone
import json


class ShipmentViewsTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create test locations
        self.origin = Location.objects.create(
            name="Test Origin",
            lat=40.7128,
            lng=-74.0060
        )
        self.destination = Location.objects.create(
            name="Test Destination", 
            lat=34.0522,
            lng=-118.2437
        )
        
        # Create test route (Route model only requires name + geometry)
        self.route = Route.objects.create(
            name="Test Route",
            geometry="[ [77.5946,12.9716], [72.8777,19.0760] ]"
        )
        
        # Create test vehicle
        self.vehicle = Vehicle.objects.create(
            plate_number="TEST-001",
            model="Test Truck",
            status="ACTIVE"
        )
        
        # Create test shipment
        self.shipment = Shipment.objects.create(
            ref_no="TEST001",
            status="PLANNED",
            carrier_name="Test Carrier",
            origin=self.origin,
            destination=self.destination,
            route=self.route,
            vehicle=self.vehicle,
            scheduled_at=datetime.now(timezone.utc)
        )
        
        # Create test milestone
        self.milestone = ShipmentMilestone.objects.create(
            shipment=self.shipment,
            kind="LOADED",
            location=self.origin,
            date=datetime.now(timezone.utc),
            actual=True
        )
        
        self.client = Client()

    def test_shipments_list_view(self):
        """Test the shipments list view"""
        response = self.client.get('/shipments/shipments/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('shipments', data)
        self.assertEqual(len(data['shipments']), 1)
        
        shipment_data = data['shipments'][0]
        self.assertEqual(shipment_data['ref_no'], 'TEST001')
        self.assertEqual(shipment_data['status'], 'PLANNED')
        self.assertEqual(shipment_data['carrier_name'], 'Test Carrier')
        self.assertIsNotNone(shipment_data['origin'])
        self.assertIsNotNone(shipment_data['destination'])
        self.assertIsNotNone(shipment_data['route'])
        self.assertIsNotNone(shipment_data['vehicle'])
        self.assertEqual(shipment_data['vehicle']['plate_number'], 'TEST-001')
        self.assertEqual(shipment_data['vehicle']['model'], 'Test Truck')
        self.assertEqual(shipment_data['vehicle']['status'], 'ACTIVE')
        self.assertEqual(len(shipment_data['milestones']), 1)

    def test_shipment_detail_view(self):
        """Test the shipment detail view"""
        response = self.client.get(f'/shipments/shipment/{self.shipment.id}/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('shipments', data)
        self.assertEqual(len(data['shipments']), 1)
        
        shipment_data = data['shipments'][0]
        self.assertEqual(shipment_data['id'], str(self.shipment.id))
        self.assertEqual(shipment_data['ref_no'], 'TEST001')

    def test_shipment_not_found(self):
        """Test shipment not found case"""
        import uuid
        fake_id = uuid.uuid4()
        response = self.client.get(f'/shipments/shipment/{fake_id}/')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.content)
        self.assertIn('detail', data)
        self.assertEqual(data['detail'], 'Shipment not found')
