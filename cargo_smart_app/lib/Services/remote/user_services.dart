import 'package:cargo_smart_app/Screens/login_screen.dart';
import 'package:dio/dio.dart';
import 'package:get/get.dart';
import 'package:get/get_core/src/get_main.dart';
import 'package:onesignal_flutter/onesignal_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:cargo_smart_app/Models/user_model.dart';
import 'package:cargo_smart_app/Models/auth_models.dart';
import 'package:cargo_smart_app/Services/remote/api_urls.dart';

class UserServices {
  final Dio _dio = Dio();
  static const String _tokenKey = 'auth_token';
  static const String _userKey = 'user_data';
  
  // Hardcoded CSRF token
  static const String _csrfToken = 'IwdTKQHOvXKP46q05bF14hUs8u1QaWrTWge1ZvQqxCXc5wdCoyRTVopVWlZpWz9t';

  UserServices() {
    _dio.options.baseUrl = ApiUrl.baseUrl;
    _dio.options.connectTimeout = const Duration(seconds: 30);
    _dio.options.receiveTimeout = const Duration(seconds: 30);
    
    // Add interceptor for automatic token and CSRF token attachment
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        // Add Bearer token
        final token = await getStoredToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        
        // Add CSRF token for POST, PUT, DELETE requests
        if (['POST', 'PUT', 'DELETE', 'PATCH'].contains(options.method)) {
          options.headers['X-CSRFToken'] = _csrfToken;
        }
        
        handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          // Token expired, clear stored data
          await clearStoredData();
        }
        handler.next(error);
      },
    ));
  }

  // Login method
  Future<LoginResponse> login(String username, String password) async {
    try {
      final request = LoginRequest(username: username, password: password);
      
      print('🔍 Login Request Details:');
      print('URL: ${ApiUrl.login}');
      print('Data: ${request.toJson()}');
      print('Headers will include: X-CSRFToken: $_csrfToken');
      
      final response = await _dio.post(
        ApiUrl.login,
        data: request.toJson(),
      );
      
      print('✅ Login Response:');
      print('Status Code: ${response.statusCode}');
      print('Response Data: ${response.data}');

      if (response.statusCode == 200) {
        final loginResponse = LoginResponse.fromJson(response.data);
        
        if (loginResponse.success && loginResponse.token != null) {
          OneSignal.login(loginResponse.user!.id);

          // Store token and user data
          await _storeToken(loginResponse.token!);
          if (loginResponse.user != null) {
            await _storeUser(loginResponse.user!);
          }
        }
        
        return loginResponse;
      } else {
        return LoginResponse(
          success: false,
          message: 'Login failed: ${response.statusMessage}',
        );
      }
    } on DioException catch (e) {
      print('❌ DioException during login:');
      print('Type: ${e.type}');
      print('Message: ${e.message}');
      print('Response: ${e.response?.data}');
      print('Status Code: ${e.response?.statusCode}');
      
      return LoginResponse(
        success: false,
        message: _handleDioError(e),
      );
    } catch (e) {
      print('❌ General Exception during login: $e');
      return LoginResponse(
        success: false,
        message: 'An unexpected error occurred: $e',
      );
    }
  }

  // Get user profile
  Future<ApiResponse<User>> getProfile() async {
    try {
      final response = await _dio.get(ApiUrl.profile);

      if (response.statusCode == 200) {
        return ApiResponse.fromJson(
          response.data,
          (json) => User.fromJson(json),
        );
      } else {
        return ApiResponse<User>(
          success: false,
          message: 'Failed to fetch profile: ${response.statusMessage}',
        );
      }
    } on DioException catch (e) {
      return ApiResponse<User>(
        success: false,
        message: _handleDioError(e),
      );
    } catch (e) {
      return ApiResponse<User>(
        success: false,
        message: 'An unexpected error occurred: $e',
      );
    }
  }

  // Logout method
  Future<void> logout() async {

      await clearStoredData();
      Get.offAll(() => LoginScreen());


  }

  // Check if user is logged in
  Future<bool> isLoggedIn() async {
    final token = await getStoredToken();
    return token != null && token.isNotEmpty;
  }

  // Get stored token
  Future<String?> getStoredToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_tokenKey);
  }

  // Get stored user
  Future<User?> getStoredUser() async {
    final prefs = await SharedPreferences.getInstance();
    final userJson = prefs.getString(_userKey);
    if (userJson != null) {
      // You might need to implement a proper JSON parsing here
      // For now, returning null as we need to know the exact format
      return null;
    }
    return null;
  }

  // Store token
  Future<void> _storeToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
  }

  // Store user data
  Future<void> _storeUser(User user) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userKey, user.toJson().toString());
  }

  // Clear all stored data
  Future<void> clearStoredData() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
    await prefs.remove(_userKey);
  }

  // Handle Dio errors
  String _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return 'Connection timeout. Please try again.';
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        final message = error.response?.data?['error'] ?? 
                       error.response?.data?['message'] ?? 
                       'Server error';
        return 'Error $statusCode: $message';
      case DioExceptionType.cancel:
        return 'Request was cancelled';
      case DioExceptionType.connectionError:
        return 'Unable to connect to server. Please check your internet connection.';
      default:
        return 'An unexpected error occurred. Please try again.';
    }
  }
}
