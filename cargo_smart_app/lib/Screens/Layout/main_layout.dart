import 'package:cargo_smart_app/Controllers/app_controller.dart';
import 'package:cargo_smart_app/Controllers/user_controller.dart';
import 'package:cargo_smart_app/Helpers/colors.dart';
import 'package:cargo_smart_app/Screens/shipment_screen.dart';
import 'package:cargo_smart_app/Screens/notifications_screen.dart';
import 'package:cargo_smart_app/Services/remote/user_services.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

import 'package:get/get.dart';

class MainLayout extends StatefulWidget {
  const MainLayout({super.key});

  @override
  State<MainLayout> createState() => _MainLayoutState();
}

class _MainLayoutState extends State<MainLayout> {
  final AppController _appController = Get.find<AppController>();
  final UserController _userController = Get.find<UserController>();
  final List<Widget> _screensList = [
    const ShipmentScreen(),
    const NotificationsScreen(),
  ];

  void _showLogoutDialog() {
    Get.dialog(
      Obx(() => AlertDialog(
        title: Text(
          'Logout',
          style: TextStyle(fontSize: 18.sp, fontWeight: FontWeight.bold),
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Are you sure you want to logout?',
              style: TextStyle(fontSize: 16.sp),
            ),
            if (_userController.isLoading.value) ...[
              10.verticalSpace,
              const CircularProgressIndicator(),
              5.verticalSpace,
              Text(
                'Logging out...',
                style: TextStyle(fontSize: 12.sp, color: kSecondaryTextColor),
              ),
            ],
          ],
        ),
        actions: [
          TextButton(
            onPressed: _userController.isLoading.value ? null : () => Get.back(),
            child: Text(
              'Cancel',
              style: TextStyle(
                color: _userController.isLoading.value 
                    ? kSecondaryTextColor.withOpacity(0.5)
                    : kSecondaryTextColor, 
                fontSize: 14.sp,
              ),
            ),
          ),
          TextButton(
            onPressed: _userController.isLoading.value 
                ? null 
                : () async {
                    Get.back();
                    await UserServices().logout();
                  },
            child: Text(
              'Logout',
              style: TextStyle(
                color: _userController.isLoading.value 
                    ? Colors.red.withOpacity(0.5)
                    : Colors.red,
                fontSize: 14.sp,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ],
      )),
      barrierDismissible: !_userController.isLoading.value,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Obx(() {
      return Scaffold(
        appBar: AppBar(
          centerTitle: true,
          toolbarHeight: 70.h,
          elevation: 0.1,
          shadowColor: Colors.grey[200],
          title: Image.asset('assets/logo.png', height: 45.h),
          actions: [
            Obx(() => IconButton(
              onPressed: _userController.isLoading.value 
                  ? null 
                  : () {
                      _showLogoutDialog();
                    },
              icon: _userController.isLoading.value
                  ? SizedBox(
                      width: 20.w,
                      height: 20.h,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation<Color>(kPrimaryColor),
                      ),
                    )
                  : Icon(Icons.logout, color: kPrimaryColor),
            )),
            10.horizontalSpace,
          ],
        ),

        body: _screensList[_appController.currentIndex.value],
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _appController.currentIndex.value,
          onTap: (index) {
            _appController.currentIndex.value = index;
          },
          type: BottomNavigationBarType.fixed,
          backgroundColor: kPrimaryColor,
          selectedFontSize: 12.sp,
          unselectedFontSize: 12.sp,
          selectedItemColor: Colors.white,
          unselectedItemColor: Colors.white,
          selectedLabelStyle: TextStyle(
            fontSize: 12.sp,
            fontWeight: FontWeight.w600,
          ),
          items: <BottomNavigationBarItem>[
            BottomNavigationBarItem(
              activeIcon: Container(
                padding: EdgeInsets.only(
                  left: 10.w,
                  right: 10.w,
                  top: 2.r,
                  bottom: 2.r,
                ),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(50.r),
                ),
                child: Icon(Icons.home, color: kSecondaryColor),
              ),
              backgroundColor: Colors.white,
              icon: Padding(
                padding: const EdgeInsets.only(top: 4).r,
                child: Icon(Icons.home, color: Colors.white),
              ),
              label: 'Shipments',
            ),
            BottomNavigationBarItem(
              activeIcon: Container(
                padding: EdgeInsets.only(left: 10.w, right: 10.w),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(50.r),
                ),
                child: Icon(Icons.notifications, color: kSecondaryColor),
              ),
              icon: Padding(
                padding: const EdgeInsets.only(top: 4).r,
                child: Icon(Icons.notifications, color: Colors.white),
              ),
              label: 'Notifcations',
            ),
          ],
        ),
      );
    });
  }
}
