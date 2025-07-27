# genetic_pattern_modulator.py

import streamlit as st
import numpy as np
import random
import os

def generate_genetic_pattern(seed=None):
    if seed:
        random.seed(seed)
        np.random.seed(seed)
    
    pattern = np.random.choice(range(1, 81), size=20, replace=False)
    return sorted(pattern)

def mutate_pattern(pattern, mutation_rate=0.1):
    mutated = pattern.copy()
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = random.randint(1, 80)
    return sorted(list(set(mutated)))[:20]

def crossover_patterns(p1, p2):
    half = len(p1) // 2
    child = list(set(p1[:half] + p2[half:]))
    while len(child) < 20:
        child.append(random.randint(1, 80))
        child = list(set(child))
    return sorted(child[:20])

def run():
    st.title("🧬 Genetic Pattern Modulator")

    seed = st.number_input("Seed (optional)", min_value=0, value=42)
    mutation_rate = st.slider("Mutation Rate", 0.0, 1.0, 0.1, step=0.05)

    if st.button("Generate Initial Pattern"):
        pattern = generate_genetic_pattern(seed)
        st.success(f"Initial Pattern: {pattern}")

    if st.button("Mutate Pattern"):
        pattern = generate_genetic_pattern(seed)
        mutated = mutate_pattern(pattern, mutation_rate)
        st.info(f"Original: {pattern}")
        st.success(f"Mutated: {mutated}")

    if st.button("Crossover Two Patterns"):
        p1 = generate_genetic_pattern(seed)
        p2 = generate_genetic_pattern(seed + 1)
        child = crossover_patterns(p1, p2)
        st.write(f"Parent 1: {p1}")
        st.write(f"Parent 2: {p2}")
        st.success(f"Child: {child}")
