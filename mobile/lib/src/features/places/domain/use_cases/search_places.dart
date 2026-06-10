import '../entities/place.dart';
import '../repositories/place_search_repository.dart';

class SearchPlaces {
  const SearchPlaces(this._repository);

  final PlaceSearchRepository _repository;

  Future<List<Place>> call(String query) {
    return _repository.search(query.trim());
  }
}
