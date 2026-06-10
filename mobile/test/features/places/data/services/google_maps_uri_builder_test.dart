import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/src/features/places/data/services/google_maps_uri_builder.dart';
import 'package:mobile/src/features/places/domain/entities/place.dart';

void main() {
  group('GoogleMapsUriBuilder', () {
    test('builds a Google Maps search URL from place coordinates', () {
      const place = Place(
        id: 'unity-park',
        name: 'Unity Park',
        category: PlaceCategory.park,
        address: 'Menelik II Avenue, Addis Ababa',
        latitude: 9.0301002,
        longitude: 38.7612997,
      );

      final uri = const GoogleMapsUriBuilder().buildPlaceSearchUri(place);

      expect(uri.scheme, 'https');
      expect(uri.host, 'www.google.com');
      expect(uri.path, '/maps/search/');
      expect(uri.queryParameters['api'], '1');
      expect(uri.queryParameters['query'], '9.030100,38.761300');
    });
  });
}
