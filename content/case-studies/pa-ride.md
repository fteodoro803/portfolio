---
title: Pa-Ride
tags: React Native (Expo Router) · TypeScript · Supabase (Postgres, PostGIS, Realtime, Auth) · Solo, self-directed
cardTags: React Native · TypeScript · Supabase (Postgres, PostGIS)
summary: A carpool marketplace for the Philippines, positioned as cost-sharing to stay outside ride-hailing regulation — solo, from spec to a PostGIS corridor-matching algorithm.
demoUrl: https://carpool-app-959816621001.australia-southeast2.run.app/
demoLabel: Try the live demo →
demoNote: ''
featured: true
visible: true
order: 1
---
## The problem

Carpooling already happens informally across the Philippines through Facebook groups — people post a route, others reply, it's arranged over Messenger. It works, but it doesn't scale past whoever happens to see the post, and formal ride-hailing-style products (BlaBlaCar included) haven't gained real traction there.

Someone floated the idea of "a carpool app for the Philippines" as a one-line pitch. Everything past that — whether it was worth building, what shape it should take, and all of the technical work — was mine.

## What I did

I started with the research, not the build: how carpooling actually works informally right now, and specifically why the formal products that already tried this failed to stick. That research shaped a real product decision early — positioning Pa-Ride as **cost-sharing rather than ride-hailing**, which keeps it outside LTFRB/TNVS regulation in the Philippines. That call runs through the whole product: the pricing model, the copy, and the fact that the app only ever *suggests* a price, never sets a fare.

- A 26-migration Postgres schema as the data model, designed from a spec I wrote myself
- A PostGIS-based corridor-matching algorithm — riders match not only to drivers going to their exact destination, but to drivers already passing near their route, with a computed detour cost and dynamic suggested price
- Seat booking and proposal negotiation as concurrency-safe Postgres functions with row-level locking, so seat availability can't be oversold or bypassed by a compromised client
- A growth loop: auto-generated shareable trip cards and public, crawler-renderable trip pages, so a driver's existing Facebook-group post keeps working while a link pulls new users into the app
- A data pipeline joining multiple open Philippine geographic datasets to seed nationwide place search, resolving real conflicts (renamed provinces, duplicate city names, missing coordinates)

I used Claude Code and Claude Design throughout, including writing a project-specific Claude Skill that checks new UI code against the app's own design-system docs automatically.

> **A decision worth being upfront about:** the corridor-matching algorithm currently uses straight-line-distance approximation rather than a real routing service — a deliberate scope call for a solo, pre-launch build, not something missed.

## Status

A few weeks into a solo, pre-launch build. No outside users yet. Core flows — post a trip, search/propose/confirm, recurring trips — are built and verified across desktop (macOS/Windows) and iOS Safari, but not yet as a compiled native iOS/Android app.
