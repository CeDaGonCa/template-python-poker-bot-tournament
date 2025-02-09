import pandas as pd
import numpy as np

# Load the CSV and clean column names
df = pd.read_csv("parsed.csv")
df.columns = df.columns.str.strip()  # Remove any extra spaces

# Mapping from round names to vectors using numpy arrays
round_to_vector = {
    1: np.array([0, 0, 0]),
    2: np.array([1, 0, 0]),
    3: np.array([0, 1, 0]),
    4: np.array([0, 0, 1])
}

# Initialize an empty list for the new data
new_data = []

# Identify unique rounds by detecting changes in "Round" values
prev_round = None
for i, row in df.iterrows():
    round_num, stack = row["Round"], row["stack"]

    # Convert the round number to a vector using numpy arrays
    round_vector = round_to_vector.get(round_num, np.array([0, 0, 0]))  # Default to [0,0,0] for safety

    # If it's the first occurrence of Round 1, add "Start"
    if round_num == 1 and prev_round != 1:
        new_data.append(["Start", ""])

    # Append the actual data row with the numpy vector
    new_data.append([round_vector.tolist(), stack])  # Convert numpy array to list for CSV compatibility

    # If it's the last occurrence of Round 4 (next row isn't 4 or doesn't exist), add "End"
    if round_num == 4 and (i == len(df) - 1 or df.iloc[i + 1]["Round"] != 4):
        new_data.append(["End", ""])

    prev_round = round_num  # Keep track of the previous round

# Convert the modified list back into a DataFrame
new_df = pd.DataFrame(new_data, columns=df.columns)

# Save back to CSV
new_df.to_csv("parsed_modified.csv", index=False)

print(new_df)  # Debugging: Check output
