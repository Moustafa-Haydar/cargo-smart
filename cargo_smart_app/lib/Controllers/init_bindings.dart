import 'package:cargo_smart_app/Controllers/app_controller.dart';
import 'package:cargo_smart_app/Controllers/user_controller.dart';
import 'package:cargo_smart_app/Controllers/shipment_controller.dart';
import 'package:cargo_smart_app/Controllers/notification_controller.dart';
import 'package:cargo_smart_app/Services/network_service.dart';
import 'package:get/get.dart';

class InitialBindings extends Bindings {
  @override
  void dependencies() {
    Get.put(NetworkService());
    Get.put(AppController());
    Get.put(UserController());
    Get.put(ShipmentController());
    Get.put(NotificationController());
  }
}
