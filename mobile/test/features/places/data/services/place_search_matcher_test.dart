import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/src/features/places/data/services/place_search_matcher.dart';
import 'package:mobile/src/features/places/domain/entities/place.dart';

void main() {
  const matcher = PlaceSearchMatcher();
  const place = Place(
    id: 'unity-park',
    name: 'Unity Park',
    category: PlaceCategory.park,
    address: 'Menelik II Avenue, Addis Ababa',
    latitude: 9.030100,
    longitude: 38.761300,
  );

  group('PlaceSearchMatcher', () {
    test('matches place name, location, and category', () {
      expect(matcher.matches(place, 'unity'), isTrue);
      expect(matcher.matches(place, 'menelik'), isTrue);
      expect(matcher.matches(place, 'park'), isTrue);
    });

    test('requires every search term to match the searchable text', () {
      expect(matcher.matches(place, 'unity addis'), isTrue);
      expect(matcher.matches(place, 'unity bole'), isFalse);
    });
  });
}
