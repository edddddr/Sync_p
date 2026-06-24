import '../entities/place.dart';

abstract class PlaceMapRepository {
  Future<bool> openInMaps(Place place);
}
