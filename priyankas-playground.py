from dotenv import load_dotenv
import os
import requests
from datasets import load_dataset
from math_arena_datasets import categories_2025
import pandas as pd
from sklearn.model_selection import train_test_split
from time import sleep
from openai import AzureOpenAI
import re

load_dotenv()
API_URL = os.environ.get("AZURE_OPENAI_ENDPOINT")
API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")

# --- Build the few-shot prompt ---
def build_prompt(examples, query):
    categories = [
        "Arithmetic", "Algebra", "Geometry",
        "Combinatorics", "Number Theory", "Probability"
    ]
    
    prompt = (
        "You are a math problem classifier.\n"
        f"Your task is to assign each problem to exactly one of these categories:\n"
        f"{', '.join(categories)}.\n"
        "Respond with only the category name.\n\n"
    )
    
    for _, row in examples.iterrows():
        prompt += f"### Example\nProblem: {row['problem']}\nCategory: {row['problem_type']}\n\n"
    
    prompt += f"### Classify this new problem\nProblem: {query}\nCategory:"
    return prompt

def classify_with_azure(prompt):
    client = AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2024-12-01-preview",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    )

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Error:", e)
        return ""
    
def flatten_concatenated_labels(x):
    x = str(x).strip()
    # Split by uppercase letters (assumes each label starts with a capital)
    labels = re.findall(r'[A-Z][a-zA-Z\s]*', x)
    if labels:
        return labels[0].strip()  # first label
    return x

# --- Load and merge all datasets ---
dfs = []
for path in categories_2025:
    dataset_dict = load_dataset(path)
    split = list(dataset_dict.keys())[0]
    df_split = dataset_dict[split].to_pandas()
    dfs.append(df_split)

df = pd.concat(dfs, ignore_index=True)
df["problem_type"] = df["problem_type"].apply(lambda x: x[0] if isinstance(x, list) else x)

# Drop null values
df = df[["problem", "problem_type"]].dropna()

# Train test split
train_df, test_df = pd.read_csv('data/problem_type_data.train.csv'), pd.read_csv('data/problem_type_data.test.csv')

train_df['problem_type'] = train_df['problem_type'].apply(flatten_concatenated_labels)
test_df['problem_type'] = test_df['problem_type'].apply(flatten_concatenated_labels)

# Using few-shot ICL Learning
correct = 0

for _, row in test_df.iterrows():
    few_shots = train_df.sample(5, random_state=None)
    prompt = build_prompt(few_shots, row["problem"])
    predicted = classify_with_azure(prompt)

    # Normalize predicted output
    predicted = predicted.strip().replace("Category:", "").strip()

    # Handle case where actual label is a list
    actual = row["problem_type"]
    if isinstance(actual, list):
        actual = actual[0]

    print(f"Predicted: {predicted} | Actual: {actual}")

    # Case-insensitive match
    if predicted.lower() == actual.lower():
        correct += 1

accuracy = correct / len(test_df)
print(f"\nAccuracy: {accuracy:.2%}")
