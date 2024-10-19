# Macrocosm Visual Engine

## Introduction
The package contains allows to setup Python's standard plotting libraries (`matplotlib`, `plotly`) to create visualizations that are consistent with the Macrocosm project's visual identity.

## Example

After installing the package, import the setup utils
```
from macrocosm_visual.viz_setup import setup_matplotlib, setup_plotly
```

Then, run the setup functions for the desired library. For example, for `matplotlib` run
```
setup_matplotlib()
```
The plots will now be styled according to the Macrocosm project's visual identity.

The `setup_matplotlib` and `setup_plotly` functions return a `VizSetup` object. This
object can be used to customize the visualizations further. `VizSetup` objects can be initialized
with any desired configuration - see `viz-configs-template.yaml` for an example configuration file.
See the docstrings for more information on `VizSetup`.