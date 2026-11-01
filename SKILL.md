---
name: genpark-personal-agent-supplement-pharmacokinetic-halflife-skill
version: "1.0.0"
description: "Zero-dependency supplement pharmacokinetics modeler, elimination half-life decay tracker, competitive absorption conflict matrix evaluator, and optimal ingestion scheduler."
license: MIT
dependencies:
  - python>=3.10
  - mcp>=1.0.0
entrypoint: client.py
---

# Personal Agent Supplement Pharmacokinetic Halflife Skill

Designed for **OpenClaw**, **Hermes**, and autonomous personal AI agents to optimize nutraceutical timing, prevent competitive transporter inhibition, model elimination half-life curves, and schedule personalized ingestion windows.

## Agent In-Context Capabilities

- **Bateman Elimination Modeling**: Computes oral absorption, plasma peaks, active circulating levels, and 95%/99% clearance washouts.
- **Competitive DMT1 Transporter Resolution**: Detects high-dose divalent cation antagonism (e.g. Zinc vs. Iron vs. Calcium) and staggers administration.
- **Lipophilic Optimization**: Identifies compounds requiring dietary triacylglycerols for micelle-mediated enterocyte uptake.

## Tools Summary

1. `model_compound_clearance_curve`: Returns active plasma milligram concentration and elimination washout timing.
2. `evaluate_supplement_stack_interactions`: Identifies mineral competitions and neurochemical timing conflicts.
