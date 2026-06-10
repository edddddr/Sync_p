import 'package:flutter/foundation.dart';

import '../../domain/entities/place.dart';
import '../../domain/use_cases/search_places.dart';

class PlaceSearchViewModel extends ChangeNotifier {
  PlaceSearchViewModel({required SearchPlaces searchPlaces})
    : _searchPlaces = searchPlaces;

  final SearchPlaces _searchPlaces;

  String _query = '';
  List<Place> _results = <Place>[];
  bool _isSearching = false;
  String? _errorMessage;
  int _searchRequestId = 0;

  String get query => _query;
  List<Place> get results => List.unmodifiable(_results);
  bool get isSearching => _isSearching;
  String? get errorMessage => _errorMessage;
  bool get hasQuery => _query.trim().isNotEmpty;

  Future<void> loadInitialResults() {
    return _runSearch(_query);
  }

  Future<void> updateQuery(String query) async {
    if (query == _query) {
      return;
    }

    _query = query;
    await _runSearch(query);
  }

  Future<void> clearSearch() async {
    if (_query.isEmpty) {
      return;
    }

    _query = '';
    await _runSearch(_query);
  }

  Future<void> _runSearch(String query) async {
    final requestId = ++_searchRequestId;
    _isSearching = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final places = await _searchPlaces(query);

      if (requestId != _searchRequestId) {
        return;
      }

      _results = places;
    } catch (_) {
      if (requestId != _searchRequestId) {
        return;
      }

      _results = <Place>[];
      _errorMessage = 'Unable to search places right now.';
    } finally {
      if (requestId == _searchRequestId) {
        _isSearching = false;
        notifyListeners();
      }
    }
  }
}
