import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:cargo_smart_app/Models/user_model.dart';
import 'package:cargo_smart_app/Models/auth_models.dart';
import 'package:cargo_smart_app/Services/remote/user_services.dart';

class UserController extends GetxController {
  final UserServices _userService = UserServices();
  
  // Observable variables
  final RxBool isLoading = false.obs;
  final RxBool isLoggedIn = false.obs;
  final Rx<User?> currentUser = Rx<User?>(null);
  final RxString errorMessage = ''.obs;

  @override
  void onInit() {
    super.onInit();
    checkAuthStatus();
  }

  // Check if user is already logged in
  Future<void> checkAuthStatus() async {
    isLoading.value = true;
    try {
      final loggedIn = await _userService.isLoggedIn();
      isLoggedIn.value = loggedIn;
      
      if (loggedIn) {
        // Try to get user profile
        await getProfile();
      }
    } catch (e) {
      errorMessage.value = 'Error checking auth status: $e';
    } finally {
      isLoading.value = false;
    }
  }

  // Login method
  Future<bool> login(String username, String password) async {
    if (username.isEmpty || password.isEmpty) {
      errorMessage.value = 'Please fill in all fields';
      return false;
    }

    isLoading.value = true;
    errorMessage.value = '';

    try {
      final response = await _userService.login(username, password);
      
      if (response.success) {
        isLoggedIn.value = true;
        currentUser.value = response.user;
        errorMessage.value = '';
        return true;
      } else {
        errorMessage.value = response.message ?? 'Login failed';
        return false;
      }
    } catch (e) {
      errorMessage.value = 'Login error: $e';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  // Get user profile
  Future<void> getProfile() async {
    try {
      final response = await _userService.getProfile();
      
      if (response.success && response.data != null) {
        currentUser.value = response.data;
      } else {
        errorMessage.value = response.message ?? 'Failed to get profile';
      }
    } catch (e) {
      errorMessage.value = 'Profile error: $e';
    }
  }

  // Logout method
  Future<void> logout() async {
    isLoading.value = true;
    try {
      // Call backend logout
      await _userService.logout();
      
      // Clear local state
      isLoggedIn.value = false;
      currentUser.value = null;
      errorMessage.value = '';
      
      // Clear OneSignal external user ID (if using OneSignal)
      // This ensures the user won't receive notifications after logout
      try {
        // Uncomment if you're using OneSignal
        // await OneSignal.User.removeExternalUserId();
      } catch (e) {
        print('OneSignal cleanup error: $e');
      }
      
      // Show success message
      Get.snackbar(
        'Success',
        'Logged out successfully',
        snackPosition: SnackPosition.TOP,
        backgroundColor: Colors.green,
        colorText: Colors.white,
        duration: const Duration(seconds: 2),
      );
      
      // Navigate to login screen
      Get.offAllNamed('/login');
    } catch (e) {
      errorMessage.value = 'Logout error: $e';
      
      // Show error message
      Get.snackbar(
        'Error',
        'Logout failed: $e',
        snackPosition: SnackPosition.TOP,
        backgroundColor: Colors.red,
        colorText: Colors.white,
        duration: const Duration(seconds: 3),
      );
    } finally {
      isLoading.value = false;
    }
  }

  // Clear error message
  void clearError() {
    errorMessage.value = '';
  }

  // Update user profile
  void updateUser(User user) {
    currentUser.value = user;
  }

}
