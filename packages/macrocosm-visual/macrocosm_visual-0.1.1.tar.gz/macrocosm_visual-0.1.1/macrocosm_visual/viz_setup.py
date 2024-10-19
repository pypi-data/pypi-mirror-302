"""
Setup plotting libraries
"""

from pathlib import Path
from typing import List, Optional

import matplotlib as mpl
import plotly.graph_objects as go
import plotly.io as pio
import yaml

# Get directory of this python file

DIR = Path(__file__).parent.absolute()
VISUAL_CONFIGS_PATH = DIR / "visual_configs.yaml"

_macrocosm_colors = None


def get_macrocosm_colors() -> dict:
    global _macrocosm_colors
    if _macrocosm_colors is not None:
        return _macrocosm_colors
    else:
        with open(VISUAL_CONFIGS_PATH) as f:
            _macrocosm_colors = yaml.safe_load(f)["macrocosm_colors"]
        return _macrocosm_colors


class VizSetup:
    def __init__(self, configs: Optional[str] = None):
        self.configs = configs

    def _get_params(self) -> dict:
        """
        Loads default parameters for boh matplotlib and plotly from a yaml file
        :param configs:
        :return:
        """
        if self.configs is not None:
            with open(self.configs) as f:
                _params = yaml.safe_load(f)
            return _params
        else:
            with open(VISUAL_CONFIGS_PATH) as f:
                _params = yaml.safe_load(f)
            return _params

    def _get_mpl_params(self) -> dict:
        """
        Loads parameters for matplotlib
        """
        if self.configs is not None:
            with open(self.configs) as f:
                _params = yaml.safe_load(f)["matplotlib"]
            return _params
        else:
            with open(VISUAL_CONFIGS_PATH) as f:
                _params = yaml.safe_load(f)["matplotlib"]
            return _params

    def _get_plotly_params(self) -> dict:
        """
        Loads parameters for plotly
        """
        if self.configs is not None:
            with open(self.configs) as f:
                _params = yaml.safe_load(f)["plotly"]
            return _params
        else:
            with open(VISUAL_CONFIGS_PATH) as f:
                _params = yaml.safe_load(f)["plotly"]
            return _params

    def setup_matplotlib(self) -> None:
        custom_rcparams = self._get_mpl_params()

        # Handle the color cycle separately
        if "axes.prop_cycle_colors" in custom_rcparams:
            colors = custom_rcparams.pop("axes.prop_cycle_colors")
            mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=colors)

        mpl.rcParams.update(custom_rcparams)
        return None

    def setup_plotly(self) -> None:
        # plotly_params = self._mpl_params_to_plotly_template()
        plotly_plain = self._get_plotly_params()
        plotly_params = dict(layout=go.Layout(plotly_plain["layout"]), data=plotly_plain["data"])
        pio.templates["macrocosm"] = plotly_params
        pio.templates.default = "macrocosm"
        return None

    @staticmethod
    def to_custom_rotation(colors: List[str]) -> None:

        # For matplotlib
        mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=colors)
        # For plotly
        pio.templates["macrocosm"]["layout"]["colorway"] = colors
        return None

    def to_configs_rotation(self) -> None:
        mpl_params = self._get_mpl_params()
        colors = mpl_params.get("axes.prop_cycle_colors", None)
        if colors is None:
            Warning("No color cycle found in configs")
        else:
            # For matplotlib
            mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=colors)
            # For plotly
            pio.templates["macrocosm"]["layout"]["colorway"] = colors
        return None


def setup_matplotlib(configs: Optional[str] = None) -> VizSetup:
    """
    Setup matplotlib configuration
    """
    vizsetup = VizSetup(configs=configs)
    vizsetup.setup_matplotlib()
    return vizsetup


def setup_plotly(configs: Optional[str] = None) -> VizSetup:
    """
    Setup plotly configuration
    """
    vizsetup = VizSetup(configs=configs)
    vizsetup.setup_plotly()
    return vizsetup
