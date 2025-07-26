# pse_neural_net.py
# Νευρωνικό Πρωτόκολλο Συνεργασίας PSEs – Kino Project Neural Harmony Layer

class NeuralPSE:
    def __init__(self, name, specialties):
        self.name = name
        self.specialties = specialties
        self.knowledge = {}
        self.connections = []

    def connect(self, other_pse):
        self.connections.append(other_pse)
        print(f"{self.name} ↔ {other_pse.name} connection established.")

    def share(self, topic, data):
        self.knowledge[topic] = data
        for conn in self.connections:
            conn.receive(topic, data)

    def receive(self, topic, data):
        if topic not in self.knowledge:
            self.knowledge[topic] = data
            print(f"{self.name} received new insight on '{topic}'.")

    def act(self):
        for topic, data in self.knowledge.items():
            print(f"{self.name} analyzing {topic} with specialties {self.specialties}...")

# Example usage
if __name__ == "__main__":
    plato = NeuralPSE("Plato", ["Abstract Design", "Ethical Flow"])
    tesla = NeuralPSE("Tesla", ["Innovation", "Streamlining"])
    gauss = NeuralPSE("Gauss", ["Predictive Structures", "Mathematical Optimization"])

    plato.connect(tesla)
    tesla.connect(gauss)

    plato.share("KINO Prediction Harmony", {"weights": [0.33, 0.45, 0.22]})
    tesla.act()
    gauss.act()
