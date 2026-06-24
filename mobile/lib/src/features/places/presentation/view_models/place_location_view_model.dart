import 'package:flutter/foundation.dart';

import '../../domain/entities/place.dart';
import '../../domain/use_cases/open_place_in_maps.dart';

class PlaceLocationViewModel extends ChangeNotifier {
  PlaceLocationViewModel({required OpenPlaceInMaps openPlaceInMaps})
    : _openPlaceInMaps = openPlaceInMaps;

  final OpenPlaceInMaps _openPlaceInMaps;

  bool _isOpening = false;
  String? _errorMessage;

  bool get isOpening => _isOpening;
  String? get errorMessage => _errorMessage;

  Future<void> openInMaps(Place place) async {
    if (_isOpening) {
      return;
    }

    _isOpening = true;
    _errorMessage = null;
    notifyListeners();

    try {
      await _openPlaceInMaps(place);
    } on MapLaunchFailure catch (error) {
      _errorMessage = error.message;
    } catch (_) {
      _errorMessage = 'Unable to open Google Maps right now.';
    } finally {
      _isOpening = false;
      notifyListeners();
    }
  }

  void clearError() {
    if (_errorMessage == null) {
      return;
    }

    _errorMessage = null;
    notifyListeners();
  }
}
