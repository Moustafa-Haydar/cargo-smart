import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:logger/logger.dart';
import 'package:cargo_smart_app/Services/network_service.dart';

abstract class BaseController extends GetxController {
  final Logger _logger = Logger();
  final NetworkService _networkService = Get.find<NetworkService>();
  
  // Common observable variables
  final RxBool isLoading = false.obs;
  final RxString errorMessage = ''.obs;
  final RxBool hasError = false.obs;

  @override
  void onInit() {
    super.onInit();
    _setupErrorHandling();
  }

  void _setupErrorHandling() {
    // Don't automatically show network error snackbars
    // Let individual API calls handle their own error messages
  }

  // Common error handling methods
  void handleError(dynamic error, {String? customMessage}) {
    _logger.e('Error occurred: $error');
    
    hasError.value = true;
    errorMessage.value = customMessage ?? _getErrorMessage(error);
    
    // Show error snackbar
    Get.snackbar(
      'Error',
      errorMessage.value,
      snackPosition: SnackPosition.BOTTOM,
      backgroundColor: Colors.red,
      colorText: Colors.white,
      duration: const Duration(seconds: 3),
      icon: const Icon(Icons.error, color: Colors.white),
    );
  }

  String _getErrorMessage(dynamic error) {
    if (error.toString().contains('SocketException')) {
      return 'Unable to connect to server. Please check your internet connection.';
    } else if (error.toString().contains('TimeoutException')) {
      return 'Request timeout. Please try again.';
    } else if (error.toString().contains('FormatException')) {
      return 'Invalid data format received.';
    } else if (error.toString().contains('Unauthorized')) {
      return 'Session expired. Please login again.';
    } else if (error.toString().contains('Connection refused')) {
      return 'Server is not responding. Please try again later.';
    } else {
      return 'An unexpected error occurred. Please try again.';
    }
  }

  void clearError() {
    hasError.value = false;
    errorMessage.value = '';
  }

  void setLoading(bool loading) {
    isLoading.value = loading;
  }

  // Common API call wrapper
  Future<T?> executeApiCall<T>(
    Future<T> Function() apiCall, {
    String? loadingMessage,
    bool showLoading = true,
    bool showError = true,
  }) async {
    try {
      if (showLoading) {
        setLoading(true);
      }
      
      clearError();
      
      // Don't pre-check connectivity - let the API call handle it
      final result = await apiCall();
      
      if (showLoading) {
        setLoading(false);
      }
      
      return result;
    } catch (error) {
      if (showLoading) {
        setLoading(false);
      }
      
      if (showError) {
        handleError(error);
      }
      
      return null;
    }
  }

  // Show success message
  void showSuccessMessage(String message) {
    Get.snackbar(
      'Success',
      message,
      snackPosition: SnackPosition.BOTTOM,
      backgroundColor: Colors.green,
      colorText: Colors.white,
      duration: const Duration(seconds: 2),
      icon: const Icon(Icons.check_circle, color: Colors.white),
    );
  }

  // Show info message
  void showInfoMessage(String message) {
    Get.snackbar(
      'Info',
      message,
      snackPosition: SnackPosition.BOTTOM,
      backgroundColor: Colors.blue,
      colorText: Colors.white,
      duration: const Duration(seconds: 2),
      icon: const Icon(Icons.info, color: Colors.white),
    );
  }

  // Show warning message
  void showWarningMessage(String message) {
    Get.snackbar(
      'Warning',
      message,
      snackPosition: SnackPosition.BOTTOM,
      backgroundColor: Colors.orange,
      colorText: Colors.white,
      duration: const Duration(seconds: 2),
      icon: const Icon(Icons.warning, color: Colors.white),
    );
  }
}
