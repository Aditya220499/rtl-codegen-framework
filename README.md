**********************************************************************************************************************************************************************************
# SoC Integration Automation

## Overview

This project demonstrates metadata-driven automation of SoC IP integration.

Instead of manually wiring vendor IP blocks, this tool:

- Parses structured IP definitions (JSON)
- Automatically connects signals based on matching port names
- Validates direction-based driver ownership
- Detects width mismatches
- Generates synthesizable SystemVerilog top-level RTL

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
│   └── top_generated.sv
└── README.md
```

---

## Input Format

Each JSON file defines IP blocks:

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

Output will be generated at:

```
output/top_generated.sv
```

---

## Demonstration Scenarios

### 1. Error Case – Multi-Driver Detection

```
python generate_top.py scenarios/scenario_error.json
```

Expected:

```
ValueError: Multiple drivers detected on signal 'irq'
```

Demonstrates electrical topology validation.

---

### 2. Valid SoC Connectivity

```
python generate_top.py scenarios/scenario_valid.json
```

Generated RTL demonstrates:

- One driver per shared signal
- Automatic input/output wiring
- Width consistency enforcement
- Safe electrical topology

---

## Why This Matters

Modern SoCs integrate many third-party IP blocks.

Manual top-level wiring does not scale.

This automation framework enables:

- Scalable IP integration
- Driver ownership validation
- Early detection of structural design errors
- Regeneration when metadata changes
- Improved integration reliability

---

## Future Extensions

- Interrupt controller auto-generation
- Arbitration detection
- Unconnected port warnings
- Bus protocol abstraction (AXI/APB)
- CI-based regression validation
- IP-XACT support



**********************************************************************************************************************************************************************************
