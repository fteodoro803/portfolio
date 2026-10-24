---
title: Melbourne Public Transport Widget
format: page
tags: Flutter (iOS/Android/macOS/Windows/Linux) · Python (Flask) · WidgetKit/SwiftUI · GTFS Realtime · Built with a collaborator
cardTags: Flutter · Flask · WidgetKit/SwiftUI · GTFS Realtime
summary: A saved route on your phone's home screen, so you can see when your tram is coming without opening an app. Built with Nicole Penrose.
demoUrl: ''
demoLabel: Try the live demo →
demoNote: ''
screenshotKind: phone
cardImages:
  - image: assets/uploads/transport-widget-1.webp
    alt: The app showing tram route 96 at Russell St/Bourke St on a map, with upcoming departures listed below
  - image: assets/uploads/transport-widget-2.webp
    alt: The Saved Routes screen listing a route 96 tram with its next two departure times
  - image: assets/uploads/transport-widget-3.webp
    alt: Map search around Melbourne's CBD with nearby stops and a list of transport types to filter by
featured: true
visible: true
order: 3
---
## Why this one

Getting home took one step too many. To find out when my tram would reach me, I had to open the PTV app or Google Maps, look up my route, and check. It was my own commute, and I'd guess it's one everyone who commutes goes through. A saved route sitting on the home screen as a widget looked like it would make that really easy.

It was my idea first. I was also fresh out of university and wanted to try making a proper app. Nicole Penrose and I had worked on a university project before, and we were both out of uni, so we figured we might as well learn new things together. Building something in the real world would get us more job ready than more study and coursework.

## How checking transport works now

Most transport apps start from a search. You open the app, find your stop, drill down to your route, and only then see the next departure. For someone who takes the same tram home every day, that's the same few taps every time.

## The reasons that shaped it

**The home screen widget.** This is the point of the whole app. If your route is on the home screen, "when's my tram?" takes no taps at all. Nicole and I built the iOS widget together, start to finish.

**Saved routes.** A regular commuter already knows their routes, so you save them once and see live departures for just those. The backend I built combines PTV's timetable and live feeds so the app can show both in one place.

<div class="shots">
  <figure>
    <img src="assets/uploads/transport-widget-2.webp" alt="The Saved Routes screen listing a route 96 tram with its next two departure times">
    <figcaption>Routes you save once, with the next departures for each.</figcaption>
  </figure>
  <figure>
    <img src="assets/uploads/transport-widget-1.webp" alt="The app showing tram route 96 at Russell St/Bourke St on a map, with upcoming departures listed below">
    <figcaption>One route on the map, with the departures below.</figcaption>
  </figure>
</div>

**Accessibility, and what we learned at industry events.** We went to industry events and learned from the people there: accessibility, but also general app design, features we could use, and feedback on what we'd built. PTV's accessibility data shows up in the app and the widget, and we kept the interface simple enough for someone who finds most apps overwhelming.

## Status

Paused since December 2025. Down the line I'm planning to port it to React Native and modernise it.

The current version was self-tested only, with no public App Store/Play Store release and no usage numbers to cite. I checked departure times against Google Maps and they matched. The home-screen widget, which is the point of the project, shipped for iOS only. There's no Android equivalent, even though the rest of the app is cross-platform.

It's built in Flutter, so one codebase works on iOS and Android (macOS, Windows and Linux builds work too), with a Flask backend on MongoDB on Cloud Run.
