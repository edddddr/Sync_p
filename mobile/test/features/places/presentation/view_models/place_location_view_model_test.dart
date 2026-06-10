import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/src/features/places/domain/entities/place.dart';
import 'package:mobile/src/features/places/domain/repositories/place_map_repository.dart';
import 'package:mobile/src/features/places/domain/use_cases/open_place_in_maps.dart';
import 'package:mobile/src/features/places/presentation/view_models/place_location_view_model.dart';

void main() {
  const place = Place(
    id: 'buna-bistro',
    name: 'Buna Bistro',
    category: PlaceCategory.cafe,
    address: 'Bole Road, Addis Ababa',
    latitude: 9.005401,
    longitude: 38.763611,
  );

  group('PlaceLocationViewModel', () {
    test('opens a place and exposes loading state', () async {
      final repository = _FakePlaceMapRepository(openResult: true);
      final viewModel = PlaceLocationViewModel(
        openPlaceInMaps: OpenPlaceInMaps(repository),
      );
      final loadingStates = <bool>[];
      viewModel.addListener(() => loadingStates.add(viewModel.isOpening));

      await viewModel.openInMaps(place);

      expect(repository.openCallCount, 1);
      expect(viewModel.isOpening, isFalse);
      expect(viewModel.errorMessage, isNull);
      expect(loadingStates, <bool>[true, false]);
    });

    test('stores an error when maps cannot be opened', () async {
      final repository = _FakePlaceMapRepository(openResult: false);
      final viewModel = PlaceLocationViewModel(
        openPlaceInMaps: OpenPlaceInMaps(repository),
      );

      await viewModel.openInMaps(place);

      expect(repository.openCallCount, 1);
      expect(viewModel.isOpening, isFalse);
      expect(viewModel.errorMessage, 'Google Maps could not be opened.');
    });
  });
}

class _FakePlaceMapRepository implements PlaceMapRepository {
  _FakePlaceMapRepository({required this.openResult});

  final bool openResult;
  int openCallCount = 0;

  @override
  Future<bool> openInMaps(Place place) async {
    openCallCount += 1;
    return openResult;
  }
}
