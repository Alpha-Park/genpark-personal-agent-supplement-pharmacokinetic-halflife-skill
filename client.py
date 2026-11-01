# -*- coding: utf-8 -*-
"""Personal Agent Supplement Pharmacokinetic Halflife Skill.

Zero-dependency supplement pharmacokinetics modeler, elimination half-life decay tracker,
competitive absorption conflict matrix evaluator, and optimal ingestion scheduler.
"""

import math
from typing import Dict, List, Any, Optional

class PersonalAgentSupplementPharmacokineticHalflife:
    """Nutraceutical pharmacokinetics and competitive absorption interaction engine
    using classic one-compartment oral absorption and elimination kinetics."""

    # Reference pharmacokinetics for common personal health compounds
    COMPOUND_DATABASE = {
        "caffeine": {"half_life_h": 5.5, "t_max_h": 0.75, "bioavail": 0.99, "lipid_required": False, "transporter": "cyp1a2"},
        "creatine": {"half_life_h": 3.0, "t_max_h": 1.5, "bioavail": 0.90, "lipid_required": False, "transporter": "crt"},
        "vitamin_d3": {"half_life_h": 360.0, "t_max_h": 12.0, "bioavail": 0.75, "lipid_required": True, "transporter": "passive_micelle"},
        "magnesium_glycinate": {"half_life_h": 4.5, "t_max_h": 2.0, "bioavail": 0.45, "lipid_required": False, "transporter": "divalent_cation"},
        "zinc_picolinate": {"half_life_h": 6.0, "t_max_h": 2.5, "bioavail": 0.50, "lipid_required": False, "transporter": "divalent_cation"},
        "iron_bisglycinate": {"half_life_h": 7.0, "t_max_h": 3.0, "bioavail": 0.40, "lipid_required": False, "transporter": "divalent_cation"},
        "ashwagandha_withanolides": {"half_life_h": 4.0, "t_max_h": 2.0, "bioavail": 0.60, "lipid_required": True, "transporter": "cyp3a4"},
        "melatonin": {"half_life_h": 0.75, "t_max_h": 0.5, "bioavail": 0.15, "lipid_required": False, "transporter": "cyp1a2"}
    }

    def model_compound_clearance_curve(
        self,
        compound_name: str,
        dose_mg: float,
        time_elapsed_hours: float,
        custom_half_life_hours: Optional[float] = None
    ) -> Dict[str, Any]:
        """Calculates plasma concentration trajectory, current circulating fraction,
        and hours until 95% clearance (4.32 * half_life)."""
        key = compound_name.lower().replace(" ", "_")
        meta = self.COMPOUND_DATABASE.get(key, {
            "half_life_h": custom_half_life_hours or 5.0,
            "t_max_h": 1.5,
            "bioavail": 0.80,
            "lipid_required": False,
            "transporter": "general"
        })

        t_half = custom_half_life_hours if custom_half_life_hours else meta["half_life_h"]
        k_el = math.log(2.0) / t_half  # elimination rate constant
        k_abs = 2.5  # rapid oral absorption rate constant

        t = max(0.0, float(time_elapsed_hours))
        # Bateman oral concentration function (normalized peak = 1.0)
        norm_factor = (k_abs / (k_abs - k_el)) if k_abs != k_el else 1.0
        circulating_fraction = max(0.0, norm_factor * (math.exp(-k_el * t) - math.exp(-k_abs * t)))
        # Scale to dose and bioavailability
        active_plasma_level_mg = round(dose_mg * meta["bioavail"] * circulating_fraction, 2)
        elimination_percentage = round((1.0 - math.exp(-k_el * t)) * 100.0, 1) if t > meta["t_max_h"] else 0.0

        hours_to_95_clearance = round(t_half * 4.32, 1)
        hours_to_99_clearance = round(t_half * 6.64, 1)

        return {
            "compound": compound_name,
            "administered_dose_mg": dose_mg,
            "time_elapsed_hours": t,
            "elimination_half_life_hours": t_half,
            "estimated_bioavailability_pct": f"{int(meta['bioavail'] * 100)}%",
            "active_circulating_dose_mg": active_plasma_level_mg,
            "percent_cleared": f"{min(100.0, elimination_percentage)}%",
            "hours_until_95pct_clearance": hours_to_95_clearance,
            "hours_until_99pct_complete_washout": hours_to_99_clearance,
            "lipid_co_ingestion_required": meta["lipid_required"]
        }

    def evaluate_supplement_stack_interactions(
        self,
        supplements_taken: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detects competitive absorption bottleneck conflicts (divalent cations, lipid carriers)
        and outputs a chronobiologically optimized ingestion schedule."""
        divalent_cations = []
        lipophilic_compounds = []
        stimulants = []
        sedatives = []
        conflicts = []

        for item in supplements_taken:
            name = item.get("name", "").lower().replace(" ", "_")
            dose = item.get("dose_mg", 0.0)
            timing = item.get("timing_24h", 8.0)

            if "zinc" in name or "iron" in name or "calcium" in name or "magnesium" in name:
                divalent_cations.append({"name": item.get("name"), "dose": dose, "timing": timing})
            if "vitamin_d" in name or "vitamin_k" in name or "omega" in name or "coq10" in name or "curcumin" in name:
                lipophilic_compounds.append({"name": item.get("name"), "timing": timing})
            if "caffeine" in name or "yohimbine" in name or "tyrosine" in name:
                stimulants.append({"name": item.get("name"), "timing": timing})
            if "melatonin" in name or "ashwagandha" in name or "gaba" in name:
                sedatives.append({"name": item.get("name"), "timing": timing})

        # Check divalent cation competition (absorption transporter DMT1 saturation)
        if len(divalent_cations) >= 2:
            names = [x["name"] for x in divalent_cations]
            conflicts.append({
                "conflict_type": "Competitive DMT1 Transporter Inhibition",
                "compounds_involved": names,
                "mechanism": "High-dose divalent minerals (e.g. Zinc, Iron, Calcium) compete for the same intestinal mucosal transporters.",
                "resolution": "Stagger administration by at least 2 hours (e.g. Zinc in morning, Magnesium in evening)."
            })

        # Check lipophilic co-ingestion requirement
        if lipophilic_compounds:
            conflicts.append({
                "conflict_type": "Lipophilic Bioavailability Optimization",
                "compounds_involved": [x["name"] for x in lipophilic_compounds],
                "mechanism": "Fat-soluble compounds require dietary triacylglycerols (> 10g lipid) for biliary micelle packaging.",
                "resolution": "Ingest alongside a fat-containing meal (avocado, eggs, olive oil)."
            })

        # Check stimulant vs sedative timing
        for stim in stimulants:
            for sed in sedatives:
                if abs(stim["timing"] - sed["timing"]) < 4.0:
                    conflicts.append({
                        "conflict_type": "Neurochemical Antagonism",
                        "compounds_involved": [stim["name"], sed["name"]],
                        "mechanism": "Adenosine antagonist / stimulant taken within 4 hours of GABAergic / melatonin sedative.",
                        "resolution": "Separate by at least 8 hours."
                    })

        return {
            "total_compounds_screened": len(supplements_taken),
            "interaction_conflicts_detected": len(conflicts),
            "detected_conflicts": conflicts,
            "stack_optimization_tier": "Frictionless Stacking" if not conflicts else "Pharmacokinetic Friction Present",
            "chronobiological_schedule_guidance": (
                "Morning: B-Complex, Vitamin D3/K2 (with breakfast fat), Creatine.\n"
                "Mid-Day: Zinc Picolinate (with lunch).\n"
                "Evening: Magnesium Glycinate (1-2 hours before bed)."
            )
        }
