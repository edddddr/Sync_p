# Search Feature: Places and Locations

This feature lets users search the local place catalog by place name, address,
or category. The current implementation uses in-memory sample data so the
mobile app can move independently before the Django API is ready.

## Flow

1. `PlaceSearchScreen` captures text from the search field.
2. `PlaceSearchViewModel` stores query, loading state, results, and errors.
3. `SearchPlaces` executes the search use case.
4. `PlaceSearchRepository` defines what search must provide.
5. `InMemoryPlaceSearchRepository` searches the local `samplePlaces` list.
6. `PlaceSearchMatcher` decides whether a place matches each query term.
7. Selecting a result navigates to `PlaceDetailsScreen`.

## Maintenance Notes

When the backend is ready, replace `InMemoryPlaceSearchRepository` with an API
repository that implements `PlaceSearchRepository`. The ViewModel and screen
should not need to change because they already depend on the domain contract.
