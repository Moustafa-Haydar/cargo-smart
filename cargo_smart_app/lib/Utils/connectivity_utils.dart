import 'dart:io';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:cargo_smart_app/Services/remote/api_urls.dart';

class ConnectivityUtils {
  static Future<bool> hasInternetConnection() async {
    try {
      // Try a simple HTTP request to a reliable endpoint
      final client = HttpClient();
      client.connectionTimeout = const Duration(seconds: 3);

      try {
        final request = await client.getUrl(
          Uri.parse('http://httpbin.org/status/200'),
        );
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
      return false;
    }
  }

  static Future<bool> canReachBackend(String baseUrl) async {
    try {
      final client = HttpClient();
      client.connectionTimeout = const Duration(seconds: 5);

      try {
        final uri = Uri.parse('$baseUrl/');
        final request = await client.getUrl(uri);
        final response = await request.close();
        return response.statusCode <
            500; // Any response < 500 means server is reachable
      } catch (e) {
        return false;
      } finally {
        client.close();
      }
    } catch (e) {
      return false;
    }
  }

  static void showConnectivityDialog() {
    Get.dialog(
      AlertDialog(
        title: const Text('Check Connectivity'),
        content: const Text('Checking your internet connection...'),
        actions: [
          TextButton(
            onPressed: () async {
              Get.back();

              // Show loading dialog
              Get.dialog(
                const AlertDialog(
                  content: Row(
                    children: [
                      CircularProgressIndicator(),
                      SizedBox(width: 16),
                      Text('Checking connectivity...'),
                    ],
                  ),
                ),
                barrierDismissible: false,
              );

              // Perform connectivity checks
              final hasInternet = await hasInternetConnection();
              final backendReachable = await canReachBackend(ApiUrl.baseUrl);

              // Close loading dialog
              Get.back();

              // Show results
              Get.dialog(
                AlertDialog(
                  title: const Text('Connectivity Status'),
                  content: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Internet: ${hasInternet ? "✅ Connected" : "❌ Not Connected"}',
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Backend: ${backendReachable ? "✅ Reachable" : "❌ Not Reachable"}',
                      ),
                      const SizedBox(height: 8),
                      Text('Backend URL: ${ApiUrl.baseUrl}'),
                    ],
                  ),
                  actions: [
                    TextButton(
                      onPressed: () => Get.back(),
                      child: const Text('OK'),
                    ),
                  ],
                ),
              );
            },
            child: const Text('Check'),
          ),
          TextButton(onPressed: () => Get.back(), child: const Text('Cancel')),
        ],
      ),
    );
  }
}
