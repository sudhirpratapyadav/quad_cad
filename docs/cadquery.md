# CadQuery Reference Guide

## Overview
CadQuery is a Python library for building parametric 3D CAD models using OpenCASCADE Technology (OCCT) kernel. It provides programmatic CAD modeling with script-based approach.

## Directory Structure
```
cadquery/
├── README.md                   # Main documentation and installation guide
├── setup.py                   # Package configuration and dependencies
├── cadquery/                  # Main Python package
│   ├── __init__.py            # Main API exports (Workplane, CQ, Assembly, etc.)
│   ├── cq.py                  # Core CQ and Workplane classes - main API
│   ├── assembly.py            # Assembly system for multi-part models
│   ├── sketch.py              # 2D sketching functionality
│   ├── selectors.py           # Geometry selection tools
│   ├── occ_impl/              # OpenCASCADE implementation layer
│   │   ├── shapes.py          # 3D geometry shapes (Solid, Face, Edge, etc.)
│   │   ├── geom.py            # Geometric primitives (Vector, Plane, Matrix)
│   │   ├── assembly.py        # Assembly implementation
│   │   ├── exporters/         # File format exporters (STEP, STL, SVG, etc.)
│   │   └── importers/         # File format importers
│   └── plugins/               # Plugin system
├── doc/                       # Documentation source files
├── examples/                  # Example scripts (Ex001-Ex026)
└── tests/                     # Test suite
```

## Core Components

### Main API Entry Points
- **cadquery/__init__.py:1-79** - Primary API exports and imports
- **cadquery/cq.py** - `CQ` and `Workplane` classes (main modeling API)
- **cadquery/assembly.py** - `Assembly` class for multi-part models
- **cadquery/sketch.py** - `Sketch` class for 2D operations

### Geometry System
- **cadquery/occ_impl/shapes.py** - Shape classes (Solid, Face, Edge, Wire, Vertex)
- **cadquery/occ_impl/geom.py** - Geometric primitives (Vector, Plane, Location, Matrix)
- **cadquery/selectors.py** - Geometry selection and filtering

### Import/Export
- **cadquery/occ_impl/exporters/** - STEP, STL, AMF, 3MF, DXF, SVG formats
- **cadquery/occ_impl/importers/** - DXF import functionality

## How CadQuery Works

1. **Workplane-based modeling**: Create 2D sketches on planes, then extrude/revolve to 3D
2. **Fluent API**: Chain operations using method chaining
3. **Selection system**: Use selectors to pick faces, edges, vertices for operations
4. **Assembly system**: Combine multiple parts with constraints
5. **OpenCASCADE backend**: Uses OCCT for precise CAD operations

## Key Files for AI Navigation
- Start with: cadquery/__init__.py for API overview
- Core modeling: cadquery/cq.py (Workplane class)
- Geometry types: cadquery/occ_impl/shapes.py
- Examples: examples/ directory (Ex001-Ex026)
- Documentation: doc/ directory with .rst files