import '../../domain/entities/place.dart';

class PlaceSearchMatcher {
  const PlaceSearchMatcher();

  static final RegExp _whitespace = RegExp(r'\s+');

  bool matches(Place place, String query) {
    final normalizedQuery = _normalize(query);

    if (normalizedQuery.isEmpty) {
      return true;
    }

    final terms = normalizedQuery.split(_whitespace);
    final searchableText = _normalize(
      '${place.name} ${place.address} ${place.category.label}',
    );

    return terms.every((term) => searchableText.contains(term));
  }

  String _normalize(String value) {
    return value.trim().toLowerCase();
  }
}
