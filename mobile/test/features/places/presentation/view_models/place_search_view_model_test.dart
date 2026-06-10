import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/src/features/places/domain/entities/place.dart';
import 'package:mobile/src/features/places/domain/repositories/place_search_repository.dart';
import 'package:mobile/src/features/places/domain/use_cases/search_places.dart';
import 'package:mobile/src/features/places/presentation/view_models/place_search_view_model.dart';

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
  ];

  group('PlaceSearchViewModel', () {
    test('loads results and exposes loading state', () async {
      final viewModel = PlaceSearchViewModel(
        searchPlaces: SearchPlaces(_FakeSearchRepository(results: places)),
      );
      final loadingStates = <bool>[];
      viewModel.addListener(() => loadingStates.add(viewModel.isSearching));

      await viewModel.loadInitialResults();

      expect(viewModel.results, places);
      expect(viewModel.errorMessage, isNull);
      expect(loadingStates, <bool>[true, false]);
    });

    test('stores query and error when search fails', () async {
      final viewModel = PlaceSearchViewModel(
        searchPlaces: SearchPlaces(_FakeSearchRepository(throwsError: true)),
      );

      await viewModel.updateQuery('bole');

      expect(viewModel.query, 'bole');
      expect(viewModel.results, isEmpty);
      expect(viewModel.errorMessage, 'Unable to search places right now.');
    });
  });
}

class _FakeSearchRepository implements PlaceSearchRepository {
  _FakeSearchRepository({
    this.results = const <Place>[],
    this.throwsError = false,
  });

  final List<Place> results;
  final bool throwsError;

  @override
  Future<List<Place>> search(String query) async {
    if (throwsError) {
      throw Exception('Search failed');
    }

    return results;
  }
}
