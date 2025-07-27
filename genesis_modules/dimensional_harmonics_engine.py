# genesis_modules/dimensional_harmonics_engine.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path

class DimensionalHarmonicsEngine:
    def __init__(self, data: pd.DataFrame):
        self.original_data = data
        self.scaled_data = None
        self.pca = None
        self.pca_result = None
        self.n_components = 2

    def scale_data(self):
        scaler = MinMaxScaler()
        self.scaled_data = scaler.fit_transform(self.original_data)
        return self.scaled_data

    def apply_pca(self, n_components=2):
        self.n_components = n_components
        self.pca = PCA(n_components=n_components)
        self.pca_result = self.pca.fit_transform(self.scaled_data)
        return self.pca_result

    def visualize(self, save_path='outputs/dimensionality_reduction/pca_visual.png'):
        if self.pca_result is None:
            raise ValueError("Run apply_pca() before visualization.")

        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            x=self.pca_result[:, 0],
            y=self.pca_result[:, 1],
            palette="viridis"
        )
        plt.title("PCA Visualization - Dimensional Harmonics")
        plt.xlabel("Principal Component 1")
        plt.ylabel("Principal Component 2")
        plt.tight_layout()

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)
        plt.close()

    def explained_variance(self):
        if self.pca is None:
            raise ValueError("Run apply_pca() first.")
        return self.pca.explained_variance_ratio_

        }
