import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:cargo_smart_app/Controllers/user_controller.dart';
import 'package:cargo_smart_app/Helpers/colors.dart';
import 'package:cargo_smart_app/Screens/Layout/main_layout.dart';
import 'package:cargo_smart_app/Screens/login_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  final UserController _userController = Get.find<UserController>();

  @override
  void initState() {
    super.initState();
    _checkAuthAndNavigate();
  }

  Future<void> _checkAuthAndNavigate() async {
    // Wait for a minimum splash duration
    await Future.delayed(const Duration(seconds: 2));
    
    // Check authentication status
    await _userController.checkAuthStatus();
    
    // Navigate based on auth status
    if (_userController.isLoggedIn.value) {
      Get.offAll(() => const MainLayout());
    } else {
      Get.offAll(() => const LoginScreen());
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kBackgroundColor,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Logo
            Image.asset(
              "assets/logo.png",
              height: 120.h,
              width: 120.w,
            ),
            SizedBox(height: 32.h),
            
            // App Name
            Text(
              "Cargo Smart",
              style: TextStyle(
                fontSize: 28.sp,
                fontWeight: FontWeight.bold,
                color: kTextColor,
                fontFamily: "Arial",
              ),
            ),
            SizedBox(height: 8.h),
            
            // Tagline
            Text(
              "Smart Logistics Management",
              style: TextStyle(
                fontSize: 16.sp,
                color: kSecondaryTextColor,
                fontFamily: "Arial",
              ),
            ),
            SizedBox(height: 48.h),
            
            // Loading indicator
            const CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(kPrimaryColor),
            ),
            SizedBox(height: 16.h),
            
            // Loading text
            Text(
              "Loading...",
              style: TextStyle(
                fontSize: 14.sp,
                color: kSecondaryTextColor,
                fontFamily: "Arial",
              ),
            ),
          ],
        ),
      ),
    );
  }
}
