import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class PostmanTest {
  static Future<void> testLoginRequest() async {
    try {
      final client = HttpClient();
      client.connectionTimeout = const Duration(seconds: 10);

      try {
        // Test the exact same request as Postman
        final uri = Uri.parse('http://10.0.2.2:8000/accounts/mobile/login/');
        final request = await client.postUrl(uri);

        // Set headers exactly like Postman
        // request.headers.set('Content-Type', 'application/json');
        request.headers.set(
          'X-CSRFToken',
          'IwdTKQHOvXKP46q05bF14hUs8u1QaWrTWge1ZvQqxCXc5wdCoyRTVopVWlZpWz9t',
        );

        // Test data (you can change these)
        final testData = '{"username": "test", "password": "test"}';
        request.write(testData);

        print('🔍 Testing login request:');
        print('URL: $uri');
        print('Headers: ${request.headers}');
        print('Data: $testData');

        final response = await request.close();
        final responseBody = await response.transform(utf8.decoder).join();

        Get.dialog(
          AlertDialog(
            title: const Text('Postman-Style Test Result'),
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Status Code: ${response.statusCode}'),
                  Text('Reason Phrase: ${response.reasonPhrase}'),
                  const SizedBox(height: 8),
                  const Text(
                    'Response Body:',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text(responseBody),
                  const SizedBox(height: 8),
                  Text(
                    response.statusCode == 200
                        ? '✅ Request successful!'
                        : '❌ Request failed',
                    style: TextStyle(
                      color:
                          response.statusCode == 200
                              ? Colors.green
                              : Colors.red,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            actions: [
              TextButton(onPressed: () => Get.back(), child: const Text('OK')),
            ],
          ),
        );

        print('✅ Response received:');
        print('Status: ${response.statusCode}');
        print('Body: $responseBody');
      } catch (e) {
        print('❌ Request failed: $e');
        Get.dialog(
          AlertDialog(
            title: const Text('Postman-Style Test Failed'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Error: $e'),
                const SizedBox(height: 8),
                const Text(
                  '❌ Request failed',
                  style: TextStyle(
                    color: Colors.red,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            actions: [
              TextButton(onPressed: () => Get.back(), child: const Text('OK')),
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
          content: Text('Failed to test: $e'),
          actions: [
            TextButton(onPressed: () => Get.back(), child: const Text('OK')),
          ],
        ),
      );
    }
  }
}
