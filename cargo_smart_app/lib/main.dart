import 'dart:developer';

import 'package:cargo_smart_app/Controllers/init_bindings.dart';
import 'package:cargo_smart_app/Screens/Layout/main_layout.dart';
import 'package:cargo_smart_app/Screens/login_screen.dart';
import 'package:cargo_smart_app/Screens/splash_screen.dart';
import 'package:cargo_smart_app/Services/notification_service.dart';
import 'package:cargo_smart_app/firebase_options.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/route_manager.dart';
import 'package:logger/web.dart';
import 'package:onesignal_flutter/onesignal_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  
  // Initialize Firebase
  final res = await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  print(res);
  
  // Initialize notification service
  await NotificationService.initialize();
  
  runApp(const MyApp());
}

Logger logger = Logger();

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(
      designSize: const Size(393, 852),
      minTextAdapt: true,
      splitScreenMode: false,
      builder: (_, child) {
        return GetMaterialApp(
          defaultTransition: Transition.cupertino,
          theme: ThemeData(
            textSelectionTheme: const TextSelectionThemeData(
              cursorColor: Colors.black,
            ),
            // fontFamily: 'Montserrat',
            scaffoldBackgroundColor: Colors.white,
            bottomSheetTheme: const BottomSheetThemeData(
              surfaceTintColor: Colors.white,
            ),
            dialogBackgroundColor: Colors.white,
            appBarTheme: const AppBarTheme(color: Colors.white, elevation: 0),
            useMaterial3: true,
            colorScheme: ColorScheme.fromSeed(
              seedColor: Colors.white,
              surfaceTint: Colors.white,
              error: Colors.red,
            ),
          ),
          debugShowCheckedModeBanner: false,
          initialBinding: InitialBindings(),
          title: 'Cargo Smart',
          builder: (context, child) {
            return MediaQuery(
              data: MediaQuery.of(
                context,
              ).copyWith(textScaler: const TextScaler.linear(1.0)),
              child: child!,
            );
          },
          home: const SplashScreen(),
        );
      },
    );
  }
}
