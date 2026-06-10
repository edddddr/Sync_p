import '../entities/place.dart';
import '../repositories/place_map_repository.dart';

class OpenPlaceInMaps {
  const OpenPlaceInMaps(this._repository);

  final PlaceMapRepository _repository;

  Future<void> call(Place place) async {
    final wasOpened = await _repository.openInMaps(place);

    if (!wasOpened) {
      throw const MapLaunchFailure('Google Maps could not be opened.');
    }
  }
}

class MapLaunchFailure implements Exception {
  const MapLaunchFailure(this.message);

  final String message;
}
