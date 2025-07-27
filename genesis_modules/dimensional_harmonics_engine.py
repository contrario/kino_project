# genesis_modules/dimensional_harmonics_engine.py

from utils.math_tools import calculate_dimensional_resonance
from core.engines.harmonics_base import HarmonicsBase
from modules.visualizers import render_harmonic_map

class DimensionalHarmonicsEngine(HarmonicsBase):
    """
    Engine that calculates harmonic resonance across dimensional layers
    and renders the output as a harmonic map.
    """

    def __init__(self, input_dimensions, seed_values):
        super().__init__()
        self.input_dimensions = input_dimensions
        self.seed_values = seed_values
        self.harmonic_profile = None

    def compute_harmonics(self):
        """
        Computes the harmonic resonance profile based on dimensions and seed values.
        """
        self.harmonic_profile = calculate_dimensional_resonance(
            self.input_dimensions,
            self.seed_values
        )
        return self.harmonic_profile

    def render(self, output_path=None):
        """
        Renders the harmonic profile as a map or graphic.
        """
        if self.harmonic_profile is None:
            self.compute_harmonics()
        render_harmonic_map(self.harmonic_profile, output_path)

    def export_profile(self):
        """
        Exports the harmonic profile as a dictionary.
        """
        return {
            "dimensions": self.input_dimensions,
            "seeds": self.seed_values,
            "profile": self.harmonic_profile
        }
