enum PlaceCategory { cafe, restaurant, park }

extension PlaceCategoryLabel on PlaceCategory {
  String get label {
    return switch (this) {
      PlaceCategory.cafe => 'Cafe',
      PlaceCategory.restaurant => 'Restaurant',
      PlaceCategory.park => 'Park',
    };
  }
}

class Place {
  const Place({
    required this.id,
    required this.name,
    required this.category,
    required this.address,
    required this.latitude,
    required this.longitude,
  });

  final String id;
  final String name;
  final PlaceCategory category;
  final String address;
  final double latitude;
  final double longitude;
}
