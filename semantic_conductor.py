# semantic_conductor.py
# Συντονιστής Πολυθεματικών Νοηματικών Οντοτήτων (PSEs) για το KINO Project

class PolyThematicEntity:
    def __init__(self, name, roles):
        self.name = name
        self.roles = roles  # Λίστα από θεματικές αρμοδιότητες
        self.active = True

    def operate(self, context):
        if not self.active:
            return None
        print(f"[{self.name}] Ενεργοποίηση με ρόλους: {', '.join(self.roles)}")
        # Placeholder για λειτουργία με βάση το context του έργου
        return f"{self.name} completed task harmoniously."

class SemanticConductor:
    def __init__(self):
        self.entities = []

    def add_entity(self, name, *roles):
        entity = PolyThematicEntity(name, roles)
        self.entities.append(entity)
        print(f"[Conductor] Προστέθηκε η πολυθεματική οντότητα: {name}")

    def execute_all(self, context="project_flow"):
        results = []
        for entity in self.entities:
            result = entity.operate(context)
            results.append(result)
        return results

# Example Initialization
if __name__ == "__main__":
    conductor = SemanticConductor()
    conductor.add_entity("Da Vinci", "Aesthetic Architect", "Flow Strategist", "Data Artist")
    conductor.add_entity("Boole", "Logic Engineer", "Filter Synthesizer", "Predictive Architect")
    conductor.add_entity("Plato", "Idea Structurer", "Abstract Mapper", "Narrative Framer")
    
    outcomes = conductor.execute_all()
    for out in outcomes:
        print(out)
