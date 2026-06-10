import 'package:flutter/material.dart';

import '../../domain/entities/place.dart';
import '../view_models/place_search_view_model.dart';
import '../widgets/place_search_result_card.dart';

typedef PlaceSelectedCallback =
    void Function(BuildContext context, Place place);

class PlaceSearchScreen extends StatefulWidget {
  const PlaceSearchScreen({
    super.key,
    required this.searchViewModel,
    required this.onPlaceSelected,
  });

  final PlaceSearchViewModel searchViewModel;
  final PlaceSelectedCallback onPlaceSelected;

  @override
  State<PlaceSearchScreen> createState() => _PlaceSearchScreenState();
}

class _PlaceSearchScreenState extends State<PlaceSearchScreen> {
  late final TextEditingController _searchController;

  @override
  void initState() {
    super.initState();
    _searchController = TextEditingController(
      text: widget.searchViewModel.query,
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: ListenableBuilder(
            listenable: widget.searchViewModel,
            builder: (context, _) {
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Discover places',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  const SizedBox(height: 16),
                  _SearchField(
                    controller: _searchController,
                    hasQuery: widget.searchViewModel.hasQuery,
                    onChanged: (query) {
                      widget.searchViewModel.updateQuery(query);
                    },
                    onClear: () {
                      _searchController.clear();
                      widget.searchViewModel.clearSearch();
                    },
                  ),
                  const SizedBox(height: 12),
                  if (widget.searchViewModel.isSearching)
                    const LinearProgressIndicator(minHeight: 2)
                  else
                    const SizedBox(height: 2),
                  const SizedBox(height: 16),
                  Expanded(
                    child: _SearchResults(
                      results: widget.searchViewModel.results,
                      errorMessage: widget.searchViewModel.errorMessage,
                      onPlaceSelected: widget.onPlaceSelected,
                    ),
                  ),
                ],
              );
            },
          ),
        ),
      ),
    );
  }
}

class _SearchField extends StatelessWidget {
  const _SearchField({
    required this.controller,
    required this.hasQuery,
    required this.onChanged,
    required this.onClear,
  });

  final TextEditingController controller;
  final bool hasQuery;
  final ValueChanged<String> onChanged;
  final VoidCallback onClear;

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      onChanged: onChanged,
      textInputAction: TextInputAction.search,
      decoration: InputDecoration(
        hintText: 'Search places or locations',
        prefixIcon: const Icon(Icons.search),
        suffixIcon: hasQuery
            ? IconButton(
                tooltip: 'Clear search',
                onPressed: onClear,
                icon: const Icon(Icons.close),
              )
            : null,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
      ),
    );
  }
}

class _SearchResults extends StatelessWidget {
  const _SearchResults({
    required this.results,
    required this.errorMessage,
    required this.onPlaceSelected,
  });

  final List<Place> results;
  final String? errorMessage;
  final PlaceSelectedCallback onPlaceSelected;

  @override
  Widget build(BuildContext context) {
    if (errorMessage != null) {
      return _SearchMessage(
        icon: Icons.error_outline,
        title: errorMessage!,
        subtitle: 'Please try again in a moment.',
      );
    }

    if (results.isEmpty) {
      return const _SearchMessage(
        icon: Icons.travel_explore,
        title: 'No places found',
        subtitle: 'Try another place name, category, or location.',
      );
    }

    return ListView.separated(
      itemCount: results.length,
      separatorBuilder: (context, index) => const SizedBox(height: 12),
      itemBuilder: (context, index) {
        final place = results[index];

        return PlaceSearchResultCard(
          place: place,
          onTap: () => onPlaceSelected(context, place),
        );
      },
    );
  }
}

class _SearchMessage extends StatelessWidget {
  const _SearchMessage({
    required this.icon,
    required this.title,
    required this.subtitle,
  });

  final IconData icon;
  final String title;
  final String subtitle;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 40, color: colorScheme.onSurfaceVariant),
          const SizedBox(height: 12),
          Text(
            title,
            style: Theme.of(
              context,
            ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 4),
          Text(
            subtitle,
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
              color: colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ),
    );
  }
}
