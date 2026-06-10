# Location Feature: Google Maps Redirect

This feature opens the selected place in Google Maps from the place details
screen. It is intentionally small, but it follows the same MVVM shape future
features should use.

## Flow

1. `PlaceDetailsScreen` renders the place and the button.
2. `PlaceLocationViewModel` owns UI state: loading and error text.
3. `OpenPlaceInMaps` contains the business action.
4. `PlaceMapRepository` hides the external map implementation from the domain.
5. `UrlLauncherPlaceMapRepository` uses `url_launcher` to open the generated URL.
6. `GoogleMapsUriBuilder` turns a `Place` into a Google Maps URL.

## Why this shape matters

The presentation layer can change without touching the map-launching code. The
data layer can switch from Google Maps URLs to a native maps SDK without
rewriting the screen. The domain layer stays small and testable, which is the
part you want to trust when maintaining the app later.
