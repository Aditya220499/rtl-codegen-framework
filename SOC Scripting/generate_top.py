import json
import os
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(BASE_DIR, "input", "ip_description.json")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "top_generated.sv")


def load_metadata():
    with open(INPUT_FILE) as f:
        return json.load(f)


def analyze_connectivity(ips):
    """
    Build connectivity graph based on port names.
    Enforce:
    - Exactly one output per shared signal
    - Width consistency
    """

    signal_map = {}

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

        widths = set(e["width"] for e in entries)
        if len(widths) > 1:
            raise ValueError(f"Width mismatch on signal '{signal}'")

        outputs = [e for e in entries if e["dir"] == "output"]
        inputs = [e for e in entries if e["dir"] == "input"]

        if len(entries) == 1:
            # isolated signal
            e = entries[0]
            net_name = f"{e['instance']}__{signal}"
            nets.append({"name": net_name, "width": e["width"]})
            connection_map[(e["instance"], signal)] = net_name

        else:
            # shared signal
            if len(outputs) == 0:
                raise ValueError(f"No driver found for shared signal '{signal}'")

            if len(outputs) > 1:
                raise ValueError(f"Multiple drivers detected on signal '{signal}'")

            # valid shared connection
            net_name = signal
            nets.append({"name": net_name, "width": outputs[0]["width"]})

            for e in entries:
                connection_map[(e["instance"], signal)] = net_name

    return nets, connection_map


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


if __name__ == "__main__":
    main()
