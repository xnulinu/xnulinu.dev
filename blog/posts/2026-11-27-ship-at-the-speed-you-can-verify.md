---
title: A software factory runs at the speed you can verify
date: 2026-11-27
summary: How I built my software factory, one bottleneck at a time, what it caught this week, and what I'm building next. The pace is set by how fast I can trust a change, not how fast agents write one.
image: software-factory.webp
---

Everyone is trying to build a software factory now. Agents write most of the code, and the question has moved from "can they" to "how do you run them".

I build AstroPulse with several AI agents working in parallel. For months I assumed the limit was how fast they could write code. It wasn't. The limit was how fast I could trust what they wrote. Each stage below is a piece of that trust, in the order I built it.

## Start: the whole platform, on every engineer's machine

```sets
title: One checkout, a few commands: the real platform on a kind cluster, no shared staging.
An engineer's laptop: the whole platform
Control plane: API, console, CLI
* Customer cluster: agent, tunnel, add-ons
Apps: deploy, history, rollback
Models on CPU: serving, policies, metrics
```

A change crosses the control plane, the agent on the customer's cluster, the tunnel, the CLI and the console. Mocks can't tell you whether that chain still holds, so every engineer and every agent gets all of it locally. Every service runs the committed HEAD, or "verified" means nothing.

## Agents in parallel, one integration tree

```flow
title: Everything in flight is tested together, never one branch at a time.
[agent] agents, one worktree each
[eye] review
[merge] local integration tree
* [cloud] deployed to kind
```

Related issues go into one PR. The integration tree is never pushed; it exists so the branches meet before main does.

## A lab for everything

```tiles
title: A lab drives the real CLI against the real platform and checks what a user would see.
[branch] Picked by the diff: each lab declares the paths it covers
[terminal] Isolated runs: own run ID, own names, own logs
[check] Red means you broke it: known failures are passed in as a baseline
[checks] Nothing unmapped: every command, operation and add-on has a lab or an open issue
[moon] Nightly on main: runs every lab; started by hand today, scheduled next
* [lock] In CI next: the same verifier and labs
```

Each lab gets its own run ID and resource names, and compares against a baseline of known failures so a red run always means the change in front of you broke something.

## Batches, one verdict

```flow
title: Changes pass alone all the time. The batch says whether they pass together.
[layers] ready PRs
[branch] fresh copy of main
[cloud] deploy together
[lab] every safe lab
* [check] one verdict
```

Individual PRs can both pass in isolation and still conflict on `main`. The batch deploys every ready PR together on a fresh copy of `main` and runs every non-destructive lab for a single go/no-go verdict.

## Every surface, every client

```tiles
title: An API change isn't done when the server is. Every client moves in the same pass.
[terminal] CLI: the same workflow, run both ways
[console] Console: light, dark and phone width, a screenshot per page
[package] Python SDK: regenerated, built and compiled in CI
[agent] MCP server: re-pinned to the new CLI on release
[doc] Docs and website: a sync PR with every release
* [api] The API owns the words: a refusal reads the same sentence everywhere
```

CI regenerates everything and fails on any diff, and refuses a breaking API change. A last step checks every artifact the way a user gets it.

## Gates aimed at how agents cheat

```gates
title: Agents find the cheapest path to green. Each layer is aimed at one of those moves.
[commit] commit: lint errors
[push] push: stale generated code
[checks] PR checks: fixed sleeps, blind retries, matching error text, narrating comments, internal names, secrets, CVEs
[agent] agent review: grading its own work, breaking a client
[gate] human gate: deleted tests, new skips, removed assertions, shims, auth changes
* [person] a person merges: an agent merging
```

Review is independent, with a neutral brief, and some PRs get a second model from another vendor. When review catches a mistake, it becomes a rule in the AGENTS.md every agent reads first. The rule at the top: the human's job is decision-making, not mechanics.

## The proof

This week the second model caught a console route that broke deleting an app named "sources". The independent reviewer caught a new API field that broke the CLI's get-then-apply round trip.

```trend
title: Merged changes per week, Jul–Nov, on a log scale. The last week is still in progress.
3.7 Jul
3.9
5.5 Aug
3.3
3.0
2.6
0 Sep
0
0
2.3
2.0 Oct
0
1.0
1.0
0
* 5.3 v1.0
7.4 Nov
6.1
```

Same agents. They didn't get better at writing code that week; I got better at checking what they wrote.

## What's still hard, and the plan

```flow
title: The loop, from an issue to a release.
[issue] issue
[branch] worktree
[lab] verify
[eye] review
* [person] human merge
[moon] nightly
[release] release
```

The left half runs every day. The right half is what I’m building now, and it’s what turns a fast workshop into a factory.

```bars
title: Where a batch run spends its time. Writing and merging are no longer the bottleneck.
* 10 labs, one at a time
5.6 Go tests and lint
3.2 deploy and restarts
2.5 generate on a fresh worktree
0.2 image build
0.1 worktree and merge
```

The workshop got fast at writing and merging, and now it waits on itself—serial labs alone take about half of every batch run.

```shift
title: Turning the workshop into a factory. A person still merges.
[wrench] Workshop today -> [factory] Factory next
labs run one at a time -> independent labs in parallel
known failures still run -> known failures skipped
every reload restarts everything -> reload only what changed
one lock held for the whole batch -> lock only around the build
one shared cluster -> an environment per agent
labs on a laptop -> the same labs in CI
nightly started by hand -> nightly every night, green opens a release PR
merges against a moving main -> a merge queue
I read the checks -> required checks block the merge
upkeep waits on me -> weekly agent routines open draft PRs
* I review at the gate -> I write the rules and checks
```

I started by writing the code. Now I review at the gate. Next I mostly write the rules and checks the agents work within—building on the same [platform composition](2026-09-16-if-everything-is-custom-it-isnt-a-platform.html "If everything is custom, it isn't a platform") and [control plane](2026-07-01-the-control-plane-is-the-product.html "The control plane is the product") boundaries. One thing doesn't move: merging stays a deliberate human act.

If you're running agents in parallel and hitting the verification wall too, [tell me what's bottlenecking your loop](../index.html#contact "Get in touch").
