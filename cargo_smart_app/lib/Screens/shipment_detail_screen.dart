import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:cargo_smart_app/Controllers/shipment_controller.dart';
import 'package:cargo_smart_app/Models/shipment_models.dart';
import 'package:cargo_smart_app/Helpers/colors.dart';
import 'package:intl/intl.dart';

class ShipmentDetailScreen extends StatefulWidget {
  const ShipmentDetailScreen({super.key});

  @override
  State<ShipmentDetailScreen> createState() => _ShipmentDetailScreenState();
}

class _ShipmentDetailScreenState extends State<ShipmentDetailScreen> {
  final ShipmentController _shipmentController = Get.find<ShipmentController>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kBackgroundColor,
      appBar: AppBar(
        title: Text(
          'Shipment Details',
          style: TextStyle(
            fontSize: 20.sp,
            fontWeight: FontWeight.bold,
            color: kTextColor,
          ),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            onPressed: () => _shipmentController.loadShipmentDetail(
              _shipmentController.selectedShipment.value?.id ?? '',
            ),
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: Obx(() {
        final shipment = _shipmentController.selectedShipment.value;
        
        if (shipment == null) {
          return const Center(
            child: Text('No shipment selected'),
          );
        }

        if (_shipmentController.isLoading.value) {
          return const Center(
            child: CircularProgressIndicator(),
          );
        }

        return SingleChildScrollView(
          padding: EdgeInsets.all(16.w),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildShipmentHeader(shipment),
              SizedBox(height: 24.h),
              _buildShipmentInfo(shipment),
              SizedBox(height: 24.h),
              _buildRouteInfo(shipment),
              SizedBox(height: 24.h),
              _buildMilestones(shipment),
              SizedBox(height: 24.h),
              _buildActionButtons(shipment),
            ],
          ),
        );
      }),
    );
  }

  Widget _buildShipmentHeader(Shipment shipment) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.r),
      ),
      child: Padding(
        padding: EdgeInsets.all(16.w),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  shipment.refNo,
                  style: TextStyle(
                    fontSize: 20.sp,
                    fontWeight: FontWeight.bold,
                    color: kTextColor,
                  ),
                ),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 12.w, vertical: 6.h),
                  decoration: BoxDecoration(
                    color: _getStatusColor(shipment.status).withOpacity(0.1),
                    borderRadius: BorderRadius.circular(16.r),
                  ),
                  child: Text(
                    shipment.statusDisplayName,
                    style: TextStyle(
                      fontSize: 14.sp,
                      color: _getStatusColor(shipment.status),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
            if (shipment.carrierName != null) ...[
              SizedBox(height: 8.h),
              Text(
                'Carrier: ${shipment.carrierName}',
                style: TextStyle(
                  fontSize: 14.sp,
                  color: kSecondaryTextColor,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildShipmentInfo(Shipment shipment) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.r),
      ),
      child: Padding(
        padding: EdgeInsets.all(16.w),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Shipment Information',
              style: TextStyle(
                fontSize: 18.sp,
                fontWeight: FontWeight.bold,
                color: kTextColor,
              ),
            ),
            SizedBox(height: 16.h),
            _buildInfoRow(
              'Origin',
              shipment.origin.name,
              Icons.location_on,
              kPrimaryColor,
            ),
            SizedBox(height: 12.h),
            _buildInfoRow(
              'Destination',
              shipment.destination.name,
              Icons.location_on,
              Colors.red,
            ),
            SizedBox(height: 12.h),
            _buildInfoRow(
              'Scheduled Date',
              DateFormat('MMM dd, yyyy HH:mm').format(shipment.scheduledAt),
              Icons.schedule,
              kSecondaryTextColor,
            ),
            if (shipment.deliveredAt != null) ...[
              SizedBox(height: 12.h),
              _buildInfoRow(
                'Delivered Date',
                DateFormat('MMM dd, yyyy HH:mm').format(shipment.deliveredAt!),
                Icons.check_circle,
                Colors.green,
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildRouteInfo(Shipment shipment) {
    if (shipment.route == null) {
      return const SizedBox.shrink();
    }

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.r),
      ),
      child: Padding(
        padding: EdgeInsets.all(16.w),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Route Information',
              style: TextStyle(
                fontSize: 18.sp,
                fontWeight: FontWeight.bold,
                color: kTextColor,
              ),
            ),
            SizedBox(height: 16.h),
            _buildInfoRow(
              'Route Name',
              shipment.route!.name,
              Icons.route,
              kPrimaryColor,
            ),
            if (shipment.route!.distance != null) ...[
              SizedBox(height: 12.h),
              _buildInfoRow(
                'Distance',
                '${shipment.route!.distance!.toStringAsFixed(1)} km',
                Icons.straighten,
                kSecondaryTextColor,
              ),
            ],
            if (shipment.route!.estimatedDuration != null) ...[
              SizedBox(height: 12.h),
              _buildInfoRow(
                'Estimated Duration',
                '${shipment.route!.estimatedDuration} minutes',
                Icons.timer,
                kSecondaryTextColor,
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildMilestones(Shipment shipment) {
    if (shipment.milestones.isEmpty) {
      return const SizedBox.shrink();
    }

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.r),
      ),
      child: Padding(
        padding: EdgeInsets.all(16.w),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Milestones',
              style: TextStyle(
                fontSize: 18.sp,
                fontWeight: FontWeight.bold,
                color: kTextColor,
              ),
            ),
            SizedBox(height: 16.h),
            ...shipment.milestones.map((milestone) => _buildMilestoneItem(milestone)),
          ],
        ),
      ),
    );
  }

  Widget _buildMilestoneItem(ShipmentMilestone milestone) {
    return Container(
      margin: EdgeInsets.only(bottom: 12.h),
      padding: EdgeInsets.all(12.w),
      decoration: BoxDecoration(
        color: milestone.actual ? Colors.green.withOpacity(0.1) : Colors.grey.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8.r),
        border: Border.all(
          color: milestone.actual ? Colors.green : Colors.grey,
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Icon(
            _getMilestoneIcon(milestone.kind),
            color: milestone.actual ? Colors.green : Colors.grey,
            size: 20.sp,
          ),
          SizedBox(width: 12.w),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  milestone.kind,
                  style: TextStyle(
                    fontSize: 14.sp,
                    fontWeight: FontWeight.w600,
                    color: milestone.actual ? Colors.green : Colors.grey,
                  ),
                ),
                Text(
                  milestone.location.name,
                  style: TextStyle(
                    fontSize: 12.sp,
                    color: kSecondaryTextColor,
                  ),
                ),
                Text(
                  DateFormat('MMM dd, yyyy HH:mm').format(milestone.date),
                  style: TextStyle(
                    fontSize: 12.sp,
                    color: kSecondaryTextColor,
                  ),
                ),
              ],
            ),
          ),
          if (milestone.actual)
            Icon(
              Icons.check_circle,
              color: Colors.green,
              size: 20.sp,
            ),
        ],
      ),
    );
  }

  Widget _buildActionButtons(Shipment shipment) {
    if (shipment.isDelivered) {
      return const SizedBox.shrink();
    }

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.r),
      ),
      child: Padding(
        padding: EdgeInsets.all(16.w),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Actions',
              style: TextStyle(
                fontSize: 18.sp,
                fontWeight: FontWeight.bold,
                color: kTextColor,
              ),
            ),
            SizedBox(height: 16.h),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () => _updateShipmentStatus(shipment, 'IN_TRANSIT'),
                    icon: const Icon(Icons.play_arrow),
                    label: const Text('Start Delivery'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.orange,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8.r),
                      ),
                    ),
                  ),
                ),
                SizedBox(width: 12.w),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () => _markAsDelivered(shipment),
                    icon: const Icon(Icons.check),
                    label: const Text('Mark Delivered'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8.r),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value, IconData icon, Color color) {
    return Row(
      children: [
        Icon(
          icon,
          size: 16.sp,
          color: color,
        ),
        SizedBox(width: 8.w),
        Text(
          '$label: ',
          style: TextStyle(
            fontSize: 14.sp,
            fontWeight: FontWeight.w500,
            color: kTextColor,
          ),
        ),
        Expanded(
          child: Text(
            value,
            style: TextStyle(
              fontSize: 14.sp,
              color: kSecondaryTextColor,
            ),
          ),
        ),
      ],
    );
  }

  IconData _getMilestoneIcon(String kind) {
    switch (kind.toUpperCase()) {
      case 'LOADED':
        return Icons.inventory;
      case 'ENROUTE':
        return Icons.local_shipping;
      case 'DELIVERED':
        return Icons.check_circle;
      default:
        return Icons.place;
    }
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'PLANNED':
        return Colors.blue;
      case 'IN_TRANSIT':
      case 'ENROUTE':
        return Colors.orange;
      case 'DELIVERED':
        return Colors.green;
      default:
        return kSecondaryTextColor;
    }
  }

  Future<void> _updateShipmentStatus(Shipment shipment, String status) async {
    final success = await _shipmentController.updateShipmentStatus(shipment.id, status);
    
    if (success) {
      Get.snackbar(
        'Success',
        'Shipment status updated successfully',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.green,
        colorText: Colors.white,
      );
    } else {
      Get.snackbar(
        'Error',
        _shipmentController.errorMessage.value,
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.red,
        colorText: Colors.white,
      );
    }
  }

  Future<void> _markAsDelivered(Shipment shipment) async {
    final success = await _shipmentController.markShipmentDelivered(shipment.id);
    
    if (success) {
      Get.snackbar(
        'Success',
        'Shipment marked as delivered successfully',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.green,
        colorText: Colors.white,
      );
    } else {
      Get.snackbar(
        'Error',
        _shipmentController.errorMessage.value,
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.red,
        colorText: Colors.white,
      );
    }
  }
}
