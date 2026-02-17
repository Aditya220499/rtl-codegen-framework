"""
SoC Integration Automation Tool
--------------------------------

This script:
- Parses IP metadata from JSON
- Automatically connects signals based on name
- Enforces direction-based driver validation
- Detects width mismatches
- Generates a synthesizable top-level SystemVerilog module

Usage:
    python generate_top.py <path_to_json>

Example:
    python generate_top.py scenarios/scenario_valid.json
"""

import json
import os
import sys
from jinja2 import Environment, FileSystemLoader


# ---------------------------
# Argument Handling
# ---------------------------

if len(sys.argv) < 2:
    print("Usage: python generate_top.py <json_file>")
    sys.exit(1)

INPUT_FILE = sys.argv[1]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "top_generated.sv")


# ---------------------------
# Load Metadata
# ---------------------------

def load_metadata():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"JSON file not found: {INPUT_FILE}")

    with open(INPUT_FILE) as f:
        return json.load(f)


# ---------------------------
# Connectivity Analysis
# ---------------------------

def analyze_connectivity(ips):
    """
    Build connectivity graph based on matching port names.

    Rules:
    - If only one port exists → isolated net
    - If multiple ports share name:
        - Exactly one must be 'output'
        - Others must be 'input'
        - Width must match
    """

    signal_map = {}

    # Group ports by signal name
    for ip in ips:
        for port in ip["ports"]:
            name = port["name"]

            if name not in signal_map:
                signal_map[name] = []

            signal_map[name].append({
                "instance": ip["instance"],
                "dir": port["dir"],
                "width": port["width"]
            })

    nets = []
    connection_map = {}

    for signal, entries in signal_map.items():

        # Check width consistency
        widths = set(e["width"] for e in entries)
        if len(widths) > 1:
            raise ValueError(f"Width mismatch detected on signal '{signal}'")

        outputs = [e for e in entries if e["dir"] == "output"]
        inputs = [e for e in entries if e["dir"] == "input"]

        # Case 1: Only one module has this signal
        if len(entries) == 1:
            e = entries[0]
            net_name = f"{e['instance']}__{signal}"

            nets.append({
                "name": net_name,
                "width": e["width"]
            })

            connection_map[(e["instance"], signal)] = net_name

        # Case 2: Shared signal between modules
        else:
            if len(outputs) == 0:
                raise ValueError(f"No driver found for shared signal '{signal}'")

            if len(outputs) > 1:
                raise ValueError(f"Multiple drivers detected on signal '{signal}'")

            # Valid connection: one driver, many inputs
            net_name = signal

            nets.append({
                "name": net_name,
                "width": outputs[0]["width"]
            })

            for e in entries:
                connection_map[(e["instance"], signal)] = net_name

    return nets, connection_map


# ---------------------------
# Main Flow
# ---------------------------

def main():
    data = load_metadata()
    ips = data["ips"]

    nets, connection_map = analyze_connectivity(ips)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("top_template.sv.j2")

    output = template.render(
        ips=ips,
        nets=nets,
        connection_map=connection_map
    )

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        f.write(output)

    print("Top module generated successfully.")
    print(f"Output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
