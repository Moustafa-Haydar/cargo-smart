import 'package:cargo_smart_app/Controllers/user_controller.dart';
import 'package:cargo_smart_app/Helpers/colors.dart';
import 'package:cargo_smart_app/Screens/Layout/main_layout.dart';
import 'package:cargo_smart_app/Utils/connectivity_utils.dart';
import 'package:cargo_smart_app/Utils/backend_test.dart';
import 'package:cargo_smart_app/Utils/postman_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final UserController _userController = Get.find<UserController>();
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (_formKey.currentState!.validate()) {
      final success = await _userController.login(
        _usernameController.text.trim(),
        _passwordController.text,
      );

      if (success) {
        Get.offAll(() => const MainLayout());
      }
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kBackgroundColor,
      body: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(24.w),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Logo
                Image.asset("assets/logo.png", height: 120.h),
                SizedBox(height: 32.h),

                // Title
                Text(
                  "Welcome Back",
                  style: TextStyle(
                    fontSize: 28.sp,
                    fontWeight: FontWeight.bold,
                    color: kTextColor,
                    fontFamily: "Arial",
                  ),
                ),
                SizedBox(height: 8.h),
                Text(
                  "Login to continue",
                  style: TextStyle(
                    fontSize: 16.sp,
                    color: kSecondaryTextColor,
                    fontFamily: "Arial",
                  ),
                ),
                SizedBox(height: 40.h),

                // Error Message
                Obx(() {
                  if (_userController.errorMessage.value.isNotEmpty) {
                    return Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(12.w),
                      margin: EdgeInsets.only(bottom: 16.h),
                      decoration: BoxDecoration(
                        color: Colors.red.shade50,
                        borderRadius: BorderRadius.circular(8.r),
                        border: Border.all(color: Colors.red.shade200),
                      ),
                      child: Text(
                        _userController.errorMessage.value,
                        style: TextStyle(
                          color: Colors.red.shade700,
                          fontSize: 14.sp,
                        ),
                      ),
                    );
                  }
                  return const SizedBox.shrink();
                }),

                // Username Field
                TextFormField(
                  controller: _usernameController,
                  keyboardType: TextInputType.text,
                  decoration: InputDecoration(
                    labelText: "Username",
                    labelStyle: TextStyle(
                      color: kSecondaryTextColor,
                      fontFamily: "Arial",
                    ),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12.r),
                    ),
                    prefixIcon: const Icon(Icons.person, color: kPrimaryColor),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your username';
                    }
                    if (value.length < 3) {
                      return 'Username must be at least 3 characters';
                    }
                    return null;
                  },
                ),
                SizedBox(height: 16.h),

                // Password Field
                TextFormField(
                  controller: _passwordController,
                  obscureText: _obscurePassword,
                  decoration: InputDecoration(
                    labelText: "Password",
                    labelStyle: TextStyle(
                      color: kSecondaryTextColor,
                      fontFamily: "Arial",
                    ),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12.r),
                    ),
                    prefixIcon: const Icon(Icons.lock, color: kPrimaryColor),
                    suffixIcon: IconButton(
                      icon: Icon(
                        _obscurePassword ? Icons.visibility : Icons.visibility_off,
                        color: kPrimaryColor,
                      ),
                      onPressed: () {
                        setState(() {
                          _obscurePassword = !_obscurePassword;
                        });
                      },
                    ),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your password';
                    }
                    if (value.length < 6) {
                      return 'Password must be at least 6 characters';
                    }
                    return null;
                  },
                ),
                SizedBox(height: 20.h),

                // Login Button
                Obx(() {
                  return SizedBox(
                    width: double.infinity,
                    height: 50.h,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: kSecondaryColor,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12.r),
                        ),
                        elevation: 0,
                      ),
                      onPressed: _userController.isLoading.value ? null : _handleLogin,
                      child: _userController.isLoading.value
                          ? SizedBox(
                              height: 20.h,
                              width: 20.w,
                              child: const CircularProgressIndicator(
                                color: Colors.white,
                                strokeWidth: 2,
                              ),
                            )
                          : Text(
                              "Login",
                              style: TextStyle(
                                fontSize: 18.sp,
                                fontFamily: "Arial",
                                color: Colors.white,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                    ),
                  );
                }),

                SizedBox(height: 20.h),

                // Forgot Password (Optional)
                TextButton(
                  onPressed: () {
                    // TODO: Implement forgot password
                    Get.snackbar(
                      'Info',
                      'Forgot password feature coming soon',
                      snackPosition: SnackPosition.BOTTOM,
                      backgroundColor: kPrimaryColor,
                      colorText: Colors.white,
                    );
                  },
                  child: Text(
                    "Forgot Password?",
                    style: TextStyle(
                      color: kPrimaryColor,
                      fontSize: 14.sp,
                      fontFamily: "Arial",
                    ),
                  ),
                ),

                SizedBox(height: 16.h),

                // Connectivity Check Button (for debugging)
                TextButton(
                  onPressed: () {
                    ConnectivityUtils.showConnectivityDialog();
                  },
                  child: Text(
                    "Check Connectivity",
                    style: TextStyle(
                      color: kSecondaryTextColor,
                      fontSize: 12.sp,
                      fontFamily: "Arial",
                    ),
                  ),
                ),

                SizedBox(height: 8.h),

                // Backend Test Button (for debugging)
                TextButton(
                  onPressed: () {
                    BackendTest.testBackendConnection();
                  },
                  child: Text(
                    "Test Backend Connection",
                    style: TextStyle(
                      color: kSecondaryTextColor,
                      fontSize: 12.sp,
                      fontFamily: "Arial",
                    ),
                  ),
                ),

                SizedBox(height: 8.h),

                // Postman-Style Test Button (for debugging)
                TextButton(
                  onPressed: () {
                    PostmanTest.testLoginRequest();
                  },
                  child: Text(
                    "Test Login Request (Postman Style)",
                    style: TextStyle(
                      color: kSecondaryTextColor,
                      fontSize: 12.sp,
                      fontFamily: "Arial",
                    ),
                  ),
                ),

              ],
            ),
          ),
        ),
      ),
    );
  }
}
