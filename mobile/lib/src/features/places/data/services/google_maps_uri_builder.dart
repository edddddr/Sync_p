import '../../domain/entities/place.dart';

class GoogleMapsUriBuilder {
  const GoogleMapsUriBuilder();

  Uri buildPlaceSearchUri(Place place) {
    return Uri.https('www.google.com', '/maps/search/', <String, String>{
      'api': '1',
      'query': _coordinateQuery(place),
    });
  }

  String _coordinateQuery(Place place) {
    return '${_formatCoordinate(place.latitude)},${_formatCoordinate(place.longitude)}';
  }

  String _formatCoordinate(double coordinate) {
    return coordinate.toStringAsFixed(6);
  }
}
