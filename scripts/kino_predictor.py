import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import numpy as np

# --- ΜΕΡΟΣ 1: ΦΟΡΤΩΣΗ & ΠΡΟΕΤΟΙΜΑΣΙΑ ΔΕΔΟΜΕΝΩΝ (ΒΗΜΑ-ΒΗΜΑ) ---

print("Βήμα 1.1: Φόρτωση δεδομένων από το 'kino_data.csv'...")
# Φόρτωση των δεδομένων από το αρχείο CSV.
# Υποθέτουμε ότι το αρχείο έχει στήλες 'draw_id' και 'winning_numbers'.
try:
    df = pd.read_csv("kino_data.csv")
    print(f"Επιτυχής φόρτωση. Το αρχείο περιέχει {len(df)} κληρώσεις.")
    print("Οι πρώτες 5 γραμμές του αρχείου:")
    print(df.head())
except FileNotFoundError:
    print("ΣΦΑΛΜΑ: Το αρχείο 'kino_data.csv' δεν βρέθηκε στον ίδιο φάκελο με τον κώδικα.")
    print("Παρακαλώ βεβαιωθείτε ότι το αρχείο υπάρχει και είναι στο σωστό σημείο.")
    exit()

print("\nΒήμα 1.2: Μετατροπή των κερδισμένων αριθμών σε λίστες ακεραίων και ταξινόμηση...")
# Μετατρέπουμε τη στήλη 'winning_numbers' από συμβολοσειρά (π.χ. "1,25,32") σε λίστα ακεραίων.
df['winning_numbers'] = df['winning_numbers'].apply(lambda x: [int(i) for i in x.split(',')])

# Πολύ σημαντικό: Ταξινομούμε τις κληρώσεις με βάση το 'draw_id' για να διασφαλίσουμε τη χρονολογική σειρά.
# Αυτό είναι ΚΡΙΣΙΜΟ για την ορθή δημιουργία χαρακτηριστικών και τον χρονολογικό διαχωρισμό.
df = df.sort_values(by='draw_id').reset_index(drop=True)
print("Οι αριθμοί μετατράπηκαν σε λίστες και οι κληρώσεις ταξινομήθηκαν χρονολογικά.")
print(f"Η πρώτη κλήρωση έχει draw_id: {df['draw_id'].min()} και η τελευταία: {df['draw_id'].max()}")

print("\nΒήμα 1.3: Δημιουργία εκτεταμένου DataFrame για Feature Engineering...")
# Δημιουργούμε ένα νέο DataFrame όπου κάθε γραμμή θα αντιστοιχεί σε έναν πιθανό αριθμό
# για μια συγκεκριμένη κλήρωση (π.χ., Κλήρωση 1 - Αριθμός 1, Κλήρωση 1 - Αριθμός 2, ..., Κλήρωση 1 - Αριθμός 80).
all_numbers = range(1, 81) # Οι αριθμοί του KINO είναι από 1 έως 80.
data_for_model = []

for i in range(len(df)):
    current_draw_id = df.loc[i, 'draw_id']
    current_winning_numbers = df.loc[i, 'winning_numbers']

    for number in all_numbers:
        row = {
            'draw_id': current_draw_id,
            'number': number,
            # Ο στόχος μας (y): Είναι αυτός ο αριθμός στους κερδισμένους αριθμούς της τρέχουσας κλήρωσης;
            'is_winning': 1 if number in current_winning_numbers else 0
        }
        data_for_model.append(row)

model_df = pd.DataFrame(data_for_model)
print(f"Δημιουργήθηκε ένα νέο DataFrame με {len(model_df)} γραμμές (Κλήρωση x Αριθμός).")
print("Οι πρώτες 5 γραμμές του νέου DataFrame:")
print(model_df.head())

print("\nΒήμα 1.4: Δημιουργία ΠΙΟ ΠΟΛΛΩΝ & ΚΑΛΥΤΕΡΩΝ Χαρακτηριστικών (Feature Engineering) βασισμένων σε Ιστορικά Δεδομένα...")
# Εδώ βελτιώνουμε τα χαρακτηριστικά μας.
# Θα υπολογίσουμε τη συχνότητα εμφάνισης και την "καθυστέρηση" κάθε αριθμού
# σε διαφορετικά χρονικά παράθυρα για να δώσουμε περισσότερες πληροφορίες στο μοντέλο.

