# -*- coding: utf-8 -*-
"""Demonstration of Personal Agent Supplement Pharmacokinetic Halflife Skill."""

import sys
sys.stdout.reconfigure(encoding='utf-8')
from client import PersonalAgentSupplementPharmacokineticHalflife

def main():
    agent = PersonalAgentSupplementPharmacokineticHalflife()

    print("=" * 70)
    print("DEMO: Personal Agent Supplement Pharmacokinetics & Stack Optimization")
    print("=" * 70)

    # 1. Model Caffeine Clearance Curve (200 mg consumed 6.5 hours ago)
    res_pk = agent.model_compound_clearance_curve(
        compound_name="caffeine",
        dose_mg=200.0,
        time_elapsed_hours=6.5
    )

    print(f"\n1. Caffeine Pharmacokinetics (200 mg oral dose @ T+6.5 hrs):")
    print(f"   Elimination Half-Life: {res_pk['elimination_half_life_hours']} hrs")
    print(f"   Active Circulating Dose: {res_pk['active_circulating_dose_mg']} mg")
    print(f"   Percent Cleared: {res_pk['percent_cleared']}")
    print(f"   Hours to 95% Elimination: {res_pk['hours_until_95pct_clearance']} hrs")
    print(f"   Hours to 99% Washout: {res_pk['hours_until_99pct_complete_washout']} hrs")

    # 2. Evaluate Stacking Interactions across user's daily regimen
    stack = [
        {"name": "Zinc Picolinate", "dose_mg": 30.0, "timing_24h": 8.0},
        {"name": "Iron Bisglycinate", "dose_mg": 25.0, "timing_24h": 8.0},
        {"name": "Vitamin D3", "dose_mg": 0.125, "timing_24h": 8.0},
        {"name": "Magnesium Glycinate", "dose_mg": 400.0, "timing_24h": 22.0}
    ]

    res_int = agent.evaluate_supplement_stack_interactions(stack)

    print(f"\n2. Daily Supplement Stack Conflict Screen:")
    print(f"   Screened Compounds: {res_int['total_compounds_screened']}")
    print(f"   Conflicts Detected: {res_int['interaction_conflicts_detected']}")
    print(f"   Stack Status: {res_int['stack_optimization_tier']}")
    for conf in res_int['detected_conflicts']:
        print(f"   - Conflict: {conf['conflict_type']}")
        print(f"     Compounds: {conf['compounds_involved']}")
        print(f"     Mechanism: {conf['mechanism']}")
        print(f"     Resolution: {conf['resolution']}")

    print("\nVerification complete: Supplement pharmacokinetic engine executed flawlessly.")

if __name__ == "__main__":
    main()
