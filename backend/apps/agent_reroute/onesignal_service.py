import requests
import json
import os
from django.conf import settings

class OneSignalService:
    def __init__(self):
        self.app_id = "d39a17d5-d9d9-464f-b0e8-514c947cca33"
        self.api_url = "https://api.onesignal.com/notifications?c=push"
        self.rest_api_key = "MDAzZDhlNTctMDdiYS00N2MwLWFhNjAtMWFmODhjZDQ1NmVk"
    
    def send_notification(self, title, message, external_user_ids=None, data=None):
        """
        Send a push notification via OneSignal API using external user IDs
        
        Args:
            title (str): Notification title
            message (str): Notification message
            external_user_ids (list): List of external user IDs to send to (optional)
            data (dict): Additional data to send with notification (optional)
        
        Returns:
            dict: API response
        """
        print(f"🔔 OneSignal Debug - Title: {title}")
        print(f"🔔 OneSignal Debug - Message: {message}")
        print(f"🔔 OneSignal Debug - External User IDs: {external_user_ids}")
        print(f"🔔 OneSignal Debug - Data: {data}")
        print(f"🔔 OneSignal Debug - API Key exists: {bool(self.rest_api_key)}")
        
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {self.rest_api_key}"
        }
        
        payload = {
            "app_id": self.app_id,
            "contents": {"en": message},
            "headings": {"en": title},
            "target_channel": "push",
        }
        
        # If external user IDs are provided, target them using include_aliases
        if external_user_ids:
            payload["include_aliases"] = {"external_id": external_user_ids}
            print(f"🔔 OneSignal Debug - Targeting specific users: {external_user_ids}")
        else:
            # Default: Send to all users
            payload["included_segments"] = ["All"]
            print(f"🔔 OneSignal Debug - Targeting all users")
        
        # Add custom data if provided
        if data:
            payload["data"] = data
        
        print(f"🔔 OneSignal Debug - Final payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            print(f"🔔 OneSignal Debug - Response status: {response.status_code}")
            print(f"🔔 OneSignal Debug - Response data: {response.text}")
            response.raise_for_status()
            return {
                "success": True,
                "data": response.json()
            }
        except requests.exceptions.RequestException as e:
            print(f"🔔 OneSignal Debug - Error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_route_update_notification(self, shipment_id, route_id, external_user_ids=None):
        """
        Send a notification when a route proposal is applied
        
        Args:
            shipment_id (str): ID of the shipment
            route_id (str): ID of the new route
            external_user_ids (list): List of external user IDs to notify (optional)
        """
        title = "Route Updated"
        message = f"Route proposal has been applied for shipment {str(shipment_id)[:8]}..."
        
        data = {
            "type": "route_update",
            "shipment_id": str(shipment_id),
            "route_id": str(route_id),
            "action": "route_applied"
        }
        
        return self.send_notification(title, message, external_user_ids, data)
