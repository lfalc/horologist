import pandas as pd
import random

def calculate_ranking(input_file):
    """
    Calculates the ranking of the participants based on their answers to the questions.
    :param input_file: The path to the input file.
    """
    questions = ['Wie schätzen sie den Preis der ersten Uhr ein?',
                 'Wie schätzen sie den Preis der zweiten Uhr ein?',
                 'Wie schätzen sie den Preis der dritten Uhr ein?',
                 'Wie schätzen sie den Preis der vierten Uhr ein?']
    prices = [6000, 15000, 12000, 300]

    # Read data
    df = pd.read_csv(input_file, sep=',', header=0)
    df_sorted = df.sort_values('Teilnehmer Nummer')
    points = {}

    for question, price in zip(questions, prices):
        values = df_sorted[question]
        differences = values - price
        absolute_differences = differences.abs()
        percentage_differences = (absolute_differences / price) * 100
        participant_points = 20 - (percentage_differences.rank(method='first', ascending=True))
        participant_points = participant_points.astype(int)
        column_name = f'Points - {question}'
        points[column_name] = participant_points

    df_points = pd.DataFrame(points)
    df_points['Total Points'] = df_points.sum(axis=1)

    # Handle ties randomly
    random.seed(42)  # Set a seed for reproducibility
    df_points['Total Points'] += [random.random() * 0.0001 for _ in range(len(df_points))]
    df_points['Total Points'] = df_points['Total Points'].astype(int)
    df_points['Teilnehmer Nummer'] = df_sorted['Teilnehmer Nummer']
    df_points_sorted = df_points.sort_values('Total Points', ascending=True)
    df_points_sorted = df_points_sorted[['Teilnehmer Nummer', 'Total Points']]  # Keep only these columns
    output_file = 'Fragen Eyetracking Ranking.json'
    df_points_sorted.to_json(output_file, orient='records', index=False)
    print(f"Ranking has been saved to '{output_file}'.")
    
    return df_points_sorted



if __name__ == "__main__":
    input_file = 'Fragen Eyetracking.csv'
    calculate_ranking(input_file)