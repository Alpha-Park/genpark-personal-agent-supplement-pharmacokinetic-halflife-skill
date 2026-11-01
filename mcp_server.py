# -*- coding: utf-8 -*-
"""FastMCP Server for Personal Agent Supplement Pharmacokinetic Halflife Skill."""

from mcp.server.fastmcp import FastMCP
from client import PersonalAgentSupplementPharmacokineticHalflife

mcp = FastMCP("PersonalAgentSupplementPharmacokineticHalflife")
client = PersonalAgentSupplementPharmacokineticHalflife()

@mcp.tool()
def model_compound_clearance_curve(
    compound_name: str = "caffeine",
    dose_mg: float = 200.0,
    time_elapsed_hours: float = 6.0,
    custom_half_life_hours: float = 5.5
) -> str:
    """Calculates active plasma level, clearance percentage, and hours to 95% elimination."""
    import json
    return json.dumps(client.model_compound_clearance_curve(
        compound_name, dose_mg, time_elapsed_hours, custom_half_life_hours
    ), indent=2)

@mcp.tool()
def evaluate_supplement_stack_interactions(
    supplements_taken_json: str
) -> str:
    """Screens supplement stack for competitive transporter competition and neurochemical antagonism."""
    import json
    data = json.loads(supplements_taken_json) if isinstance(supplements_taken_json, str) else supplements_taken_json
    return json.dumps(client.evaluate_supplement_stack_interactions(data), indent=2)

if __name__ == "__main__":
    mcp.run()
