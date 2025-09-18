import 'package:get/get.dart';
import 'package:cargo_smart_app/Services/notification_service.dart';
import 'package:logger/logger.dart';

class NotificationController extends GetxController {
  final Logger _logger = Logger();
  
  // Observable variables
  final RxBool isLoading = false.obs;
  final RxList<Map<String, dynamic>> notifications = <Map<String, dynamic>>[].obs;
  final RxInt unreadCount = 0.obs;
  final RxString errorMessage = ''.obs;

  @override
  void onInit() {
    super.onInit();
    _initializeNotifications();
  }

  Future<void> _initializeNotifications() async {
    try {
      await NotificationService.initialize();
      await _loadNotifications();
    } catch (e) {
      _logger.e('Failed to initialize notifications: $e');
      errorMessage.value = 'Failed to initialize notifications';
    }
  }

  Future<void> _loadNotifications() async {
    // In a real app, you would fetch notifications from your backend
    // For now, we'll use mock data
    notifications.value = [
      {
        'id': '1',
        'title': 'New Shipment Assigned',
        'body': 'You have been assigned a new shipment #SH001',
        'timestamp': DateTime.now().subtract(const Duration(hours: 2)),
        'read': false,
        'type': 'shipment_assigned',
        'data': {'shipment_id': 'shipment_1'},
      },
      {
        'id': '2',
        'title': 'Shipment Status Update',
        'body': 'Shipment #SH002 has been marked as delivered',
        'timestamp': DateTime.now().subtract(const Duration(hours: 5)),
        'read': true,
        'type': 'shipment_update',
        'data': {'shipment_id': 'shipment_2'},
      },
      {
        'id': '3',
        'title': 'Route Optimization',
        'body': 'Your route has been optimized for better efficiency',
        'timestamp': DateTime.now().subtract(const Duration(days: 1)),
        'read': true,
        'type': 'route_update',
        'data': {},
      },
    ];
    
    _updateUnreadCount();
  }

  void _updateUnreadCount() {
    unreadCount.value = notifications.where((notification) => !notification['read']).length;
  }

  // Mark notification as read
  Future<void> markAsRead(String notificationId) async {
    try {
      final index = notifications.indexWhere((n) => n['id'] == notificationId);
      if (index != -1) {
        notifications[index]['read'] = true;
        _updateUnreadCount();
      }
    } catch (e) {
      _logger.e('Failed to mark notification as read: $e');
    }
  }

  // Mark all notifications as read
  Future<void> markAllAsRead() async {
    try {
      for (var notification in notifications) {
        notification['read'] = true;
      }
      _updateUnreadCount();
    } catch (e) {
      _logger.e('Failed to mark all notifications as read: $e');
    }
  }

  // Delete notification
  Future<void> deleteNotification(String notificationId) async {
    try {
      notifications.removeWhere((n) => n['id'] == notificationId);
      _updateUnreadCount();
    } catch (e) {
      _logger.e('Failed to delete notification: $e');
    }
  }

  // Clear all notifications
  Future<void> clearAllNotifications() async {
    try {
      notifications.clear();
      unreadCount.value = 0;
    } catch (e) {
      _logger.e('Failed to clear all notifications: $e');
    }
  }

  // Refresh notifications
  Future<void> refreshNotifications() async {
    isLoading.value = true;
    try {
      await _loadNotifications();
      errorMessage.value = '';
    } catch (e) {
      errorMessage.value = 'Failed to refresh notifications';
      _logger.e('Failed to refresh notifications: $e');
    } finally {
      isLoading.value = false;
    }
  }

  // Get notifications by type
  List<Map<String, dynamic>> getNotificationsByType(String type) {
    return notifications.where((n) => n['type'] == type).toList();
  }

  // Get unread notifications
  List<Map<String, dynamic>> get unreadNotifications {
    return notifications.where((n) => !n['read']).toList();
  }

  // Handle notification tap
  void handleNotificationTap(Map<String, dynamic> notification) {
    markAsRead(notification['id']);
    
    final type = notification['type'];
    final data = notification['data'] as Map<String, dynamic>?;
    
    switch (type) {
      case 'shipment_assigned':
      case 'shipment_update':
        if (data?['shipment_id'] != null) {
          // Navigate to shipment detail
          Get.toNamed('/shipment-detail', arguments: {'shipmentId': data!['shipment_id']});
        }
        break;
      case 'route_update':
        // Navigate to shipments screen
        Get.toNamed('/shipments');
        break;
      default:
        // Navigate to home
        Get.toNamed('/home');
    }
  }

  // Clear error message
  void clearError() {
    errorMessage.value = '';
  }
}
