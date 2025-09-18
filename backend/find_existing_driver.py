#!/usr/bin/env python
"""
Find existing driver with external_id and test OneSignal notification
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cargosmart.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.vehicles.models import Vehicle
from apps.shipments.models import Shipment
from apps.agent_reroute.onesignal_service import OneSignalService

User = get_user_model()

def find_drivers_with_external_id():
    """Find all users with external_id"""
    print("🔍 Finding users with external_id...")
    print("=" * 50)
    
    users_with_external_id = User.objects.filter(external_id__isnull=False).exclude(external_id='')
    
    if not users_with_external_id.exists():
        print("❌ No users found with external_id")
        return []
    
    print(f"✅ Found {users_with_external_id.count()} user(s) with external_id:")
    print()
    
    for user in users_with_external_id:
        print(f"👤 User: {user.username}")
        print(f"   ID: {user.id}")
        print(f"   External ID: {user.external_id}")
        print(f"   Name: {user.first_name} {user.last_name}")
        print(f"   Email: {user.email}")
        
        # Check if user has assigned vehicles
        vehicles = Vehicle.objects.filter(driver=user)
        if vehicles.exists():
            print(f"   🚛 Assigned Vehicles: {vehicles.count()}")
            for vehicle in vehicles:
                print(f"      - {vehicle.plate_number} ({vehicle.id})")
        else:
            print(f"   🚛 No vehicles assigned")
        
        # Check if user has shipments
        shipments = Shipment.objects.filter(vehicle__driver=user)
        if shipments.exists():
            print(f"   📦 Shipments: {shipments.count()}")
            for shipment in shipments[:3]:  # Show first 3
                print(f"      - {shipment.ref_no} ({shipment.id})")
        else:
            print(f"   📦 No shipments found")
        
        print()
    
    return list(users_with_external_id)

def test_notification_with_existing_driver():
    """Test notification with existing driver"""
    print("🧪 Testing OneSignal notification with existing driver...")
    print("=" * 60)
    
    # Find users with external_id
    users = find_drivers_with_external_id()
    
    if not users:
        print("❌ No users with external_id found. Cannot test notification.")
        return
    
    # Use the first user with external_id
    driver = users[0]
    print(f"🎯 Testing with driver: {driver.username} (external_id: {driver.external_id})")
    
    # Find a shipment for this driver
    shipment = Shipment.objects.filter(vehicle__driver=driver).first()
    
    if not shipment:
        print("❌ No shipments found for this driver. Creating a test shipment...")
        
        # Create a test shipment
        from apps.geo.models import Location
        
        origin, _ = Location.objects.get_or_create(
            name='Test Origin',
            defaults={'lat': 40.7128, 'lng': -74.0060}
        )
        
        destination, _ = Location.objects.get_or_create(
            name='Test Destination',
            defaults={'lat': 40.7589, 'lng': -73.9851}
        )
        
        # Get or create a vehicle for this driver
        vehicle, _ = Vehicle.objects.get_or_create(
            plate_number=f'TEST-{driver.username.upper()}',
            defaults={
                'model': 'Test Vehicle',
                'status': 'ACTIVE',
                'driver': driver,
            }
        )
        
        if not vehicle.driver:
            vehicle.driver = driver
            vehicle.save()
        
        # Create shipment
        shipment, _ = Shipment.objects.get_or_create(
            ref_no=f'TEST-{driver.username.upper()}-001',
            defaults={
                'status': 'PLANNED',
                'carrier_name': 'Test Carrier',
                'origin': origin,
                'destination': destination,
                'vehicle': vehicle,
                'scheduled_at': '2025-01-20 10:00:00',
            }
        )
        
        if not shipment.vehicle:
            shipment.vehicle = vehicle
            shipment.save()
        
        print(f"✅ Created test shipment: {shipment.ref_no}")
    
    print(f"📦 Using shipment: {shipment.ref_no} (ID: {shipment.id})")
    print(f"🚛 Vehicle: {shipment.vehicle.plate_number if shipment.vehicle else 'None'}")
    print(f"👤 Driver: {shipment.vehicle.driver.username if shipment.vehicle and shipment.vehicle.driver else 'None'}")
    
    # Test OneSignal notification
    print("\n🔔 Testing OneSignal notification...")
    onesignal = OneSignalService()
    
    result = onesignal.send_route_update_notification(
        shipment_id=shipment.id,
        route_id="test-route-123",
        external_user_ids=[driver.external_id]
    )
    
    print(f"📱 Notification result:")
    print(f"   Success: {result['success']}")
    
    if result['success']:
        print(f"   ✅ Notification sent successfully!")
        print(f"   OneSignal ID: {result['data'].get('id')}")
        print(f"   Recipients: {result['data'].get('recipients', 'Unknown')}")
    else:
        print(f"   ❌ Notification failed!")
        print(f"   Error: {result['error']}")
    
    return {
        'driver': driver,
        'shipment': shipment,
        'notification_result': result
    }

def test_api_endpoint_with_existing_data():
    """Test the API endpoint with existing data"""
    print("\n🌐 Testing API endpoint with existing data...")
    print("=" * 60)
    
    # Find a shipment with a driver
    shipment = Shipment.objects.filter(
        vehicle__driver__external_id__isnull=False
    ).exclude(vehicle__driver__external_id='').first()
    
    if not shipment:
        print("❌ No shipments found with drivers that have external_id")
        return
    
    print(f"📦 Testing with shipment: {shipment.ref_no} (ID: {shipment.id})")
    print(f"👤 Driver: {shipment.vehicle.driver.username}")
    print(f"🔑 External ID: {shipment.vehicle.driver.external_id}")
    
    # Test API endpoint
    import requests
    import json
    
    url = f"http://localhost:8000/agent_reroute/shipments/{shipment.id}/apply/"
    
    payload = {
        "proposed_route_id": "test-route-456",
        "path": "test-path-data"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": "IwdTKQHOvXKP46q05bF14hUs8u1QaWrTWge1ZvQqxCXc5wdCoyRTVopVWlZpWz9t"
    }
    
    try:
        print(f"🚀 Making API request to: {url}")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📄 Response data:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            data = response.json()
            if data.get('notification_sent'):
                print("✅ API test successful - notification sent!")
            else:
                print("⚠️ API test successful but notification failed")
                print(f"   Error: {data.get('notification_error')}")
        else:
            print("❌ API test failed!")
            
    except Exception as e:
        print(f"❌ API test error: {e}")

if __name__ == "__main__":
    print("🚛 CargoSmart OneSignal Testing with Existing Data")
    print("=" * 70)
    
    # Test 1: Find existing drivers
    test_notification_with_existing_driver()
    
    # Test 2: Test API endpoint
    test_api_endpoint_with_existing_data()
    
    print("\n🎉 Testing complete!")
    print("Check your OneSignal dashboard and mobile app for notifications.")
