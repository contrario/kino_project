
import random

class PSEAutoGenerator:
    def __init__(self, context):
        self.context = context

    def generate_pse(self):
        pse_list = []
        pse_name = self._generate_name()
        specialties = self._assign_specialties()
        pse_list.append({
            "name": pse_name,
            "specialties": specialties,
            "origin": "Auto-Generated",
            "project_context": self.context
        })
        return pse_list

    def _generate_name(self):
        prefixes = ["Neo", "Meta", "Quantum", "Syn", "Trans"]
        suffixes = ["Nexus", "Core", "Mind", "Loop", "Agent"]
        return random.choice(prefixes) + random.choice(suffixes)

    def _assign_specialties(self):
        specialty_pool = [
            "Pattern Recognition",
            "Fractal Forecasting",
            "Visual Semantics",
            "Probabilistic Strategy",
            "Color Psychology",
            "Bayesian Estimation",
            "Emotive Mapping",
            "Sequential Intelligence"
        ]
        return random.sample(specialty_pool, 3)
