import sys

sys.exit()

scaffold = """
├── __init__.py
├── io/
│   ├── __init__.py
│   ├── paths.py
│   ├── json_tools.py
│   └── geojson_tools.py
├── maps/
│   ├── __init__.py
│   ├── leaflet_helpers.py
│   ├── style_tools.py
│   └── interaction.py
├── geometry/
│   ├── __init__.py
│   ├── points.py
│   ├── bbox.py
│   ├── distance.py
│   ├── bearing.py
│   ├── interpolation.py
│   └── simplify.py
├── spatial/
│   ├── __init__.py
│   ├── feature_queries.py
│   ├── intersections.py
│   ├── buffers.py
│   └── pip.py
├── games/
│   ├── __init__.py
│   ├── worldle.py
│   └── pursuit.py
├── graphs/
│   ├── __init__.py
│   ├── rail_graph.py
│   ├── connectivity.py
│   └── routing.py
└── utils/
    ├── __init__.py
    ├── formatting.py
    └── validation.py
"""

from pathlib import Path

pname = None

for item in scaffold.split("\n"):
    parts = item.split()
    if len(parts):
        if parts[-1][-1] == "/":
            print(f"dir: {parts[-1]}")
            pname = parts[-1]
            p = Path(parts[-1])
            p.mkdir(exist_ok=True)
        else:
            print(f"file: {parts[-1]}")
            if pname:
                print(f"./{pname}{parts[-1]}")
                with open(f"./{pname}{parts[-1]}", "w"):
                    pass


