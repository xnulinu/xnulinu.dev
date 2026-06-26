---
title: The control plane is the product
date: 2026-07-01
summary: In autonomous systems, capability is becoming a commodity. The defensible problem is trusted execution — not diagnosis.
---

For most of my career the hard part of platform work was getting a system to *understand* state: read the metrics, correlate the logs, find the failing node. We built increasingly good diagnostic machinery, and we assumed that was where the value lived.

It isn't. Not anymore.

As models get more capable, diagnosis collapses toward a commodity. A model wired to your connectors can describe what broke and propose a fix in seconds. The thing that stays hard — the thing that actually gates whether any of this reaches production — is **action**.

## Reading is not acting

A system that reads can be wrong cheaply. A system that *acts* in production can be wrong catastrophically, at machine speed, without hesitation. So the engineering problem shifts entirely. It stops being "can it figure out the answer" and becomes:

- Can it only do what it's *scoped* to do?
- Is there a *blast radius* it cannot exceed?
- Is every action *reversible*?
- Is there a *gate* before anything irreversible?

None of that is intelligence. All of it is infrastructure.

## The shape that keeps recurring

Every dependable system I've built has the same spine: intent never reaches production unchecked. It passes through validation, scoping, and — for anything sensitive — a human gate, before it executes, and everything it does is audited and reversible.

That was true for a Kubernetes operator reconciling a fleet of clusters. It's true for an AI agent remediating a live incident. The actor changed; the control plane didn't.

That's the bet behind everything I'm building now: the model was never the bottleneck. The control layer was.
