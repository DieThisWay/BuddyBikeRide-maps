# BuddyBikeRide maps

Off-road map files for the BuddyBikeRide app: dirt roads, tracks, trails and fords for each country, visible from far zoom levels and usable without internet.

- `countries.json` lists the countries. Add one with its Geofabrik path to have it built.
- `offroad.yml` is the [Planetiler](https://github.com/onthegomap/planetiler) schema.
- The `Build country maps` workflow rebuilds every country once a month and publishes the files and `manifest.json` as the latest release.
- `download-style-v1.json` is the style the app downloads offline base maps with: OpenFreeMap tiles at the fixed `planet/latest` address, with the same fonts and icons as the map. The monthly build warns if OpenFreeMap's icons or fonts move. The app keeps the copy it downloaded with, so a changed file needs a new name (v2) and a matching change in the app.

Map data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), available under the Open Database License (ODbL).
