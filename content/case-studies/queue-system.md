---
title: Realtime Queue Management System
tags: React 18 · TypeScript · Meteor (Node.js) · MongoDB · Docker · Google Cloud · Solo build, reviewed by others
cardTags: React · Meteor · MongoDB · Docker · Google Cloud
summary: Started from my brother's story about hospital wait times in the Philippines — grew into a multi-tenant RBAC platform any organisation running a queue can use.
demoUrl: https://queue-system-322182421963.australia-southeast2.run.app/
demoLabel: Try the live demo →
demoNote: (seeded with demo data)
featured: true
visible: false
order: 2
---
## The problem

This one started as a one-line story, not a spec. My brother described waiting hours for his turn at one of the biggest hospitals in the Philippines — no real system behind it, just "when is it my turn?" I started designing specifically for that: the healthcare wait-time problem, because it's one of the more visible, painful gaps I could point to back home. A few months in, it became clear the same problem — and the same fix — applied to any organisation running a queue, not just hospitals. That's the actual reason the platform ended up supporting arbitrary companies and facilities with role-scoped staff, rather than a healthcare-specific tool: it's where the problem itself led, not a scope decision made up front.

## What I did

- Architected the multi-tenant RBAC platform that resulted: companies, facilities, and role-scoped staff memberships, with a permission engine, an invitation flow, and audit logging — spanning 74 Meteor methods and 35 real-time publications
- Found that the wait-time calculation had drifted into three inconsistent implementations — hand-duplicated across contexts that couldn't share the same code path — and replaced them with one shared formula in a single pass, fixing incorrect displays and closing a cross-facility data leak
- Designed the UI mobile-first and low-bandwidth-optimised — a deliberate call given how disproportionately high mobile phone ownership is in the Philippines relative to population and economic status — with role-based navigation split across staff and patient flows
- Used Meteor's optimistic UI methods so actions feel instant on weaker mobile connections, rolling back with a warning only if the server call actually fails
- Built live-reformatting, validated phone number inputs for Philippine mobile numbers, with dedicated test coverage — so a user doesn't need to already know the expected format to get it right
- Grew the test suite to 180+ unit and integration tests (Mocha/Chai), running automatically via GitHub Actions CI on every pull request
- Containerised with Docker and deployed to Google Cloud, personally diagnosing discrepancies between local and staging builds when a deploy didn't behave as expected

> Next planned step, not yet built: mobile number verification via Twilio as part of patient sign-in, a direct extension of the mobile-first reasoning above.

## Status

Deployed to Google Cloud as a dev/staging environment. Not yet in use by a real clinic or organisation — built mostly solo, with input and review from others along the way.
