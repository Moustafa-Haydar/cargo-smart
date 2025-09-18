import 'package:cargo_smart_app/Models/user_model.dart';

class LoginRequest {
  final String username;
  final String password;

  LoginRequest({
    required this.username,
    required this.password,
  });

  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'password': password,
    };
  }
}

class LoginResponse {
  final bool success;
  final String? token;
  final User? user;
  final String? message;

  LoginResponse({
    required this.success,
    this.token,
    this.user,
    this.message,
  });

  factory LoginResponse.fromJson(Map<String, dynamic> json) {
    return LoginResponse(
      success: json['token'] != null,
      token: json['token'],
      user: json['user'] != null ? User.fromJson(json['user']) : null,
      message: json['error'] ?? json['message'],
    );
  }
}

class ApiResponse<T> {
  final bool success;
  final T? data;
  final String? message;

  ApiResponse({
    required this.success,
    this.data,
    this.message,
  });

  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Map<String, dynamic>) fromJsonT,
  ) {
    return ApiResponse<T>(
      success: json['error'] == null,
      data: json['user'] != null ? fromJsonT(json['user']) : null,
      message: json['error'] ?? json['message'],
    );
  }
}
