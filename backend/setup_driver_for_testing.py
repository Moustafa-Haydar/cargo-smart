#!/usr/bin/env python
"""
Setup script for testing OneSignal notifications
This script creates a test driver with external_id and assigns them to a vehicle and shipment
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
from apps.geo.models import Location
from apps.rbac.models import Group, UserGroup

User = get_user_model()

def setup_test_driver():
    print("🚀 Setting up test driver for OneSignal notifications...")
    print("=" * 60)
    
    # Step 1: Create or get test driver
    print("1️⃣ Creating test driver...")
    driver, created = User.objects.get_or_create(
        username='test_driver',
        defaults={
            'email': 'test_driver@example.com',
            'first_name': 'Test',
            'last_name': 'Driver',
            'external_id': 'driver_123',  # OneSignal external ID
        }
    )
    
    if created:
        driver.set_password('password123')
        driver.save()
        print(f"   ✅ Created test driver: {driver.username}")
    else:
        # Update existing driver with external_id
        driver.external_id = 'driver_123'
        driver.save()
        print(f"   ✅ Updated test driver: {driver.username}")
    
    print(f"   Driver ID: {driver.id}")
    print(f"   Driver External ID: {driver.external_id}")
    
    # Step 2: Add driver to Driver group
    print("\n2️⃣ Adding driver to Driver group...")
    driver_group, _ = Group.objects.get_or_create(name='Driver')
    UserGroup.objects.get_or_create(user=driver, group=driver_group)
    print(f"   ✅ Added {driver.username} to Driver group")
    
    # Step 3: Create test locations
    print("\n3️⃣ Creating test locations...")
    origin, _ = Location.objects.get_or_create(
        name='Test Origin Warehouse',
        defaults={'lat': 40.7128, 'lng': -74.0060}
    )
    
    destination, _ = Location.objects.get_or_create(
        name='Test Destination Store',
        defaults={'lat': 40.7589, 'lng': -73.9851}
    )
    
    print(f"   ✅ Origin: {origin.name}")
    print(f"   ✅ Destination: {destination.name}")
    
    # Step 4: Create test vehicle
    print("\n4️⃣ Creating test vehicle...")
    vehicle, created = Vehicle.objects.get_or_create(
        plate_number='TEST-001',
        defaults={
            'model': 'Test Delivery Truck',
            'status': 'ACTIVE',
            'driver': driver,  # Assign driver to vehicle
        }
    )
    
    if created:
        print(f"   ✅ Created test vehicle: {vehicle.plate_number}")
    else:
        # Update existing vehicle with driver
        vehicle.driver = driver
        vehicle.save()
        print(f"   ✅ Updated test vehicle: {vehicle.plate_number}")
    
    print(f"   Vehicle ID: {vehicle.id}")
    print(f"   Assigned Driver: {vehicle.driver.username}")
    
    # Step 5: Create test shipment
    print("\n5️⃣ Creating test shipment...")
    shipment, created = Shipment.objects.get_or_create(
        ref_no='TEST-SHIPMENT-001',
        defaults={
            'status': 'PLANNED',
            'carrier_name': 'Test Carrier Co.',
            'origin': origin,
            'destination': destination,
            'vehicle': vehicle,  # Assign vehicle to shipment
            'scheduled_at': '2025-01-20 10:00:00',
        }
    )
    
    if created:
        print(f"   ✅ Created test shipment: {shipment.ref_no}")
    else:
        # Update existing shipment with vehicle
        shipment.vehicle = vehicle
        shipment.save()
        print(f"   ✅ Updated test shipment: {shipment.ref_no}")
    
    print(f"   Shipment ID: {shipment.id}")
    print(f"   Assigned Vehicle: {shipment.vehicle.plate_number}")
    
    # Step 6: Summary
    print("\n" + "=" * 60)
    print("🎉 TEST SETUP COMPLETE!")
    print("=" * 60)
    print(f"Driver: {driver.username}")
    print(f"  - ID: {driver.id}")
    print(f"  - External ID: {driver.external_id}")
    print(f"  - Email: {driver.email}")
    print(f"  - Password: password123")
    print()
    print(f"Vehicle: {vehicle.plate_number}")
    print(f"  - ID: {vehicle.id}")
    print(f"  - Model: {vehicle.model}")
    print(f"  - Driver: {vehicle.driver.username}")
    print()
    print(f"Shipment: {shipment.ref_no}")
    print(f"  - ID: {shipment.id}")
    print(f"  - Status: {shipment.status}")
    print(f"  - Vehicle: {shipment.vehicle.plate_number}")
    print()
    print("🔔 Ready to test OneSignal notifications!")
    print("   Use shipment ID:", shipment.id)
    print("   Driver external_id:", driver.external_id)
    
    return {
        'driver': driver,
        'vehicle': vehicle,
        'shipment': shipment
    }

def test_notification_setup():
    """Test the notification setup by checking relationships"""
    print("\n🧪 Testing notification setup...")
    
    try:
        shipment = Shipment.objects.get(ref_no='TEST-SHIPMENT-001')
        
        print(f"✅ Found shipment: {shipment.ref_no}")
        
        if shipment.vehicle:
            print(f"✅ Shipment has vehicle: {shipment.vehicle.plate_number}")
            
            if shipment.vehicle.driver:
                print(f"✅ Vehicle has driver: {shipment.vehicle.driver.username}")
                print(f"✅ Driver has external_id: {shipment.vehicle.driver.external_id}")
                
                if shipment.vehicle.driver.external_id:
                    print("🎉 Perfect! Ready for OneSignal notifications!")
                    return True
                else:
                    print("❌ Driver missing external_id")
                    return False
            else:
                print("❌ Vehicle has no driver assigned")
                return False
        else:
            print("❌ Shipment has no vehicle assigned")
            return False
            
    except Shipment.DoesNotExist:
        print("❌ Test shipment not found")
        return False

if __name__ == "__main__":
    print("🚛 CargoSmart OneSignal Test Setup")
    print("=" * 60)
    
    # Setup test data
    test_data = setup_test_driver()
    
    # Test the setup
    if test_notification_setup():
        print("\n✅ Setup verification successful!")
        print("\n📱 Next steps:")
        print("1. Make sure your Django server is running")
        print("2. Test the route proposal endpoint:")
        print(f"   POST /agent_reroute/shipments/{test_data['shipment'].id}/apply/")
        print("3. Check OneSignal dashboard for notification delivery")
        print("4. Check your mobile app for the notification")
    else:
        print("\n❌ Setup verification failed!")
        print("Please check the error messages above.")
