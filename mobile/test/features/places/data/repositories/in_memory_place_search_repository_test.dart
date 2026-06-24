import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/src/features/places/data/repositories/in_memory_place_search_repository.dart';
import 'package:mobile/src/features/places/domain/entities/place.dart';

void main() {
  const places = <Place>[
    Place(
      id: 'buna-bistro',
      name: 'Buna Bistro',
      category: PlaceCategory.cafe,
      address: 'Bole Road, Addis Ababa',
      latitude: 9.005401,
      longitude: 38.763611,
    ),
    Place(
      id: 'unity-park',
      name: 'Unity Park',
      category: PlaceCategory.park,
      address: 'Menelik II Avenue, Addis Ababa',
      latitude: 9.030100,
      longitude: 38.761300,
    ),
  ];

  group('InMemoryPlaceSearchRepository', () {
    test('returns all places for an empty query', () async {
      const repository = InMemoryPlaceSearchRepository(places: places);

      final results = await repository.search('');

      expect(results, places);
    });

    test('filters places using name, location, and category', () async {
      const repository = InMemoryPlaceSearchRepository(places: places);

      expect(await repository.search('buna'), <Place>[places.first]);
      expect(await repository.search('menelik'), <Place>[places.last]);
      expect(await repository.search('park'), <Place>[places.last]);
    });
  });
}
