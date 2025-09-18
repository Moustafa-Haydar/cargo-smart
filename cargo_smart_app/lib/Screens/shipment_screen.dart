import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:cargo_smart_app/Controllers/shipment_controller.dart';
import 'package:cargo_smart_app/Models/shipment_models.dart';
import 'package:cargo_smart_app/Helpers/colors.dart';
import 'package:cargo_smart_app/Screens/shipment_detail_screen.dart';
import 'package:intl/intl.dart';

class ShipmentScreen extends StatefulWidget {
  const ShipmentScreen({super.key});

  @override
  State<ShipmentScreen> createState() => _ShipmentScreenState();
}

class _ShipmentScreenState extends State<ShipmentScreen> with TickerProviderStateMixin {
  final ShipmentController _shipmentController = Get.find<ShipmentController>();
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kBackgroundColor,
      appBar: AppBar(
        title: Text(
          'Shipments',
          style: TextStyle(
            fontSize: 20.sp,
            fontWeight: FontWeight.bold,
            color: kTextColor,
          ),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        bottom: TabBar(
          controller: _tabController,
          labelColor: kPrimaryColor,
          unselectedLabelColor: kSecondaryTextColor,
          indicatorColor: kPrimaryColor,
          tabs: [
            Tab(text: 'All'),
            Tab(text: 'Active'),
            Tab(text: 'Delivered'),
          ],
        ),
      ),
      body: Obx(() {
        if (_shipmentController.isLoading.value) {
          return const Center(
            child: CircularProgressIndicator(),
          );
        }

        if (_shipmentController.errorMessage.value.isNotEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  Icons.error_outline,
                  size: 64.sp,
                  color: Colors.red,
                ),
                SizedBox(height: 16.h),
                Text(
                  _shipmentController.errorMessage.value,
                  style: TextStyle(
                    fontSize: 16.sp,
                    color: Colors.red,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 16.h),
                ElevatedButton(
                  onPressed: () => _shipmentController.loadShipments(),
                  child: const Text('Retry'),
                ),
              ],
            ),
          );
        }

        return TabBarView(
          controller: _tabController,
          children: [
            _buildShipmentList(_shipmentController.shipments),
            _buildShipmentList(_shipmentController.activeShipments),
            _buildShipmentList(_shipmentController.deliveredShipments),
          ],
        );
      }),
    );
  }

  Widget _buildShipmentList(List<Shipment> shipments) {
    if (shipments.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.local_shipping_outlined,
              size: 64.sp,
              color: kSecondaryTextColor,
            ),
            SizedBox(height: 16.h),
            Text(
              'No shipments found',
              style: TextStyle(
                fontSize: 18.sp,
                color: kSecondaryTextColor,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: () => _shipmentController.loadShipments(),
      child: ListView.builder(
        padding: EdgeInsets.all(16.w),
        itemCount: shipments.length,
        itemBuilder: (context, index) {
          final shipment = shipments[index];
          return _buildShipmentCard(shipment);
        },
      ),
    );
  }

  Widget _buildShipmentCard(Shipment shipment) {
    return Card(
      margin: EdgeInsets.only(bottom: 16.h),
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.r),
      ),
      child: InkWell(
        onTap: () {
          _shipmentController.selectShipment(shipment);
          Get.to(() => const ShipmentDetailScreen());
        },
        borderRadius: BorderRadius.circular(12.r),
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
                      fontSize: 16.sp,
                      fontWeight: FontWeight.bold,
                      color: kTextColor,
                    ),
                  ),
                  Container(
                    padding: EdgeInsets.symmetric(horizontal: 8.w, vertical: 4.h),
                    decoration: BoxDecoration(
                      color: _getStatusColor(shipment.status).withOpacity(0.1),
                      borderRadius: BorderRadius.circular(12.r),
                    ),
                    child: Text(
                      shipment.statusDisplayName,
                      style: TextStyle(
                        fontSize: 12.sp,
                        color: _getStatusColor(shipment.status),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 12.h),
              Row(
                children: [
                  Icon(
                    Icons.location_on,
                    size: 16.sp,
                    color: kPrimaryColor,
                  ),
                  SizedBox(width: 8.w),
                  Expanded(
                    child: Text(
                      '${shipment.origin.name} → ${shipment.destination.name}',
                      style: TextStyle(
                        fontSize: 14.sp,
                        color: kTextColor,
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 8.h),
              Row(
                children: [
                  Icon(
                    Icons.schedule,
                    size: 16.sp,
                    color: kSecondaryTextColor,
                  ),
                  SizedBox(width: 8.w),
                  Text(
                    'Scheduled: ${DateFormat('MMM dd, yyyy HH:mm').format(shipment.scheduledAt)}',
                    style: TextStyle(
                      fontSize: 12.sp,
                      color: kSecondaryTextColor,
                    ),
                  ),
                ],
              ),
              if (shipment.deliveredAt != null) ...[
                SizedBox(height: 8.h),
                Row(
                  children: [
                    Icon(
                      Icons.check_circle,
                      size: 16.sp,
                      color: Colors.green,
                    ),
                    SizedBox(width: 8.w),
                    Text(
                      'Delivered: ${DateFormat('MMM dd, yyyy HH:mm').format(shipment.deliveredAt!)}',
                      style: TextStyle(
                        fontSize: 12.sp,
                        color: Colors.green,
                      ),
                    ),
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
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
}