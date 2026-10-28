---
title: Realtime Queue Management System
format: page
tags: React 18 · TypeScript · Meteor (Node.js) · MongoDB · Docker · Google Cloud · Reviewed by others
cardTags: React · Meteor · MongoDB · Docker · Google Cloud
summary: Waiting is a big part of life in the Philippines. I built a queue system that tells people where they stand and roughly when it's their turn.
demoUrl: lab/queue-demo/
demoLabel: Try the live demo →
demoNote: (seeded with demo data)
screenshotKind: web
cardImages:
  - image: assets/uploads/queue-system-1.webp
    alt: Staff dashboard for a dentistry clinic's queue, showing two patients waiting with their estimated wait times
featured: true
visible: true
order: 2
---
## Why this one

It started with my brother. He'd waited hours for his turn at one of the biggest hospitals in the Philippines, and all he wanted was some information. We started talking about a fix straight away.

The story was the spark, though. I grew up in the Philippines and I've been through that same wait, like every other Filipino. Now that I had the means to do something about it, I felt compelled to.

A lot of life there is waiting: in traffic, in a queue, for your turn, for a service to finish. I thought information could make a real difference to people's quality of life and let them get on with living it, which is why I wanted to take this one on.

## How waiting works now

You go there, sit, and wait until you're called. It's crowded and slow, and until your turn comes you have no idea where you stand. Some places have a screen. Visa services show which ID is next, but that's as far as the information goes, and it's one number for the whole room.

I thought people could have information specific to themselves: where they are in line, and roughly when it'll be their turn.

## The reasons that shaped it

**So people can just know.** The public queue page is the biggest reason. You join from your phone with no account to make, and you can see where you stand and how long you're likely to wait, without having to ask anyone.

<div class="shots">
  <figure>
    <img src="assets/uploads/queue-system-join.webp" alt="The public queue join screen for a dentistry clinic, with a name field, three services to pick from and a Prefer a specific provider option">
    <figcaption>Joining takes a name and what you need, with the option to ask for a provider you know.</figcaption>
  </figure>
  <figure>
    <img src="assets/uploads/queue-system-status.webp" alt="A patient's queue status screen showing their number, DEN-05, their position in line as third with two people ahead, and an estimated wait of 24 minutes">
    <figcaption>Your number, your place in line and your estimated wait.</figcaption>
  </figure>
</div>

**Filipinos trust someone they know.** When you join, you can ask for a specific provider, and the wait estimate counts that person's line, not whoever is quickest. Most people would rather go with a person they know, so the estimate has to be about that choice.

**Low bandwidth, phone first.** Mobile phone ownership in the Philippines is high compared to income, so the phone is the screen most people have, and connections aren't always strong. It's designed for the phone first and kept light.

**It has to feel responsive.** Phones there tend to be older or less powerful, so a slow tap feels broken. The screen updates as soon as you tap, and if the server says no, it rolls back with a warning.

**Any queue, not just hospitals.** A few months in, I noticed the same problem and the same fix applied to any organisation running a queue. So the platform supports companies and facilities with role-scoped staff, not a healthcare-only tool. My family and friends helped me talk it through, but a lot of it comes from growing up there. The project is a culmination of that.

<div class="shots shots-wide">
  <figure>
    <img src="assets/uploads/queue-system-1.webp" alt="Staff dashboard for a dentistry clinic's queue, showing two patients waiting with their estimated wait times">
    <figcaption>The staff side: a clinic's queue, with each patient's estimated wait.</figcaption>
  </figure>
</div>

## Status

Deployed to Google Cloud as a dev/staging environment. It isn't in use by a clinic or organisation yet. I built most of it myself, with input and review from others along the way.

It's React 18 and TypeScript on Meteor with MongoDB, in Docker on Google Cloud, with 180+ tests running on every pull request.
