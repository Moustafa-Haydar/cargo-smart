import 'package:flutter/material.dart';
import 'package:onesignal_flutter/onesignal_flutter.dart';
import 'package:get/get.dart';
import 'package:logger/logger.dart';

class NotificationService {
  static final Logger _logger = Logger();
  static bool _initialized = false;

  static Future<void> initialize() async {
    if (_initialized) return;

    try {
      // Initialize OneSignal
      OneSignal.Debug.setLogLevel(OSLogLevel.verbose);
      OneSignal.initialize("d39a17d5-d9d9-464f-b0e8-514c947cca33");
      
      // Request permission
      OneSignal.Notifications.requestPermission(true);
      
      // Set up notification handlers
      _setupNotificationHandlers();
      
      _initialized = true;
      _logger.i('NotificationService initialized successfully');
    } catch (e) {
      _logger.e('Failed to initialize NotificationService: $e');
    }
  }

  static void _setupNotificationHandlers() {
    // Handle notification received while app is in foreground
    OneSignal.Notifications.addForegroundWillDisplayListener((event) {
      _logger.i('Notification received in foreground: ${event.notification.title}');
      
      // Show a snackbar or custom notification UI
      Get.snackbar(
        event.notification.title ?? 'Notification',
        event.notification.body ?? '',
        snackPosition: SnackPosition.TOP,
        duration: const Duration(seconds: 4),
        backgroundColor: const Color(0xFF2196F3),
        colorText: Colors.white,
        icon: const Icon(Icons.notifications, color: Colors.white),
      );
    });

    // Handle notification clicked
    OneSignal.Notifications.addClickListener((event) {
      _logger.i('Notification clicked: ${event.notification.title}');
      
      // Handle navigation based on notification data
      _handleNotificationClick(event.notification);
    });

    // Handle permission changes
    OneSignal.Notifications.addPermissionObserver((state) {
      _logger.i('Notification permission changed: $state');
    });
  }

  static void _handleNotificationClick(OSNotification notification) {
    try {
      final additionalData = notification.additionalData;
      
      if (additionalData != null) {
        final type = additionalData['type'] as String?;
        final shipmentId = additionalData['shipment_id'] as String?;
        
        switch (type) {
          case 'shipment_update':
            if (shipmentId != null) {
              // Navigate to shipment detail
              Get.toNamed('/shipment-detail', arguments: {'shipmentId': shipmentId});
            }
            break;
          case 'new_shipment':
            // Navigate to shipments screen
            Get.toNamed('/shipments');
            break;
          default:
            // Navigate to home
            Get.toNamed('/home');
        }
      }
    } catch (e) {
      _logger.e('Error handling notification click: $e');
    }
  }

  // Send a test notification (for development)
  static Future<void> sendTestNotification() async {
    try {
      // This would typically be done from your backend
      // For testing purposes, you can use OneSignal's REST API
      _logger.i('Test notification sent');
    } catch (e) {
      _logger.e('Failed to send test notification: $e');
    }
  }

  // Get the current user's OneSignal player ID
  static Future<String?> getPlayerId() async {
    try {
      final deviceState = await OneSignal.User.getOnesignalId();
      return deviceState;
    } catch (e) {
      _logger.e('Failed to get player ID: $e');
      return null;
    }
  }

  // Set user tags for targeted notifications
  static Future<void> setUserTags(Map<String, String> tags) async {
    try {
      OneSignal.User.addTags(tags);
      _logger.i('User tags set: $tags');
    } catch (e) {
      _logger.e('Failed to set user tags: $e');
    }
  }

  // Clear user tags
  static Future<void> clearUserTags() async {
    try {
      OneSignal.User.removeTags([]);
      _logger.i('User tags cleared');
    } catch (e) {
      _logger.e('Failed to clear user tags: $e');
    }
  }
}
