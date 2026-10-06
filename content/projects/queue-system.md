---
title: Realtime Queue Management System
format: page
tags: React 18 · TypeScript · Meteor (Node.js) · MongoDB · Docker · Google Cloud · Reviewed by others
cardTags: React · Meteor · MongoDB · Docker · Google Cloud
summary: Started from my brother's story about hospital wait times in the Philippines. It grew into a multi-tenant RBAC platform that any organisation running a queue can use.
demoUrl: https://queue-demo-322182421963.australia-southeast2.run.app/
demoLabel: Try the live demo →
demoNote: (seeded with demo data)
featured: true
visible: true
order: 2
---
## The problem

This one started as a story, not a spec. My brother told me about waiting hours for his turn at one of the biggest hospitals in the Philippines, with no system behind it, just a lot of "when is it my turn?" That stuck with me, so I started designing for it. Hospital wait times are one of the more visible and painful gaps I could point to back home.

A few months in, I noticed the same problem and the same fix applied to any organisation running a queue, not just hospitals. That's why the platform supports any company and facility with role-scoped staff, instead of being a healthcare-only tool. The problem led there, I didn't plan it up front.

## What I did

- Architected the multi-tenant RBAC platform that came out of that: companies, facilities and role-scoped staff memberships, with a permission engine, an invitation flow and audit logging. It spans 74 Meteor methods and 35 real-time publications
- Found that the wait-time calculation had drifted into three different implementations, copied by hand across places that couldn't share a code path. I replaced them with one shared formula in a single pass, which fixed incorrect displays and closed a cross-facility data leak
- Designed the UI mobile-first and for low bandwidth, since mobile phone ownership in the Philippines is high compared to income, with role-based navigation split across staff and patient flows
- Used Meteor's optimistic UI methods so actions feel instant on weaker mobile connections, rolling back with a warning if the server call fails
- Built phone number inputs for Philippine mobile numbers that reformat as you type and validate, with their own tests, so nobody needs to know the expected format up front
- Grew the test suite to 180+ unit and integration tests (Mocha/Chai), run by GitHub Actions on every pull request
- Containerised it with Docker and deployed to Google Cloud. When a deploy didn't behave like my local build, I tracked down the differences between local and staging myself

## Status

Deployed to Google Cloud as a dev/staging environment. It isn't in use by a clinic or organisation yet. I built most of it myself, with input and review from others along the way.
