import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split

# 1. Load and preprocess data
def load_data(file_path):
    df = pd.read_csv(file_path)
    main_numbers = df[['N1', 'N2', 'N3', 'N4', 'N5']]
    lucky_stars = df[['S1', 'S2']]
    return df, main_numbers, lucky_stars

# 2. Analyze frequency
def number_frequencies(numbers_df, number_range):
    all_numbers = numbers_df.to_numpy().flatten()
    freq = pd.Series(all_numbers).value_counts().sort_index()
    return freq.reindex(range(1, number_range + 1), fill_value=0)

# 3. Create features and labels
def create_features_labels(numbers_df, number_range):
    mlb = MultiLabelBinarizer(classes=range(1, number_range + 1))
    X = numbers_df.shift(1).dropna().apply(lambda row: sorted(set(row.dropna().astype(int))), axis=1)
    y = numbers_df.dropna().apply(lambda row: sorted(set(row.dropna().astype(int))), axis=1)
    X_bin = mlb.fit_transform(X)
    y_bin = mlb.transform(y)
    return X_bin, y_bin, mlb

# 4. Train model
def train_model(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

# 5. Predict probabilities for each number
def predict_probabilities(model, X_latest, mlb):
    probs = model.predict_proba([X_latest])[0]
    return dict(zip(mlb.classes_, probs))

# 6. Generate random ticket
def generate_ticket():
    main = sorted(random.sample(range(1, 51), 5))
    stars = sorted(random.sample(range(1, 13), 2))
    return main, stars

# 7. Annotate with probabilities
def annotate_ticket(main, stars, main_probs, star_probs):
    annotated_main = [(n, round(main_probs.get(n, 0), 4)) for n in main]
    annotated_stars = [(s, round(star_probs.get(s, 0), 4)) for s in stars]
    return annotated_main, annotated_stars

# 8. Visualize
def plot_distribution(freq, title):
    plt.figure(figsize=(12, 4))
    sns.barplot(x=freq.index, y=freq.values)
    plt.title(title)
    plt.xlabel("Number")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

# ---- MAIN PROGRAM ---- #
if __name__ == "__main__":
    # Load data
    df, main_numbers, lucky_stars = load_data("/Users/teitelbaumsair/Downloads/euromillions-draw-history.csv")

    # Frequency plots
    main_freq = number_frequencies(main_numbers, 50)
    star_freq = number_frequencies(lucky_stars, 12)
    plot_distribution(main_freq, "Main Numbers Frequency (Last 180 Days)")
    plot_distribution(star_freq, "Lucky Stars Frequency (Last 180 Days)")

    # Prepare model data
    X_main, y_main, mlb_main = create_features_labels(main_numbers, 50)
    X_star, y_star, mlb_star = create_features_labels(lucky_stars, 12)

    # Train models
    model_main = train_model(X_main, y_main)
    model_star = train_model(X_star, y_star)

    # Predict probabilities from the last known draw
    X_latest_main = X_main[-1]
    X_latest_star = X_star[-1]
    main_probs = predict_probabilities(model_main, X_latest_main, mlb_main)
    star_probs = predict_probabilities(model_star, X_latest_star, mlb_star)

    # Generate ticket
    main_ticket, star_ticket = generate_ticket()
    annotated_main, annotated_star = annotate_ticket(main_ticket, star_ticket, main_probs, star_probs)

    # Display result
    print("\n🎟️  Your EuroMillions Ticket:")
    print("Main Numbers:", annotated_main)
    print("Lucky Stars:", annotated_star)