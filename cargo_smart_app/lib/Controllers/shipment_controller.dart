import 'package:get/get.dart';
import 'package:cargo_smart_app/Models/shipment_models.dart';
import 'package:cargo_smart_app/Services/remote/shipment_services.dart';

class ShipmentController extends GetxController {
  final ShipmentServices _shipmentService = ShipmentServices();
  
  // Observable variables
  final RxBool isLoading = false.obs;
  final RxList<Shipment> shipments = <Shipment>[].obs;
  final Rx<Shipment?> selectedShipment = Rx<Shipment?>(null);
  final RxString errorMessage = ''.obs;

  @override
  void onInit() {
    super.onInit();
    loadShipments();
  }

  // Load all shipments
  Future<void> loadShipments() async {
    isLoading.value = true;
    errorMessage.value = '';
    
    try {
      final response = await _shipmentService.getDriverShipments();
      
      if (response.success && response.data != null) {
        shipments.value = response.data!;
        errorMessage.value = '';
      } else {
        errorMessage.value = response.message ?? 'Failed to load shipments';
      }
    } catch (e) {
      errorMessage.value = 'Error loading shipments: $e';
    } finally {
      isLoading.value = false;
    }
  }

  // Load specific shipment details
  Future<void> loadShipmentDetail(String shipmentId) async {
    isLoading.value = true;
    errorMessage.value = '';
    
    try {
      final response = await _shipmentService.getShipmentDetail(shipmentId);
      
      if (response.success && response.data != null) {
        selectedShipment.value = response.data!;
        errorMessage.value = '';
      } else {
        errorMessage.value = response.message ?? 'Failed to load shipment details';
      }
    } catch (e) {
      errorMessage.value = 'Error loading shipment details: $e';
    } finally {
      isLoading.value = false;
    }
  }

  // Mark shipment as delivered
  Future<bool> markShipmentDelivered(String shipmentId) async {
    isLoading.value = true;
    errorMessage.value = '';
    
    try {
      final response = await _shipmentService.markShipmentDelivered(shipmentId);
      
      if (response.success && response.data != null) {
        // Update the shipment in the list
        final index = shipments.indexWhere((s) => s.id == shipmentId);
        if (index != -1) {
          shipments[index] = response.data!;
        }
        
        // Update selected shipment if it's the same
        if (selectedShipment.value?.id == shipmentId) {
          selectedShipment.value = response.data!;
        }
        
        errorMessage.value = '';
        return true;
      } else {
        errorMessage.value = response.message ?? 'Failed to mark shipment as delivered';
        return false;
      }
    } catch (e) {
      errorMessage.value = 'Error marking shipment as delivered: $e';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  // Update shipment status
  Future<bool> updateShipmentStatus(String shipmentId, String status) async {
    isLoading.value = true;
    errorMessage.value = '';
    
    try {
      final response = await _shipmentService.updateShipmentStatus(shipmentId, status);
      
      if (response.success && response.data != null) {
        // Update the shipment in the list
        final index = shipments.indexWhere((s) => s.id == shipmentId);
        if (index != -1) {
          shipments[index] = response.data!;
        }
        
        // Update selected shipment if it's the same
        if (selectedShipment.value?.id == shipmentId) {
          selectedShipment.value = response.data!;
        }
        
        errorMessage.value = '';
        return true;
      } else {
        errorMessage.value = response.message ?? 'Failed to update shipment status';
        return false;
      }
    } catch (e) {
      errorMessage.value = 'Error updating shipment status: $e';
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  // Set selected shipment
  void selectShipment(Shipment shipment) {
    selectedShipment.value = shipment;
  }

  // Clear selected shipment
  void clearSelectedShipment() {
    selectedShipment.value = null;
  }

  // Clear error message
  void clearError() {
    errorMessage.value = '';
  }

  // Get shipments by status
  List<Shipment> getShipmentsByStatus(String status) {
    return shipments.where((shipment) => shipment.status == status).toList();
  }

  // Get active shipments (not delivered)
  List<Shipment> get activeShipments {
    return shipments.where((shipment) => !shipment.isDelivered).toList();
  }

  // Get delivered shipments
  List<Shipment> get deliveredShipments {
    return shipments.where((shipment) => shipment.isDelivered).toList();
  }
}
