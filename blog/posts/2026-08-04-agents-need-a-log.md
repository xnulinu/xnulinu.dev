---
title: Agents need a log
date: 2026-08-04
summary: The control layer decides what an agent may do. The record of what it actually did — durable, ordered, queryable — is the harder half. That's a streaming problem.
image: agents-need-a-log.webp
---

I've spent the last year building the control layer that lets AI agents act safely in production: scoped access, approval gates, blast-radius checks, rollback. That was the bet in [the control plane is the product](2026-07-01-the-control-plane-is-the-product.html "The control plane is the product") — capability is a commodity, trusted execution is the product.

That layer works. But the part I keep coming back to sits underneath it.

## Governance is only as good as its record

Every question an operator asks about an agent is a question about history:

- Which agent took this action, who approved it, under what scope, and when did that approval expire?
- What exactly did the agent change, in what order, and what happened next?
- Which actions have succeeded often enough that we can stop reviewing them?

The first is audit. The second is rollback — you can't reverse what you can't reconstruct. The third is the feedback loop — how a team goes from read-only suggestions to earned autonomy. All three are answered the same way: by replaying and querying the record of what the agent did.

So the record can't be an afterthought — not log lines scattered across services, not rows overwritten in place. Every agent action needs to be an event: durable, ordered, queryable.

## That's a stream

And the record has more than one reader. Policy enforcement consumes it. The approval flow consumes it. Audit consumes it, possibly years later. The system that learns which actions are safe to automate consumes all of it, repeatedly.

A durable, ordered, replayable record with many independent consumers moving at their own pace — we have a name for that shape. It's the problem we built Kafka for. We've just been applying it to data instead of decisions.

## The log remembers; the stream judges

But the log is only half the build. A record by itself is an archive. Governance is computation over the record, running live:

- An approval that expires is a timer on state.
- A runaway agent is a windowed pattern — forty actions in two minutes.
- Blast radius is a join: this action here, those errors over there, moments later.
- A trust score — which actions have earned autonomy — is an aggregation over the entire history, recomputed whenever the definition of "safe" evolves.

That's stateful stream processing: large keyed state, event-time correctness, and the ability to replay years of history before cutting over to live. This is Flink's half of the problem, the way the record itself is Kafka's. One layer remembers; the other judges.

The agent stack everyone draws — model, tools, policy — is missing its bottom layer. Under the control plane there has to be a log, and running on the log, the machinery that turns history into judgment. Agents don't just need guardrails; they need a streaming platform.