# Αρχικοποιούμε στήλες για τα νέα χαρακτηριστικά.
model_df['freq_past_5_draws'] = 0.0
model_df['freq_past_10_draws'] = 0.0
model_df['freq_past_20_draws'] = 0.0
model_df['draws_since_last_appearance'] = 0
model_df['avg_freq_all_time'] = 0.0 # Μέση συχνότητα εμφάνισης αριθμού μέχρι την τρέχουσα κλήρωση

# Για κάθε αριθμό και για κάθε κλήρωση, υπολογίζουμε τα χαρακτηριστικά του από ΠΡΟΗΓΟΥΜΕΝΕΣ κληρώσεις.
# Αυτή η διαδικασία μπορεί να είναι χρονοβόρα για μεγάλα datasets.
total_rows = len(model_df)
for i in range(total_rows):
    current_draw_id = model_df.loc[i, 'draw_id']
    current_number = model_df.loc[i, 'number']

    # Προσοχή: Εδώ επιλέγουμε κληρώσεις αυστηρά ΠΡΙΝ την τρέχουσα κλήρωση (current_draw_id)
    # για να μην υπάρχει "διαρροή" πληροφοριών από το μέλλον.
    past_draws_df_relevant = df[df['draw_id'] < current_draw_id]

    if not past_draws_df_relevant.empty:
        # Συχνότητα εμφάνισης στις τελευταίες 5, 10, 20 κληρώσεις
        windows = [5, 10, 20]
        for window_size in windows:
            last_N_draws = past_draws_df_relevant.tail(window_size)
            if not last_N_draws.empty:
                count = sum(1 for nums in last_N_draws['winning_numbers'] if current_number in nums)
                model_df.loc[i, f'freq_past_{window_size}_draws'] = count / len(last_N_draws)
            else:
                model_df.loc[i, f'freq_past_{window_size}_draws'] = 0.0 # Αν δεν υπάρχουν αρκετές προηγούμενες κληρώσεις

        # Αριθμός κληρώσεων από την τελευταία εμφάνιση (Draws Since Last Appearance)
        past_appearances = past_draws_df_relevant[past_draws_df_relevant['winning_numbers'].apply(lambda x: current_number in x)]
        if not past_appearances.empty:
            last_appearance_draw_id = past_appearances['draw_id'].max()
            model_df.loc[i, 'draws_since_last_appearance'] = current_draw_id - last_appearance_draw_id
        else:
            # Αν δεν έχει εμφανιστεί ποτέ πριν, βάζουμε μια μεγάλη τιμή
            model_df.loc[i, 'draws_since_last_appearance'] = current_draw_id - df['draw_id'].min() + 1 # Συνολικές κληρώσεις που έχει "χάσει"

        # Μέση συχνότητα εμφάνισης όλων των εποχών (μέχρι την τρέχουσα)
        total_draws_so_far = len(past_draws_df_relevant)
        if total_draws_so_far > 0:
            total_appearances = sum(1 for nums in past_draws_df_relevant['winning_numbers'] if current_number in nums)
            model_df.loc[i, 'avg_freq_all_time'] = total_appearances / total_draws_so_far
    else:
        # Για τις πολύ πρώτες κληρώσεις που δεν έχουν προηγούμενο ιστορικό
        model_df.loc[i, ['freq_past_5_draws', 'freq_past_10_draws', 'freq_past_20_draws', 'draws_since_last_appearance', 'avg_freq_all_time']] = 0.0, 0.0, 0.0, df['draw_id'].min(), 0.0


# Αφαιρούμε τις γραμμές όπου το 'draws_since_last_appearance' είναι μηδέν (σημαίνει ότι δεν υπήρχε προηγούμενη κλήρωση για υπολογισμό)
# Ή, καλύτερα, τις γραμμές που αντιστοιχούν στις πρώτες κληρώσεις (π.χ., 20 πρώτες)
# για τις οποίες δεν έχουμε πλήρη χαρακτηριστικά (π.χ. freq_past_20_draws).
# Για απλότητα, θα κρατήσουμε μόνο γραμμές όπου το 'draw_id' είναι αρκετά μεγάλο ώστε να έχουν υπολογιστεί τα χαρακτηριστικά
min_draw_id_for_features = df['draw_id'].min() + 20 # Θεωρούμε ότι χρειαζόμαστε 20 προηγούμενες κληρώσεις για το freq_past_20_draws
model_df = model_df[model_df['draw_id'] > min_draw_id_for_features].copy()


