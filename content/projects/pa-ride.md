---
title: Pa-Ride
format: page
tags: React Native (Expo Router) · TypeScript · Supabase (Postgres, PostGIS, Realtime, Auth) · Self-directed
cardTags: React Native · TypeScript · Supabase (Postgres, PostGIS)
summary: A carpool marketplace for the Philippines, positioned as cost-sharing to stay outside ride-hailing regulation. I took it from a one-line idea to a PostGIS corridor-matching algorithm.
demoUrl: https://carpool-app-959816621001.australia-southeast2.run.app/?demo=driver
demoLabel: Try the live demo →
demoNote: ''
featured: true
visible: true
order: 1
---
## The problem

Carpooling already happens across the Philippines, just informally. Someone posts a route in a Facebook group, others reply, and it all gets sorted out over Messenger. It works, but it only reaches whoever happens to see the post, and the formal ride-hailing-style products (BlaBlaCar included) haven't gained much traction there.

Someone floated "a carpool app for the Philippines" as a one-line pitch, and I picked it up from there. Whether it was worth building, what shape it should take and all of the technical work were mine.

## What I did

I started with research instead of code. I wanted to know how carpooling works informally right now, and why the formal products that tried this didn't stick. Seeing that the informal version already works, my question became how to build on it instead of replacing it. That led to the biggest product decision: positioning Pa-Ride as **cost-sharing rather than ride-hailing**, which keeps it outside LTFRB/TNVS regulation. That call runs through the whole product, from the pricing model to the copy to the app suggesting a price but never setting a fare.

- A 26-migration Postgres schema as the data model, designed from a spec I wrote myself
- A PostGIS corridor-matching algorithm. Riders match with drivers going to their destination, and also with drivers who are already passing near their route, with a computed detour cost and a suggested price
- Seat booking and proposal negotiation as concurrency-safe Postgres functions with row-level locking, so seats can't be oversold or bypassed by a compromised client
- Auto-generated shareable trip cards and public trip pages that crawlers can read. A driver's Facebook-group post keeps working, and the link pulls new people into the app
- A data pipeline that joins several open Philippine geographic datasets to seed nationwide place search, which meant untangling renamed provinces, duplicate city names and missing coordinates

I used Claude Code and Claude Design throughout, including a project-specific Claude Skill that checks new UI code against the app's own design-system docs.

## Status

I'm a few weeks into building it and it's pre-launch, so there are no outside users yet. The core flows (post a trip, search, propose, confirm, recurring trips) are built and verified on desktop (macOS/Windows) and iOS Safari, but not yet as a compiled native iOS/Android app.
