import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:cargo_smart_app/Models/shipment_models.dart';
import 'package:cargo_smart_app/Models/auth_models.dart';
import 'package:cargo_smart_app/Services/remote/api_urls.dart';

class ShipmentServices {
  final Dio _dio = Dio();
  
  // Hardcoded CSRF token
  static const String _csrfToken = 'IwdTKQHOvXKP46q05bF14hUs8u1QaWrTWge1ZvQqxCXc5wdCoyRTVopVWlZpWz9t';

  ShipmentServices() {
    _dio.options.baseUrl = ApiUrl.baseUrl;
    _dio.options.connectTimeout = const Duration(seconds: 30);
    _dio.options.receiveTimeout = const Duration(seconds: 30);
    
    // Add interceptor for automatic token and CSRF token attachment
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        // Get token from shared preferences
        final prefs = await SharedPreferences.getInstance();
        final token = prefs.getString('auth_token');
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
          final prefs = await SharedPreferences.getInstance();
          await prefs.remove('auth_token');
          await prefs.remove('user_data');
        }
        handler.next(error);
      },
    ));
  }

  // Get all shipments for driver
  Future<ApiResponse<List<Shipment>>> getDriverShipments() async {
    try {
      final response = await _dio.get(ApiUrl.driverShipments);

      if (response.statusCode == 200) {
        final shipments = (response.data['shipments'] as List<dynamic>)
            .map((shipment) => Shipment.fromJson(shipment))
            .toList();
        
        return ApiResponse<List<Shipment>>(
          success: true,
          data: shipments,
        );
      } else {
        return ApiResponse<List<Shipment>>(
          success: false,
          message: 'Failed to fetch shipments: ${response.statusMessage}',
        );
      }
    } on DioException catch (e) {
      return ApiResponse<List<Shipment>>(
        success: false,
        message: _handleDioError(e),
      );
    } catch (e) {
      return ApiResponse<List<Shipment>>(
        success: false,
        message: 'An unexpected error occurred: $e',
      );
    }
  }

  // Get specific shipment details
  Future<ApiResponse<Shipment>> getShipmentDetail(String shipmentId) async {
    try {
      final response = await _dio.get(ApiUrl.getShipmentDetail(shipmentId));

      if (response.statusCode == 200) {
        final shipment = Shipment.fromJson(response.data['shipment']);
        
        return ApiResponse<Shipment>(
          success: true,
          data: shipment,
        );
      } else {
        return ApiResponse<Shipment>(
          success: false,
          message: 'Failed to fetch shipment details: ${response.statusMessage}',
        );
      }
    } on DioException catch (e) {
      return ApiResponse<Shipment>(
        success: false,
        message: _handleDioError(e),
      );
    } catch (e) {
      return ApiResponse<Shipment>(
        success: false,
        message: 'An unexpected error occurred: $e',
      );
    }
  }

  // Mark shipment as delivered
  Future<ApiResponse<Shipment>> markShipmentDelivered(String shipmentId) async {
    try {
      final response = await _dio.post(ApiUrl.markShipmentDelivered(shipmentId));

      if (response.statusCode == 200) {
        final shipment = Shipment.fromJson(response.data['shipment']);
        
        return ApiResponse<Shipment>(
          success: true,
          data: shipment,
          message: response.data['message'],
        );
      } else {
        return ApiResponse<Shipment>(
          success: false,
          message: 'Failed to mark shipment as delivered: ${response.statusMessage}',
        );
      }
    } on DioException catch (e) {
      return ApiResponse<Shipment>(
        success: false,
        message: _handleDioError(e),
      );
    } catch (e) {
      return ApiResponse<Shipment>(
        success: false,
        message: 'An unexpected error occurred: $e',
      );
    }
  }

  // Update shipment status
  Future<ApiResponse<Shipment>> updateShipmentStatus(
    String shipmentId, 
    String status
  ) async {
    try {
      final statusUpdate = ShipmentStatusUpdate(status: status);
      
      final response = await _dio.post(
        ApiUrl.updateShipmentStatus(shipmentId),
        data: statusUpdate.toJson(),
      );

      if (response.statusCode == 200) {
        final shipment = Shipment.fromJson(response.data['shipment']);
        
        return ApiResponse<Shipment>(
          success: true,
          data: shipment,
          message: response.data['message'],
        );
      } else {
        return ApiResponse<Shipment>(
          success: false,
          message: 'Failed to update shipment status: ${response.statusMessage}',
        );
      }
    } on DioException catch (e) {
      return ApiResponse<Shipment>(
        success: false,
        message: _handleDioError(e),
      );
    } catch (e) {
      return ApiResponse<Shipment>(
        success: false,
        message: 'An unexpected error occurred: $e',
      );
    }
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