print("Δημιουργήθηκαν περισσότερα και καλύτερα χαρακτηριστικά.")
print("Οι πρώτες 5 γραμμές του DataFrame με χαρακτηριστικά:")
print(model_df.head())
print(f"Συνολικές γραμμές μετά τη δημιουργία χαρακτηριστικών: {len(model_df)}")


# --- ΜΕΡΟΣ 2: ΠΡΟΕΤΟΙΜΑΣΙΑ ΓΙΑ ΤΟ ΜΟΝΤΕΛΟ ---

print("\nΒήμα 2.1: Ορισμός Χαρακτηριστικών (X) και Στόχου (y)...")
# X: Τα χαρακτηριστικά που θα χρησιμοποιήσει το μοντέλο για να κάνει προβλέψεις.
# Τώρα έχουμε περισσότερα χαρακτηριστικά!
X = model_df[['freq_past_5_draws', 'freq_past_10_draws', 'freq_past_20_draws',
              'draws_since_last_appearance', 'avg_freq_all_time']]

# y: Ο στόχος που θέλουμε να προβλέψουμε (αν ο αριθμός είναι κερδισμένος στην τρέχουσα κλήρωση).
y = model_df['is_winning']

print("Χαρακτηριστικά (X) και Στόχος (y) ορίστηκαν.")
print(f"Σχήμα του X: {X.shape}")
print(f"Σχήμα του y: {y.shape}")

print("\nΒήμα 2.2: Κανονικοποίηση των Χαρακτηριστικών (StandardScaler)...")
# Η κανονικοποίηση βοηθά πολλά μοντέλα μηχανικής μάθησης να λειτουργούν καλύτερα.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Τα χαρακτηριστικά κανονικοποιήθηκαν.")

print("\nΒήμα 2.3: ΧΡΟΝΟΛΟΓΙΚΟΣ Διαχωρισμός Δεδομένων σε Εκπαιδευτικό και Δοκιμαστικό Σύνολο...")
# Αυτό είναι μια σημαντική βελτίωση! Αντί για τυχαίο split, χωρίζουμε τα δεδομένα χρονολογικά.
# Εκπαιδεύουμε σε παλαιότερες κληρώσεις και δοκιμάζουμε σε νεότερες.
split_point = int(len(X_scaled) * 0.8) # Χωρίζουμε στο 80% των δεδομένων.
X_train = X_scaled[:split_point]
y_train = y[:split_point]
X_test = X_scaled[split_point:]
y_test = y[split_point:]

print("Τα δεδομένα διαχωρίστηκαν χρονολογικά επιτυχώς.")
print(f"Μέγεθος εκπαιδευτικού συνόλου (X_train): {X_train.shape}")
print(f"Μέγεθος δοκιμαστικού συνόλου (X_test): {X_test.shape}")
print("Σημείωση: Το εκπαιδευτικό σύνολο περιέχει παλαιότερες κληρώσεις, το δοκιμαστικό νεότερες.")


# --- ΜΕΡΟΣ 3: ΜΟΝΤΕΛΟΠΟΙΗΣΗ & ΑΞΙΟΛΟΓΗΣΗ ---

print("\nΒήμα 3.1: Εκπαίδευση του Random Forest Μοντέλου...")
model = RandomForestClassifier(n_estimators=500, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)
print("Το Random Forest μοντέλο εκπαιδεύτηκε επιτυχώς.")

print("\nΒήμα 3.2: Προβλέψεις στο Δοκιμαστικό Σύνολο και Αξιολόγηση Μετρικών...")
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='binary')
recall = recall_score(y_test, y_pred, average='binary')
f1 = f1_score(y_test, y_pred, average='binary')

