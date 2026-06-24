import 'package:flutter/material.dart';

import '../../domain/entities/place.dart';
import '../view_models/place_location_view_model.dart';
import '../widgets/place_category_chip.dart';

class PlaceDetailsScreen extends StatelessWidget {
  const PlaceDetailsScreen({
    super.key,
    required this.place,
    required this.locationViewModel,
  });

  final Place place;
  final PlaceLocationViewModel locationViewModel;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: ListenableBuilder(
          listenable: locationViewModel,
          builder: (context, _) {
            return SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _PlaceHeader(place: place),
                    const SizedBox(height: 24),
                    Text(
                      'Location',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      place.address,
                      style: Theme.of(context).textTheme.bodyLarge,
                    ),
                    const SizedBox(height: 16),
                    _OpenMapsButton(
                      isOpening: locationViewModel.isOpening,
                      onPressed: () => locationViewModel.openInMaps(place),
                    ),
                    if (locationViewModel.errorMessage != null) ...[
                      const SizedBox(height: 12),
                      _ErrorMessage(message: locationViewModel.errorMessage!),
                    ],
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class _PlaceHeader extends StatelessWidget {
  const _PlaceHeader({required this.place});

  final Place place;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return DecoratedBox(
      decoration: BoxDecoration(
        color: colorScheme.primaryContainer,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            PlaceCategoryChip(category: place.category),
            const SizedBox(height: 40),
            Icon(
              Icons.place_outlined,
              size: 44,
              color: colorScheme.onPrimaryContainer,
            ),
            const SizedBox(height: 16),
            Text(
              place.name,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                color: colorScheme.onPrimaryContainer,
                fontWeight: FontWeight.w800,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _OpenMapsButton extends StatelessWidget {
  const _OpenMapsButton({required this.isOpening, required this.onPressed});

  final bool isOpening;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      child: FilledButton.icon(
        onPressed: isOpening ? null : onPressed,
        icon: isOpening
            ? const SizedBox.square(
                dimension: 18,
                child: CircularProgressIndicator(strokeWidth: 2),
              )
            : const Icon(Icons.map_outlined),
        label: Text(
          isOpening ? 'Opening Google Maps...' : 'Open in Google Maps',
        ),
      ),
    );
  }
}

class _ErrorMessage extends StatelessWidget {
  const _ErrorMessage({required this.message});

  final String message;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return DecoratedBox(
      decoration: BoxDecoration(
        color: colorScheme.errorContainer,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            Icon(Icons.error_outline, color: colorScheme.onErrorContainer),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                message,
                style: TextStyle(color: colorScheme.onErrorContainer),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
