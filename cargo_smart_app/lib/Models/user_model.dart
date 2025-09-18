class User {
  final String id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;
  final bool isActive;
  final List<String> groups;

  User({
    required this.id,
    required this.username,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.isActive,
    required this.groups,
  });

  String get fullName => '$firstName $lastName'.trim();

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id']?.toString() ?? '',
      username: json['username'] ?? '',
      email: json['email'] ?? '',
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      isActive: json['is_active'] ?? false,
      groups: List<String>.from(json['groups'] ?? []),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'first_name': firstName,
      'last_name': lastName,
      'is_active': isActive,
      'groups': groups,
    };
  }
}

