---
title: If everything is custom, it isn't a platform
date: 2026-09-16
summary: How do you build a platform without making every new workload a bespoke integration? Bricks are the reusable capabilities. Blueprints compose them around the part of the product that's actually yours.
---

One problem keeps coming back:

**How do you build a platform without making every new workload a bespoke integration?**

You can build an inference stack. Then a training stack. Then something for agents, databases, schedulers, or whatever comes next. But if every new product needs another special path through the platform, you haven't really built a platform.

This is why I keep coming back to Bricks and Blueprints while building AstroPulse.

## Bricks

A Brick is a reusable production capability: compute, Kubernetes, GPUs, networking, deployment, identity, observability, autoscaling, policy, rollback, and so on.

The important part isn't the name. It's the contract. A Brick declares what it requires, what it provides, what it can connect to, who owns it, and how it is operated.

Installing cert-manager is easy. Making certificate management a capability that can safely participate in many different production architectures is much harder. So is knowing whether the cert-manager already on the cluster is the platform's, someone else's, or not there at all. That's a Brick.

## Blueprints

But Bricks alone aren't enough. If I give someone 30 infrastructure APIs and ask them to assemble their own production system, I've just given them another infrastructure project.

Something needs to compose the Bricks. A Blueprint describes how Bricks come together to form a production system. Some Bricks come from the platform. Some already exist in the company: its identity provider, its auth service, its billing.

An inference company, for example, might own a custom scheduler, routing algorithm, or caching strategy. That's their product. AstroPulse shouldn't replace it. But that product still needs GPUs, deployment, networking, identity, observability, lifecycle, governance, and operations around it.

The Blueprint expresses that surrounding machinery while leaving the differentiated behavior with the company building the product.

```sets
Blueprint: the whole production system
Platform Bricks: GPUs, deployment, networking, observability
Company Bricks: identity provider, auth service, billing
* Your product: scheduler, routing, caching
```

| Blueprint supplies | AstroPulse connects | Company continues to own |
|---|---|---|
| Model, runtime, hostname | GPUs, workload, gateway, TLS | Model choice and product behavior |
| Identity provider reference | Authentication on the endpoint | Issuing credentials, deciding who gets them |
| Scaling signal | Autoscaling and capacity | Scheduling, routing, caching |

And I don't think a Blueprint should become another giant YAML file. The input should be closer to intent:

> Run this runtime on GPUs. Keep the workload in my cloud. Give it private storage and an authenticated endpoint. Scale using this signal. This scheduling behavior belongs to my product.

The platform resolves that intent into the actual infrastructure.

```flow
Intent
Blueprint
Plan
Policy / Approval
Bricks
* Production system
```

That planning layer matters. Before changing infrastructure, the system should be able to explain what it will create, what it will reuse, what it will change, and what policy applies.

And because every Brick has an explicit contract, the one composing the Blueprint doesn't have to be a person. That gives AI a much safer place to operate. An agent shouldn't need to SSH into machines or improvise Kubernetes manifests. It can reason about intent, construct or modify a Blueprint, inspect the resulting plan, and operate through the same policy, approval, audit, and rollback boundaries as a human or an API — the [control plane](2026-07-01-the-control-plane-is-the-product.html "The control plane is the product") doing its job.

The reason for the architecture is composition.

AstroPulse already has much of the control plane and many of the capabilities that can become Bricks. What I'm working toward now is the composition layer that makes those capabilities genuinely programmable.

And the test for me is simple:

**Can somebody build something on AstroPulse that I never specifically designed AstroPulse to build?**

If every new workload requires another special path, I haven't built a platform. If a company can bring the thing that makes its product different and compose the production machinery it needs around it, then maybe I have.

If your team spends more time on the machinery *around* your product than on the product itself, [tell me how you're dealing with it](../index.html#contact "Get in touch").
