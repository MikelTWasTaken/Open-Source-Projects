import pandas as pd
from collections import Counter
import random

# === CONFIGURATION ===
DRAW_FILE_PATH = "/Users/teitelbaumsair/Downloads/euromillions-draw-history.csv"  # <-- Make sure this matches your filename
SUGGESTION_MODE = 'most_frequent'  # Options: 'most_frequent', 'least_frequent', 'random'

# === HELPER FUNCTIONS ===

def load_draw_data(file_path):
    df = pd.read_csv(file_path)
    
    # Extract number columns based on your dataset
    main_cols = ['N1', 'N2', 'N3', 'N4', 'N5']
    star_cols = ['S1', 'S2']
    
    all_main_numbers = df[main_cols].values.flatten()
    all_star_numbers = df[star_cols].values.flatten()
    
    return all_main_numbers, all_star_numbers

def analyze_frequencies(numbers):
    return Counter(numbers)

def get_top_numbers(counter, total_needed, reverse=True):
    sorted_items = counter.most_common()
    if not reverse:
        sorted_items = sorted(counter.items(), key=lambda x: x[1])
    
    return [num for num, _ in sorted_items[:total_needed]]

def suggest_numbers(main_freq, star_freq, mode='most_frequent'):
    if mode == 'most_frequent':
        main_suggestion = get_top_numbers(main_freq, 5, reverse=True)
        star_suggestion = get_top_numbers(star_freq, 2, reverse=True)
    elif mode == 'least_frequent':
        main_suggestion = get_top_numbers(main_freq, 5, reverse=False)
        star_suggestion = get_top_numbers(star_freq, 2, reverse=False)
    elif mode == 'random':
        main_suggestion = random.sample(range(1, 51), 5)
        star_suggestion = random.sample(range(1, 13), 2)
    else:
        raise ValueError("Invalid suggestion mode")

    main_suggestion.sort()
    star_suggestion.sort()
    return main_suggestion, star_suggestion

# === MAIN EXECUTION ===

def main():
    main_numbers, star_numbers = load_draw_data(DRAW_FILE_PATH)
    
    main_freq = analyze_frequencies(main_numbers)
    star_freq = analyze_frequencies(star_numbers)
    
    print("\nTop 10 Main Numbers (Most Frequent):", main_freq.most_common(10))
    print("Top 5 Star Numbers (Most Frequent):", star_freq.most_common(5))

    suggested_main, suggested_star = suggest_numbers(main_freq, star_freq, SUGGESTION_MODE)
    
    print(f"\nSuggested Numbers Based on '{SUGGESTION_MODE}' strategy:")
    print("Main Numbers:", suggested_main)
    print("Star Numbers:", suggested_star)

if __name__ == "__main__":
    main()