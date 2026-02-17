**********************************************************************************************************************************************************************************
# SoC Integration Automation

![CI](https://github.com/Aditya220499/rtl-codegen-framework/actions/workflows/ci.yml/badge.svg)

---

## Overview

This project demonstrates metadata-driven automation of SoC IP integration.

Instead of manually wiring vendor IP blocks, this tool:

- Parses structured IP definitions (JSON)
- Automatically connects signals based on matching port names
- Validates direction-based driver ownership
- Detects width mismatches
- Supports top-level external signals (e.g., `clk`, `rst_n`)
- Generates synthesizable SystemVerilog top-level RTL
- Produces a connectivity report for visibility

This reflects modern SoC integration workflows used in semiconductor product companies.

---

## Project Structure

```
soc-integration-automation/
│
├── generate_top.py
├── templates/
│   └── top_template.sv.j2
├── scenarios/
│   ├── scenario_valid.json
│   └── scenario_error.json
├── output/
│   ├── top_generated.sv
│   └── connectivity_report.txt
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

---

## Input Format

Each JSON file defines IP blocks and their ports.

Example:

```json
{
  "ips": [
    {
      "module": "cpu_core",
      "instance": "u_cpu",
      "ports": [
        {"name": "irq", "dir": "input", "width": 1},
        {"name": "data_out", "dir": "output", "width": 32}
      ]
    }
  ]
}
```

Each IP requires:

- Module name
- Instance name
- Port list
- Direction (`input` / `output`)
- Width

---

## Installation

Ensure Python 3.8+ is installed.

Install Jinja2:

```
python -m pip install jinja2
```

---

## Execution

Run with a scenario file:

```
python generate_top.py scenarios/scenario_valid.json
```

or

```
python generate_top.py scenarios/scenario_error.json
```

Generated outputs:

```
output/top_generated.sv
output/connectivity_report.txt
```

---

## Demonstration Scenarios

### 1️⃣ Error Case – Multi-Driver Detection

```
python generate_top.py scenarios/scenario_error.json
```

Expected:

```
ValueError: Multiple drivers detected on signal 'irq'
```

Demonstrates electrical topology validation.

---

### 2️⃣ Valid SoC Connectivity

```
python generate_top.py scenarios/scenario_valid.json
```

Generated RTL demonstrates:

- One driver per shared signal
- Automatic inter-block connectivity
- Width consistency enforcement
- Safe electrical topology

Connectivity report summarizes:

- Drivers
- Consumers
- External signals
- Signal ownership

---

## Continuous Integration (CI)

This repository includes a GitHub Actions workflow.

On every push or pull request:

- Valid scenario must generate RTL successfully
- Error scenario must fail (multi-driver detection)
- Output RTL file must exist
- Connectivity report must be generated

This ensures structural and electrical correctness is automatically verified.

---

## Why CI Matters in VLSI Automation

In hardware design, integration errors are expensive.

Common integration mistakes include:

- Multiple drivers on a net
- Width mismatches
- Undriven inputs
- Incorrect signal ownership
- Broken top-level connectivity

Without automation, these errors may only be discovered:

- During simulation
- During synthesis
- During late integration
- Or worse — after silicon tape-out

CI provides:

- Early detection of structural bugs
- Regression protection when code evolves
- Confidence in tool correctness
- Automated validation on every commit

In modern semiconductor workflows, automation and CI are critical for scalable SoC development.

---

## Why This Project Matters

Modern SoCs integrate many third-party IP blocks.

Manual top-level wiring does not scale.

This automation framework enables:

- Scalable IP integration
- Driver ownership validation
- Early detection of structural design errors
- Regeneration when metadata changes
- Improved integration reliability
- Infrastructure-level verification discipline

---

## Future Extensions

- Interrupt controller auto-generation
- Arbitration detection
- Unconnected port warnings
- Bus protocol abstraction (AXI/APB)
- IP-XACT support
- Graph-based connectivity visualization

**********************************************************************************************************************************************************************************
