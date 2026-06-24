import '../entities/place.dart';

abstract class PlaceSearchRepository {
  Future<List<Place>> search(String query);
}
