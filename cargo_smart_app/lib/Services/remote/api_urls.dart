class ApiUrl {
  static const String baseUrl = "http://10.0.2.2:8000/";

  // ################################
  // ||                            ||
  // ||          ROOT              ||
  // ||                            ||
  // ################################
  static const String root = baseUrl;

  // ################################
  // ||                            ||
  // ||            USER            ||
  // ||                            ||
  // ################################
  static const String account = "${baseUrl}accounts/mobile/";
  static const String login = "${account}login/";
  static const String profile = "${account}profile/";
  static const String logout = "${account}logout/";
  static const String csrf = "${baseUrl}accounts/csrf/";

  // ################################
  // ||                            ||
  // ||          SHIPMENTS         ||
  // ||                            ||
  // ################################
  static const String driverShipments =
      "${baseUrl}shipments/mobile/driver/shipments/";
  static String getShipmentDetail(String id) =>
      "${baseUrl}shipments/mobile/driver/shipment/$id/";
  static String markShipmentDelivered(String id) =>
      "${baseUrl}shipments/mobile/driver/shipment/$id/delivered/";
  static String updateShipmentStatus(String id) =>
      "${baseUrl}shipments/mobile/driver/shipment/$id/status/";

  // ################################
  // ||                            ||
  // ||        Notifications       ||
  // ||                            ||
  // ################################
}
