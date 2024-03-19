import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load the dataset
file_path = 'csgo_data.csv'  
df = pd.read_csv(file_path)

# Initial Data Exploration
print(df.head())
print(df.columns)
print(df.isnull().sum())

# Visualization Function
def plot_data(df, x, hue=None, kind="count", figsize=(20, 16)):
    plt.figure(figsize=figsize)
    if kind == "count":
        sns.countplot(x=x, hue=hue, data=df)
    elif kind == "bar":
        sns.barplot(x=df[x].value_counts().index, y=df[x].value_counts().values)
    plt.show()

# Feature Engineering
df.drop(columns=[col for col in df.columns if df[col].nunique() == 1], inplace=True)

# Encode Categorical Data
label_encoder = LabelEncoder()
df['bomb_planted'] = label_encoder.fit_transform(df['bomb_planted'])
df['round_winner'] = label_encoder.fit_transform(df['round_winner'])

# One-Hot Encoding
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_df = pd.DataFrame(OH_encoder.fit_transform(df[['map']]))
OH_cols_df.columns = OH_encoder.get_feature_names_out(['map'])
df = pd.concat([df.drop(['map'], axis=1), OH_cols_df], axis=1)

# Prepare for Modeling
X = df.drop('round_winner', axis=1)
y = df['round_winner']

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine Optimal Number of Clusters (KMeans)
def find_optimal_clusters(X, max_clusters=10):
    scores = []
    for i in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, random_state=1).fit(X)
        scores.append(kmeans.inertia_)
    return scores.index(min(scores)) + 2

n_clusters = find_optimal_clusters(X_scaled)
X['Cluster'] = KMeans(n_clusters=n_clusters, random_state=1).fit_predict(X_scaled)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Model Training and Evaluation
models = {
    "Logistic Regression": LogisticRegression(random_state=1, max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=1),
    "Random Forest": RandomForestClassifier(random_state=1),
}

def evaluate_model(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{model.__class__.__name__} Accuracy: {accuracy:.4f}")

for name, model in models.items():
    print(f"Evaluating {name}")
    evaluate_model(model, X_train, X_test, y_train, y_test)
