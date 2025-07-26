import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

# Φόρτωση των δεδομένων
df = pd.read_csv("kino_data.csv")

# Καθαρισμός των δεδομένων και προετοιμασία
df['winning_numbers'] = df['winning_numbers'].apply(lambda x: [int(i) for i in x.split(',')])  # Διόρθωση μορφής
ticket = [3, 2, 4, 1, 5, 0, 7]  # Παράδειγμα δελτίου

# Υπολογισμός των επιτυχιών για το δελτίο
df['hit_count'] = df['winning_numbers'].apply(lambda x: len(set(ticket) & set(x)))

# Χρήση όλων των αριθμών πλην του 'hit_count' για τα χαρακτηριστικά X και τα αποτελέσματα y
X = df.drop(columns=['hit_count', 'winning_numbers'])
y = df['hit_count']

# Προετοιμασία των δεδομένων (κανονικοποίηση)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Διαχωρισμός σε εκπαιδευτικά και δοκιμαστικά σύνολα
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Δημιουργία του Random Forest μοντέλου
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Προβλέψεις για το δοκιμαστικό σύνολο
y_pred = model.predict(X_test)

# Υπολογισμός των μετρικών
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Εμφάνιση των αποτελεσμάτων
print(f"Ακρίβεια: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}")

# Χρήση Cross-Validation για την αξιολόγηση
cross_val_results = cross_val_score(model, X_scaled, y, cv=5)
print("Αξιολογήσεις με Cross-Validation:", cross_val_results)
print("Μέση ακρίβεια:", cross_val_results.mean())

# Βελτιστοποίηση υπερπαραμέτρων με GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Βέλτιστες παράμετροι
print("Βέλτιστες παράμετροι:", grid_search.best_params_)

# Αξιολόγηση του μοντέλου με τις καλύτερες παραμέτρους
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)
print(f"Βελτιωμένη ακρίβεια με βέλτιστες παραμέτρους: {accuracy_score(y_test, y_pred_best):.2f}")