print(f"\nΑποτελέσματα Αξιολόγησης (Πρόβλεψη αν ένας αριθμός θα κληρωθεί):")
print(f"  Ακρίβεια (Accuracy): {accuracy:.4f} (Ποσοστό σωστών προβλέψεων συνολικά)")
print(f"  Precision: {precision:.4f} (Από τους αριθμούς που προβλέψαμε ότι θα κληρωθούν (True Positives), πόσοι πραγματικά κληρώθηκαν)")
print(f"  Recall: {recall:.4f} (Από τους αριθμούς που πραγματικά κληρώθηκαν (Actual Positives), πόσους προβλέψαμε)")
print(f"  F1-Score: {f1:.4f} (Μέση τιμή Precision και Recall - καλός δείκτης για ανισόρροπα δεδομένα)")

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)
print("  [[True Negatives (TN)  False Positives (FP)]")
print("   [False Negatives (FN) True Positives (TP)]]")
print("  Ανάλυση:")
print(f"    - {cm[0,0]} Σωστά Μη-Κερδισμένοι (True Negatives): Αριθμοί που δεν κληρώθηκαν και το μοντέλο σωστά προέβλεψε ότι δεν θα κληρωθούν.")
print(f"    - {cm[0,1]} Λάθος Προβλέψεις Κερδισμένων (False Positives): Αριθμοί που δεν κληρώθηκαν, αλλά το μοντέλο ΛΑΘΟΣ προέβλεψε ότι θα κληρωθούν. Αυτοί είναι οι 'χαμένοι' αριθμοί στα δελτία μας.")
print(f"    - {cm[1,0]} Λάθος Προβλέψεις Μη-Κερδισμένων (False Negatives): Αριθμοί που κληρώθηκαν, αλλά το μοντέλο ΛΑΘΟΣ προέβλεψε ότι ΔΕΝ θα κληρωθούν. Αυτοί είναι οι 'χαμένοι' κερδισμένοι αριθμοί.")
print(f"    - {cm[1,1]} Σωστά Κερδισμένοι (True Positives): Αριθμοί που κληρώθηκαν και το μοντέλο σωστά προέβλεψε ότι θα κληρωθούν. Αυτοί είναι οι 'χτυπημένοι' αριθμοί στα δελτία μας.")


print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nΕρμηνεία Classification Report:")
print("- Το Precision για το '1' (κερδισμένοι αριθμοί) δείχνει πόσο αξιόπιστες είναι οι προβλέψεις μας όταν λέμε ότι ένας αριθμός θα κληρωθεί.")
print("- Το Recall για το '1' δείχνει πόσους από τους πραγματικούς κερδισμένους αριθμούς καταφέραμε να εντοπίσουμε.")
print("- Το F1-score είναι μια μέση τιμή αυτών των δύο και είναι καλός δείκτης για ανισόρροπα δεδομένα.")

# Το Cross-Validation με time-series split είναι πιο περίπλοκο και απαιτεί ειδικές τεχνικές (π.χ. TimeSeriesSplit).
# Για την ώρα, αφήνουμε την απλή μορφή του cross_val_score, αλλά σημειώνουμε την ανάγκη για TimeSeriesSplit για πιο ακριβή αποτελέσματα.
print("\nΒήμα 3.3: Αξιολόγηση με Cross-Validation (Απλή Μορφή - απαιτείται TimeSeriesSplit για βέλτιστα αποτελέσματα)...")
# Προσοχή: Το απλό cross_val_score μπορεί να "διαρρεύσει" πληροφορίες από το μέλλον αν δεν χρησιμοποιηθεί
# ειδικός splitter για χρονοσειρές όπως το TimeSeriesSplit. Για την ώρα, το αφήνουμε για επίδειξη.
# cross_val_results = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
# print(f"  Αξιολογήσεις με Cross-Validation (Accuracy σε κάθε 'fold'): {cross_val_results}")
# print(f"  Μέση ακρίβεια Cross-Validation: {cross_val_results.mean():.4f}")
print("  (Παραλείφθηκε το απλό Cross-Validation για την ώρα λόγω φύσης χρονοσειρών. Θα το συζητήσουμε αν χρειαστεί ειδικό splitter.)")


print("\nΒήμα 3.4: Βελτιστοποίηση Υπερπαραμέτρων με GridSearchCV...")
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5]
}

# Επειδή το GridSearchCV κάνει τυχαίους διαχωρισμούς (folds), μπορεί να μην είναι ιδανικό για χρονοσειρές.
# Για πιο ακριβή βελτιστοποίηση σε χρονοσειρές, θα χρειαζόταν το TimeSeriesSplit και εδώ.
# Το n_jobs=-1 χρησιμοποιεί όλους τους πυρήνες CPU για ταχύτερη εκτέλεση.
grid_search = GridSearchCV(RandomForestClassifier(random_state=42, class_weight='balanced'), param_grid, cv=3, scoring='f1', n_jobs=-1)
grid_search.fit(X_train, y_train)

