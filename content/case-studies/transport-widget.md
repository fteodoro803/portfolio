---
title: Melbourne Public Transport Widget
tags: Flutter (iOS/Android/macOS/Windows/Linux) · Python (Flask) · WidgetKit/SwiftUI · GTFS Realtime · Built with a collaborator
cardTags: Flutter · Flask · WidgetKit/SwiftUI · GTFS Realtime
summary: A personalised departure board on your phone's home screen, built with a collaborator. I implemented PTV's request-signing scheme from scratch to get there.
demoUrl: ''
demoLabel: Try the live demo →
demoNote: ''
featured: true
visible: true
order: 3
---
## The problem

A regular commuter already knows their routes, but most PT apps still make them search and drill down every time they want to know when the next tram or train is. The idea was a personalised departure board: save your regular routes once, then see live departures for just those, straight from your phone's home screen.

## What we did, and what I did

We chose Flutter to get one codebase across iOS and Android (macOS, Windows and Linux builds work too). The cross-platform options at the time didn't have a great alternative for a public release, and the app needed to work whichever phone someone had.

My work centred on the data layer and backend:

- Built the Flask backend on MongoDB, which scrapes PTV's GTFS schedule feed by parsing the open-data portal's HTML. It checks a CKAN API endpoint first, so the ~130MB dataset rebuild runs when the source data has changed
- Set up the Cloud Build pipeline that auto-deploys to Cloud Run on every merge, with Cloud Scheduler triggering it nightly, an hour after PTV's own data refresh
- Implemented PTV's HMAC-SHA1 request-signing scheme from scratch to authenticate with the Timetable API, and combined it with GTFS Realtime protobuf feeds so live and scheduled data sit in one model
- Designed the 14-table normalised local schema (Drift/SQLite) with a reusable, unit-tested merge-update helper, so the app serves cached transit data first and calls the PTV/GTFS APIs on a cache miss

Nicole Penrose and I built the iOS home-screen widget (WidgetKit/SwiftUI) together from start to finish. We also both worked on accessibility from the beginning, surfacing PTV's accessibility data in the app and the widget, and keeping the interface simple enough for someone who finds most apps overwhelming.

## Status

Paused since December 2025 while I port it over to React Native. I'm rebuilding it to be more modern, to make room for AI features, and to learn AWS and Terraform along the way.

The current version was self-tested only, with no public App Store/Play Store release and no usage numbers to cite. I checked departure times against Google Maps and they matched. The home-screen widget, which is the point of the project, shipped for iOS only. There's no Android equivalent, even though the rest of the app is cross-platform.
