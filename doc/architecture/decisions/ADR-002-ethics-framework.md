# ADR-002: Ethics framework for commercial use

**Status**: Accepted

**Date**: 2026-05-08

## Context

“Cognitive Bias Tester” educates users to **recognize and resist** manipulation and biased reasoning. That mission is incompatible with customers who would reuse our tooling **to manipulate** people at scale. The project specification (`doc/project-progress/spec.md`, **Key Technical Decisions** — row **15**, **Ethics framework**) calls for an explicit ADR in Epic E010 defining B2B segments we refuse so ethics and legal posture stay clear as we grow.

## Decision

We adopt a public ethics stance for **who we sell to** and **who we do not**, aligned with teaching resistance to manipulation—not enabling it.

### Mission alignment

We build training that helps users notice framing, anchoring, sunk-cost pressure, and similar patterns **defensively**. Products, integrations, or custom content that turn this into **offensive manipulation** (deceiving or unduly pressuring audiences) are out of scope and unsupported.

## We will not sell to

- **Manipulative marketing agencies** — campaigns optimised to exploit cognitive biases against consumer interests.
- **Dark-pattern designers** — teams shipping deceptive UX intended to trick users into harmful or unwanted actions.
- **Political microtargeting firms** — operations using psychographic segmentation to manipulate voters or suppress turnout.
- **Gambling operators** — businesses whose revenue depends on reinforcing loss-chasing and impulsive betting.

(Expand or refine categories only via a **new ADR that amends this record**—see **Amendment process** below.)

## We are open to

- **HR / Learning & Development** — training employees on ethical decision-making and bias awareness.
- **Financial advisors** — education that helps clients recognise sales pressure and biased framing.
- **Healthcare informed-decision tooling** — patient or clinician education that improves understanding without coercion (subject to regulation and clinical governance where applicable).
- **Judiciary and legal training** — bias-awareness curricula for fair proceedings.
- **Education sector** — schools and universities teaching critical thinking and debiasing.

## Amendment process

- **No silent edits** to this list: adding or removing a category requires a **follow-up ADR** (e.g. `ADR-0NN-amend-ethics-framework.md`) that references ADR-002, states the change, rationale, and effective date.
- **Versioning:** keep accepted ADRs immutable; use amend/replace ADRs for substantive policy changes.

## Consequences

- **Positive:** Clear external message; easier sales qualification; groundwork for contractual “acceptable use” language.
- **Negative:** Some revenue opportunities will be declined; edge-case customers may require legal review to classify.