print(f"\n  Βέλτιστες παράμετροι που βρέθηκαν: {grid_search.best_params_}")

best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)
print(f"  Βελτιωμένη ακρίβεια με βέλτιστες παραμέτρους: {accuracy_score(y_test, y_pred_best):.4f}")
print(f"  Βελτιωμένο F1-Score με βέλτιστες παραμέτρους: {f1_score(y_test, y_pred_best, average='binary'):.4f}")


print("\nΒήμα 3.5: Σημαντικότητα Χαρακτηριστικών...")
feature_importances = best_model.feature_importances_
feature_names = X.columns
for i, feature in enumerate(feature_names):
    print(f"  Χαρακτηριστικό: {feature}, Σημαντικότητα: {feature_importances[i]:.4f}")
print("\nΕρμηνεία Σημαντικότητας Χαρακτηριστικών:")
print("  Αυτοί οι αριθμοί δείχνουν ποια από τα χαρακτηριστικά (όπως η συχνότητα ή η καθυστέρηση) το μοντέλο βρήκε πιο χρήσιμα για την πρόβλεψη.")
print("  Όσο υψηλότερη η τιμή, τόσο πιο σημαντικό ήταν το χαρακτηριστικό για το μοντέλο.")


# --- ΜΕΡΟΣ 4: ΠΩΣ ΝΑ ΚΑΝΕΤΕ ΠΡΟΒΛΕΨΕΙΣ ΓΙΑ ΤΗΝ ΕΠΟΜΕΝΗ ΚΛΗΡΩΣΗ ---

print("\n--- ΜΕΡΟΣ 4: ΠΩΣ ΝΑ ΚΑΝΕΤΕ ΠΡΟΒΛΕΨΕΙΣ ΓΙΑ ΤΗΝ ΕΠΟΜΕΝΗ ΚΛΗΡΩΣΗ ---")
print("Βήμα 4.1: Προετοιμασία δεδομένων για την επόμενη (μελλοντική) κλήρωση...")
# Για να προβλέψετε τους αριθμούς για την επόμενη κλήρωση, πρέπει να υπολογίσετε
# τα χαρακτηριστικά (features) για κάθε αριθμό (1-80) με βάση ΟΛΕΣ τις κληρώσεις ΠΟΥ ΕΧΟΥΝ ΗΔΗ ΓΙΝΕΙ.

last_known_draw_id = df['draw_id'].max()
data_for_next_prediction = []

print(f"Υπολογισμός χαρακτηριστικών για την πρόβλεψη της κλήρωσης μετά το Draw ID: {last_known_draw_id}")

for number in all_numbers:
    row = {'number': number}

    # Δεδομένα από ΟΛΕΣ τις προηγούμενες κληρώσεις (μέχρι την τελευταία γνωστή)
    all_past_draws = df[df['draw_id'] <= last_known_draw_id]

    if not all_past_draws.empty:
        # Συχνότητα εμφάνισης στις τελευταίες 5, 10, 20 κληρώσεις
        windows = [5, 10, 20]
        for window_size in windows:
            last_N_known_draws = all_past_draws.tail(window_size)
            if not last_N_known_draws.empty:
                count = sum(1 for nums in last_N_known_draws['winning_numbers'] if number in nums)
                row[f'freq_past_{window_size}_draws'] = count / len(last_N_known_draws)
            else:
                row[f'freq_past_{window_size}_draws'] = 0.0

        # Αριθμός κληρώσεων από την τελευταία εμφάνιση
        past_appearances = all_past_draws[all_past_draws['winning_numbers'].apply(lambda x: number in x)]
        if not past_appearances.empty:
            last_appearance_draw_id = past_appearances['draw_id'].max()
            row['draws_since_last_appearance'] = last_known_draw_id - last_appearance_draw_id
        else:
            row['draws_since_last_appearance'] = last_known_draw_id - df['draw_id'].min() + 1 # Αν δεν έχει εμφανιστεί ποτέ

        # Μέση συχνότητα εμφάνισης όλων των εποχών
        total_draws_so_far = len(all_past_draws)
        if total_draws_so_far > 0:
            total_appearances = sum(1 for nums in all_past_draws['winning_numbers'] if number in nums)
            row['avg_freq_all_time'] = total_appearances / total_draws_so_far
        else:
            row['avg_freq_all_time'] = 0.0
    else:
        # Αν δεν υπάρχουν καθόλου προηγούμενες κληρώσεις (πρακτικά απίθανο)
        row['freq_past_5_draws'] = 0.0
        row['freq_past_10_draws'] = 0.0
        row['freq_past_20_draws'] = 0.0
        row['draws_since_last_appearance'] = df['draw_id'].min()
        row['avg_freq_all_time'] = 0.0

    data_for_next_prediction.append(row)

