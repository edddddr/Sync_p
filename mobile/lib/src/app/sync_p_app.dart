import 'package:flutter/material.dart';

import '../features/places/data/repositories/in_memory_place_search_repository.dart';
import '../features/places/data/sample_places.dart';
import '../features/places/data/repositories/url_launcher_place_map_repository.dart';
import '../features/places/domain/entities/place.dart';
import '../features/places/domain/use_cases/open_place_in_maps.dart';
import '../features/places/domain/use_cases/search_places.dart';
import '../features/places/presentation/view_models/place_location_view_model.dart';
import '../features/places/presentation/view_models/place_search_view_model.dart';
import '../features/places/presentation/views/place_details_screen.dart';
import '../features/places/presentation/views/place_search_screen.dart';

class SyncPApp extends StatefulWidget {
  const SyncPApp({super.key});

  @override
  State<SyncPApp> createState() => _SyncPAppState();
}

class _SyncPAppState extends State<SyncPApp> {
  late final PlaceLocationViewModel _locationViewModel;
  late final PlaceSearchViewModel _searchViewModel;

  @override
  void initState() {
    super.initState();
    final mapRepository = UrlLauncherPlaceMapRepository();
    final openPlaceInMaps = OpenPlaceInMaps(mapRepository);
    final searchRepository = InMemoryPlaceSearchRepository(
      places: samplePlaces,
    );
    final searchPlaces = SearchPlaces(searchRepository);

    _locationViewModel = PlaceLocationViewModel(
      openPlaceInMaps: openPlaceInMaps,
    );
    _searchViewModel = PlaceSearchViewModel(searchPlaces: searchPlaces);
    _searchViewModel.loadInitialResults();
  }

  @override
  void dispose() {
    _searchViewModel.dispose();
    _locationViewModel.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'SyncP',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1F7A64)),
        useMaterial3: true,
      ),
      home: PlaceSearchScreen(
        searchViewModel: _searchViewModel,
        onPlaceSelected: _openPlaceDetails,
      ),
    );
  }

  void _openPlaceDetails(BuildContext context, Place place) {
    _locationViewModel.clearError();
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) {
          return PlaceDetailsScreen(
            place: place,
            locationViewModel: _locationViewModel,
          );
        },
      ),
    );
  }
}
