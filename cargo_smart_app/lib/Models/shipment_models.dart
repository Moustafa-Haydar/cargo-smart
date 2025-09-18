class Location {
  final String id;
  final String name;
  final String? address;
  final double? latitude;
  final double? longitude;

  Location({
    required this.id,
    required this.name,
    this.address,
    this.latitude,
    this.longitude,
  });

  factory Location.fromJson(Map<String, dynamic> json) {
    return Location(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      address: json['address'],
      latitude: json['latitude']?.toDouble(),
      longitude: json['longitude']?.toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'address': address,
      'latitude': latitude,
      'longitude': longitude,
    };
  }
}

class Route {
  final String id;
  final String name;
  final String? polyline;
  final double? distance;
  final int? estimatedDuration;

  Route({
    required this.id,
    required this.name,
    this.polyline,
    this.distance,
    this.estimatedDuration,
  });

  factory Route.fromJson(Map<String, dynamic> json) {
    return Route(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      polyline: json['polyline'],
      distance: json['distance']?.toDouble(),
      estimatedDuration: json['estimated_duration'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'polyline': polyline,
      'distance': distance,
      'estimated_duration': estimatedDuration,
    };
  }
}

class ShipmentMilestone {
  final String id;
  final String kind;
  final Location location;
  final DateTime date;
  final bool actual;
  final DateTime? predictiveEta;

  ShipmentMilestone({
    required this.id,
    required this.kind,
    required this.location,
    required this.date,
    required this.actual,
    this.predictiveEta,
  });

  factory ShipmentMilestone.fromJson(Map<String, dynamic> json) {
    return ShipmentMilestone(
      id: json['id']?.toString() ?? '',
      kind: json['kind'] ?? '',
      location: Location.fromJson(json['location'] ?? {}),
      date: DateTime.parse(json['date']),
      actual: json['actual'] ?? false,
      predictiveEta: json['predictive_eta'] != null 
          ? DateTime.parse(json['predictive_eta']) 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'kind': kind,
      'location': location.toJson(),
      'date': date.toIso8601String(),
      'actual': actual,
      'predictive_eta': predictiveEta?.toIso8601String(),
    };
  }
}

class Shipment {
  final String id;
  final String refNo;
  final String status;
  final String? carrierName;
  final Location origin;
  final Location destination;
  final Location? currentLocation;
  final Route? route;
  final DateTime scheduledAt;
  final DateTime? deliveredAt;
  final List<ShipmentMilestone> milestones;

  Shipment({
    required this.id,
    required this.refNo,
    required this.status,
    this.carrierName,
    required this.origin,
    required this.destination,
    this.currentLocation,
    this.route,
    required this.scheduledAt,
    this.deliveredAt,
    required this.milestones,
  });

  factory Shipment.fromJson(Map<String, dynamic> json) {
    return Shipment(
      id: json['id']?.toString() ?? '',
      refNo: json['ref_no'] ?? '',
      status: json['status'] ?? '',
      carrierName: json['carrier_name'],
      origin: Location.fromJson(json['origin'] ?? {}),
      destination: Location.fromJson(json['destination'] ?? {}),
      currentLocation: json['current_location'] != null 
          ? Location.fromJson(json['current_location']) 
          : null,
      route: json['route'] != null 
          ? Route.fromJson(json['route']) 
          : null,
      scheduledAt: DateTime.parse(json['scheduled_at']),
      deliveredAt: json['delivered_at'] != null 
          ? DateTime.parse(json['delivered_at']) 
          : null,
      milestones: (json['milestones'] as List<dynamic>?)
          ?.map((milestone) => ShipmentMilestone.fromJson(milestone))
          .toList() ?? [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'ref_no': refNo,
      'status': status,
      'carrier_name': carrierName,
      'origin': origin.toJson(),
      'destination': destination.toJson(),
      'current_location': currentLocation?.toJson(),
      'route': route?.toJson(),
      'scheduled_at': scheduledAt.toIso8601String(),
      'delivered_at': deliveredAt?.toIso8601String(),
      'milestones': milestones.map((milestone) => milestone.toJson()).toList(),
    };
  }

  // Helper methods
  bool get isDelivered => status == 'DELIVERED';
  bool get isInTransit => status == 'IN_TRANSIT' || status == 'ENROUTE';
  bool get isPlanned => status == 'PLANNED';
  
  String get statusDisplayName {
    switch (status) {
      case 'PLANNED':
        return 'Planned';
      case 'IN_TRANSIT':
      case 'ENROUTE':
        return 'In Transit';
      case 'DELIVERED':
        return 'Delivered';
      default:
        return status;
    }
  }
}

class ShipmentStatusUpdate {
  final String status;

  ShipmentStatusUpdate({required this.status});

  Map<String, dynamic> toJson() {
    return {
      'status': status,
    };
  }
}
