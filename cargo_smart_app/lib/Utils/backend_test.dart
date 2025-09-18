import 'dart:io';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:cargo_smart_app/Services/remote/api_urls.dart';

class BackendTest {
  static Future<void> testBackendConnection() async {
    try {
      final client = HttpClient();
      client.connectionTimeout = const Duration(seconds: 5);
      
            try {
              final uri = Uri.parse(ApiUrl.root);
              final request = await client.getUrl(uri);
              final response = await request.close();
        
        Get.dialog(
          AlertDialog(
            title: const Text('Backend Test Result'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                 Text('Status Code: ${response.statusCode}'),
                 Text('Reason Phrase: ${response.reasonPhrase}'),
                const SizedBox(height: 8),
                Text(
                  response.statusCode < 500 
                    ? 'Backend is reachable!'
                    : 'Backend returned error',
                  style: TextStyle(
                    color: response.statusCode < 500 ? Colors.green : Colors.red,
                    fontWeight: FontWeight.bold,
                  ),
                ),
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
      } catch (e) {
        Get.dialog(
          AlertDialog(
            title: const Text('Backend Test Failed'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Error: $e'),
                const SizedBox(height: 8),
                const Text(
                  '❌ Cannot connect to backend',
                  style: TextStyle(
                    color: Colors.red,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                const Text('Possible causes:'),
                const Text('• Django server not running'),
                const Text('• Wrong URL (localhost:8000)'),
                const Text('• Firewall blocking connection'),
                const Text('• Backend crashed'),
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
      } finally {
        client.close();
      }
    } catch (e) {
      Get.dialog(
        AlertDialog(
          title: const Text('Test Error'),
          content: Text('Failed to test backend: $e'),
          actions: [
            TextButton(
              onPressed: () => Get.back(),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    }
  }
}
