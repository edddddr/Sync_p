import '../../domain/entities/place.dart';
import '../../domain/repositories/place_search_repository.dart';
import '../services/place_search_matcher.dart';

class InMemoryPlaceSearchRepository implements PlaceSearchRepository {
  const InMemoryPlaceSearchRepository({
    required List<Place> places,
    PlaceSearchMatcher matcher = const PlaceSearchMatcher(),
  }) : _places = places,
       _matcher = matcher;

  final List<Place> _places;
  final PlaceSearchMatcher _matcher;

  @override
  Future<List<Place>> search(String query) async {
    return _places.where((place) => _matcher.matches(place, query)).toList();
  }
}
