---
title: Pa-Ride
format: page
tags: React Native (Expo Router) · TypeScript · Supabase (Postgres, PostGIS, Realtime, Auth) · Self-directed
cardTags: React Native · TypeScript · Supabase (Postgres, PostGIS)
summary: Filipinos already carpool through Facebook groups. Pa-Ride keeps what works about that and fixes the rest.
demoUrl: https://carpool-app-959816621001.australia-southeast2.run.app/
demoLabel: Try the live demo →
demoNote: ''
screenshotKind: phone
cardImages:
  - image: assets/uploads/pa-ride-search.webp
    alt: The Pa-Ride search screen with a "Where are you headed?" bar, saved route chips, a list and map toggle, and trip cards showing the driver, route, seats left and price per seat
  - image: assets/uploads/pa-ride-trip-page.webp
    alt: A trip page as a rider sees it, with the departure time, route, driver profile and stats, price per seat, seats left and a Request a seat button
  - image: assets/uploads/pa-ride-proposal.webp
    alt: The Request a seat form, filled in with one seat, a pickup point, an offer of 180 pesos per seat and a short baggage note
  - image: assets/uploads/pa-ride-live-sheet.webp
    alt: Live trip tracking with the bottom sheet open, showing how many minutes away the driver is, the driver and a Message button, and the vehicle's plate
  - image: assets/uploads/pa-ride-live-map.webp
    alt: Live trip tracking on a map of Metro Manila, with the driver's position and route and a bottom sheet showing the rider's pickup and time away
featured: true
visible: true
order: 1
---
## Why this one

A friend floated a one-line pitch: a carpool app for the Philippines. I liked the idea of working with him, so I took it a lot further than a pitch usually goes.

I also like fixing things so they're easier for people, and carpooling in the Philippines has a lot of steps and a lot of places for things to go wrong. Most of them looked fixable to me.

## How carpooling works now

It already happens, just on Facebook. Every area has its own group. A driver posts a trip, usually as a picture, riders comment, and then everyone moves to a messaging app to sort out the rest.

I read through the groups, talked to people, and read up on why the formal apps hadn't taken off. The same four problems kept coming up. It's scattered, with a different group for every area. It's hard to trust anyone you haven't dealt with before. Your number and identity go to everyone who replies. And it's messy: no search, no clear seat count, and no way to tell if a post is still open.

BlaBlaCar works well in other countries, but here it never got into the community or the way Filipinos already do things, so it had no drivers and no riders.

## Keep what works, fix the rest

Since people already do this and it mostly works, I didn't want to replace it. I wanted to take away the reasons not to use it, one Facebook habit at a time.

**Nothing to install.** Everyone has Facebook, so Pa-Ride is just a website. You don't need an account to look at a trip, and you sign up when you do something, like asking for a seat.

**Posting is a form.** Everyone knows how to post in a group, so a driver fills in a form instead. Every trip then has a clear seat count and price, which a picture in a group never does.

**Trust comes from a record, not mutual friends.** On Facebook you can see a profile and your mutual friends. Here it's a verified phone number and a trip record, and every trip ends with a recorded outcome, so the record keeps growing.

**Negotiation has one shape.** Facebook messaging is free-flow, so everyone does it their own way. In Pa-Ride a rider proposes a price, the driver counters or accepts, and both sides have it recorded. When it's agreed, the seat is locked, so one seat can't be promised to two people.

<div class="shots">
  <figure>
    <img src="assets/uploads/pa-ride-search.webp" alt="The Pa-Ride search screen, with trip cards showing the driver, route, seats left and price per seat">
    <figcaption>Every trip in one place, with seats left and price per seat.</figcaption>
  </figure>
  <figure>
    <img src="assets/uploads/pa-ride-proposal.webp" alt="The Request a seat form, filled in with one seat, a pickup point, an offer of 180 pesos per seat and a short baggage note">
    <figcaption>A rider proposes a price, and the driver counters or accepts.</figcaption>
  </figure>
</div>

**Cost-sharing, not ride-hailing.** The app suggests a price and never sets a fare. That keeps Pa-Ride a way to split costs, outside LTFRB and TNVS regulation, and it shapes the pricing and the copy.

**Matching on the route, not just the destination.** Riders also see drivers who are already passing near them, with the detour it would cost and a suggested price. That idea came from my friend, and we worked it out together.

## Transition, not replacement

Drivers keep posting where they do today. Every trip becomes a share card with a QR code and a link, ready to post in a Facebook group. Whoever sees it lands on the trip page without an account: post, scan, view, join. The more people use it, the more it sustains itself.

<div class="shots">
  <figure>
    <img src="assets/uploads/pa-ride-share-card.webp" alt="A Pa-Ride share card for a Muntinlupa to Quezon City trip, showing the date, departure time, price per seat, seats, the driver and a QR code">
    <figcaption>The card a driver posts in a Facebook group.</figcaption>
  </figure>
  <figure>
    <img src="assets/uploads/pa-ride-trip-page.webp" alt="A trip page as a rider sees it, with the departure time, route, driver profile, price per seat, seats left and a Request a seat button">
    <figcaption>Where the QR code lands, no account needed.</figcaption>
  </figure>
</div>

It also needed a name people say out loud and a friendly, playful design, since it's meant to feel like something you'd mention to a friend.

## Status

I'm a few weeks into building it and it's pre-launch, so there are no outside users yet. The core flows (post a trip, search, propose, confirm, recurring trips) are built and verified on desktop (macOS/Windows) and iOS Safari, but not yet as a compiled native iOS/Android app.

It's built with React Native (Expo Router) and TypeScript on Supabase, with Postgres and PostGIS doing the route matching. I used Claude Code and Claude Design throughout.
