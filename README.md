**********************************************************************************************************************************************************************************
# 1.  SOC Scripting

# SoC Top Module Generator

## Overview
This project demonstrates metadata-driven automation of SoC IP integration.
Instead of manually wiring vendor IP blocks, this script:

- Parses structured IP definitions (JSON)
- Generates unique nets for each IP port
- Uses a Jinja template to generate a SystemVerilog top module
- Produces synthesizable RTL automatically

This approach reflects modern SoC integration workflows used in  semiconductor companies.

---

## Project Structure

```
soc-top-generator/
│
├── generate_top.py
├── input/
│   └── ip_description.json
├── templates/
│   └── top_template.sv.j2
├── output/
│   └── top_generated.sv
```

---

## Input Format

`input/ip_description.json`

```json
{
  "ips": [
    {
      "module": "cpu_core",
      "instance": "u_cpu",
      "ports": [
        {"name": "clk", "dir": "input", "width": 1},
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
- Direction
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

From the project root directory:

```
python generate_top.py
```

Output will be generated at:

```
output/top_generated.sv
```

---

## Why This Matters

Modern SoCs integrate many third-party IP blocks.

Manual wiring does not scale.

This automation framework enables:

- Faster integration
- Reduced human error
- Regeneration when IP definitions change
- Scalable SoC architecture

---

## Future Extensions

- Parameter support
- Width mismatch detection
- Bus grouping (AXI/APB abstraction)
- TCL script generation
- Verification scaffold generation


**********************************************************************************************************************************************************************************
