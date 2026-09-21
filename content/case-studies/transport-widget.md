---
title: Melbourne Public Transport Widget
tags: Flutter (iOS/Android/macOS/Windows/Linux) · Python (Flask) · WidgetKit/SwiftUI · GTFS Realtime · Built with a collaborator
cardTags: Flutter · Flask · WidgetKit/SwiftUI · GTFS Realtime
summary: A personalised departure board on your phone's home screen, built with a collaborator — reverse-engineered PTV's request-signing scheme from scratch to get there.
demoUrl: ''
demoLabel: Try the live demo →
demoNote: ''
featured: true
visible: true
order: 3
---
> Built with Nicole Penrose through near-constant pair programming — not a clean feature split. This write-up says "we" where that's true.

## The problem

A regular commuter already knows their routes — but most PT apps still make them search and drill down every single time just to check when the next tram or train is. The idea was a personalised departure board: save your regular routes once, then see live departures for just those, straight from your phone's home screen.

## What we did, and what I did

We chose Flutter to ship one codebase across iOS and Android (macOS/Windows/Linux builds also work), at a time when the cross-platform tooling landscape didn't have a great alternative for a public release, and because the app needed to work regardless of which phone someone had.

My work centred on the data layer and backend:

- Built the Flask backend on MongoDB that scrapes PTV's GTFS schedule feed by parsing the open-data portal's HTML, cross-checking a CKAN API endpoint before reprocessing so a ~130MB dataset rebuild only runs when the source data has actually changed
- Set up the Cloud Build pipeline that auto-deploys to Cloud Run on every merge, triggered nightly via Cloud Scheduler timed deliberately for an hour after PTV's own data refresh
- Implemented PTV's HMAC-SHA1 request-signing scheme from scratch to authenticate against the Timetable API, combined with GTFS Realtime protobuf feeds so live and scheduled data sit in one model
- Designed the 14-table normalised local schema (Drift/SQLite) with a reusable, unit-tested merge-update helper, so the app serves cached transit data first and only calls the PTV/GTFS APIs on a cache miss

Nicole and I co-built the iOS home-screen widget (WidgetKit/SwiftUI) end-to-end together, and both worked on accessibility from the outset — surfacing PTV's own accessibility data in-app and in the widget, and keeping the interface simple enough for someone who finds most apps overwhelming.

## Status

Paused since December 2025. Self-tested only — no public App Store/Play Store release, no usage numbers to cite. Departure times were checked personally against Google Maps and matched. The home-screen widget — the actual point of the project — only ever shipped for iOS; there's no Android equivalent, even though the rest of the app is genuinely cross-platform.
