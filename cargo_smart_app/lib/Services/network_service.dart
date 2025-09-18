import 'dart:io';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:logger/logger.dart';

class NetworkService extends GetxService {
  static final Logger _logger = Logger();
  
  final RxBool isConnected = true.obs;
  final RxString connectionType = 'unknown'.obs;

  @override
  void onInit() {
    super.onInit();
    // Don't check connectivity on init to avoid blocking app startup
    // Connectivity will be checked when actually needed
  }

  Future<void> checkConnectivity() async {
    try {
      // Try a simple HTTP request to a reliable endpoint
      final client = HttpClient();
      client.connectionTimeout = const Duration(seconds: 5);
      
      try {
        final request = await client.getUrl(Uri.parse('http://httpbin.org/status/200'));
        final response = await request.close();
        isConnected.value = response.statusCode == 200;
        _logger.i('Network connectivity check: ${isConnected.value ? "Connected" : "Disconnected"}');
      } catch (e) {
        // If httpbin.org fails, try a simple DNS lookup
        try {
          final result = await InternetAddress.lookup('google.com');
          isConnected.value = result.isNotEmpty && result[0].rawAddress.isNotEmpty;
          _logger.i('Network connectivity check (DNS): ${isConnected.value ? "Connected" : "Disconnected"}');
        } catch (dnsError) {
          isConnected.value = false;
          _logger.w('Network disconnected - both HTTP and DNS failed');
        }
      } finally {
        client.close();
      }
    } catch (e) {
      isConnected.value = false;
      _logger.e('Network check failed: $e');
    }
  }

  Future<bool> hasInternetConnection() async {
    try {
      final client = HttpClient();
      client.connectionTimeout = const Duration(seconds: 3);
      
      try {
        final request = await client.getUrl(Uri.parse('http://httpbin.org/status/200'));
        final response = await request.close();
        return response.statusCode == 200;
      } catch (e) {
        // Fallback to DNS lookup
        try {
          final result = await InternetAddress.lookup('google.com');
          return result.isNotEmpty && result[0].rawAddress.isNotEmpty;
        } catch (dnsError) {
          return false;
        }
      } finally {
        client.close();
      }
    } catch (e) {
      _logger.e('Internet connection check failed: $e');
      return false;
    }
  }

  void showNoInternetSnackbar() {
    Get.snackbar(
      'No Internet Connection',
      'Please check your internet connection and try again.',
      snackPosition: SnackPosition.BOTTOM,
      backgroundColor: Colors.red,
      colorText: Colors.white,
      duration: const Duration(seconds: 3),
      icon: const Icon(Icons.wifi_off, color: Colors.white),
    );
  }
}