next_draw_features = pd.DataFrame(data_for_next_prediction)

# Κανονικοποιούμε τα νέα δεδομένα χρησιμοποιώντας τον ίδιο scaler που εκπαιδεύτηκε πριν.
# ΠΡΟΣΟΧΗ: ΠΟΤΕ μην κάνετε fit_transform σε νέα δεδομένα, μόνο transform!
X_predict = scaler.transform(next_draw_features[['freq_past_5_draws', 'freq_past_10_draws', 'freq_past_20_draws',
                                                'draws_since_last_appearance', 'avg_freq_all_time']])

print("  Χαρακτηριστικά για την επόμενη κλήρωση υπολογίστηκαν και κανονικοποιήθηκαν.")
print("  Πρώτες 5 γραμμές χαρακτηριστικών για πρόβλεψη:")
print(next_draw_features.head())

print("\nΒήμα 4.2: Πρόβλεψη πιθανότητας εμφάνισης για κάθε αριθμό...")
probabilities = best_model.predict_proba(X_predict)[:, 1] # Παίρνουμε την πιθανότητα για την κλάση 1 (κερδισμένος)

predictions_df = pd.DataFrame({'number': all_numbers, 'probability': probabilities})
predictions_df = predictions_df.sort_values(by='probability', ascending=False).reset_index(drop=True)

print("Οι αριθμοί ταξινομήθηκαν κατά σειρά προβλεπόμενης πιθανότητας εμφάνισης:")
print(predictions_df.head(20)) # Εμφανίζουμε τους 20 πιο πιθανούς αριθμούς

print("\nΤΕΛΟΣ ΕΚΤΕΛΕΣΗΣ ΚΩΔΙΚΑ.")
print("\n--- ΣΗΜΑΝΤΙΚΗ ΠΑΡΑΤΗΡΗΣΗ ΓΙΑ ΤΗΝ ΑΠΟΔΟΣΗ ΤΟΥ ΜΟΝΤΕΛΟΥ ---")
print("Τα αποτελέσματα αξιολόγησης (Accuracy, Precision, Recall, F1-Score) δείχνουν ότι το μοντέλο δεν έχει πολύ υψηλή προβλεπτική δύναμη.")
print("Αυτό οφείλεται κυρίως σε δύο λόγους:")
print("1. ΦΥΣΗ ΤΟΥ ΠΑΙΧΝΙΔΙΟΥ: Το KINO είναι ένα παιχνίδι τυχαίας κλήρωσης. Είναι εξαιρετικά δύσκολο, αν όχι αδύνατο, να προβλέψεις πραγματικά τους αριθμούς του.")
print("2. ΜΙΚΡΟ ΜΕΓΕΘΟΣ ΔΕΔΟΜΕΝΩΝ: Με μόνο 99 κληρώσεις (που μεταφράζονται σε 7920 γραμμές δεδομένων για το μοντέλο), το μοντέλο δεν έχει αρκετά δεδομένα για να βρει ισχυρά στατιστικά μοτίβα, ακόμα και αν αυτά υπήρχαν.")
print("Συνήθως, σε τέτοια προβλήματα, χρειαζόμαστε δεκάδες ή εκατοντάδες χιλιάδες κληρώσεις.")
print("\nΠαρόλα αυτά, ο κώδικας υλοποιεί σωστά τις τεχνικές Machine Learning για τον τύπο δεδομένων σας.")
print("Οι 'προβλεπόμενες δεκάδες' που εμφανίζονται στο τέλος είναι οι αριθμοί που το μοντέλο θεωρεί πιο πιθανούς με βάση την ιστορία τους και τα χαρακτηριστικά που δημιουργήσαμε.")