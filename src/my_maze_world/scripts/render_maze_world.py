#!/usr/bin/env python3
"""Write a maze world with the requested wall thickness."""

import argparse
import math
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("wall_thickness", type=float)
    args = parser.parse_args()

    if not math.isfinite(args.wall_thickness) or args.wall_thickness <= 0:
        parser.error("wall_thickness must be a positive finite number")

    tree = ET.parse(args.source)
    for model in tree.findall("./world/model"):
        if not model.get("name", "").startswith(("wall_", "maze_wall")):
            continue
        for size in model.findall("./link/*/geometry/box/size"):
            dimensions = [float(value) for value in size.text.split()]
            thickness_axis = 0 if dimensions[0] < dimensions[1] else 1
            dimensions[thickness_axis] = args.wall_thickness
            size.text = " ".join(f"{value:g}" for value in dimensions)

    tree.write(args.output, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
