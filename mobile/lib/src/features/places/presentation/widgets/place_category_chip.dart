import 'package:flutter/material.dart';

import '../../domain/entities/place.dart';

class PlaceCategoryChip extends StatelessWidget {
  const PlaceCategoryChip({super.key, required this.category});

  final PlaceCategory category;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return DecoratedBox(
      decoration: BoxDecoration(
        color: colorScheme.secondaryContainer,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(_icon, size: 16, color: colorScheme.onSecondaryContainer),
            const SizedBox(width: 6),
            Text(
              category.label,
              style: TextStyle(
                color: colorScheme.onSecondaryContainer,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }

  IconData get _icon {
    return switch (category) {
      PlaceCategory.cafe => Icons.local_cafe_outlined,
      PlaceCategory.restaurant => Icons.restaurant_outlined,
      PlaceCategory.park => Icons.park_outlined,
    };
  }
}
