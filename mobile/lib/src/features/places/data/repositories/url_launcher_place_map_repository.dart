import 'package:url_launcher/url_launcher.dart';

import '../../domain/entities/place.dart';
import '../../domain/repositories/place_map_repository.dart';
import '../services/google_maps_uri_builder.dart';

typedef UrlLauncher = Future<bool> Function(Uri url, {LaunchMode mode});

class UrlLauncherPlaceMapRepository implements PlaceMapRepository {
  UrlLauncherPlaceMapRepository({
    GoogleMapsUriBuilder uriBuilder = const GoogleMapsUriBuilder(),
    UrlLauncher? launcher,
  }) : _uriBuilder = uriBuilder,
       _launcher = launcher ?? launchUrl;

  final GoogleMapsUriBuilder _uriBuilder;
  final UrlLauncher _launcher;

  @override
  Future<bool> openInMaps(Place place) {
    final mapsUri = _uriBuilder.buildPlaceSearchUri(place);
    return _launcher(mapsUri, mode: LaunchMode.externalApplication);
  }
}
