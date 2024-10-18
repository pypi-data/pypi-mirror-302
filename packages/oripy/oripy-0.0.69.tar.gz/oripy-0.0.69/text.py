# CodeLibrary.py

class CodeLibraryText:

    fptree = """ 
class FPNode:
    \"\"\" Represents a node in the FP-tree. \"\"\"
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None

class FPTree:
    \"\"\" Constructs and mines the FP-tree. \"\"\"
    def __init__(self, transactions, min_support):
        self.min_support = min_support
        self.header_table = {}
        self.root = FPNode(None, 0, None)
        self.transactions = transactions
        self.frequent_items = self._get_frequent_items()
        self._build_tree()

    def _get_frequent_items(self):
        \"\"\" Retrieve frequent items based on min_support from transactions. \"\"\"
        item_count = {}
        for transaction in self.transactions:
            for item in transaction:
                item_count[item] = item_count.get(item, 0) + 1
        return {k: v for k, v in item_count.items() if v >= self.min_support}

    def _build_tree(self):
        \"\"\" Build the FP-tree from the transactions. \"\"\"
        for i, transaction in enumerate(self.transactions, 1):
            sorted_items = sorted(
                [item for item in transaction if item in self.frequent_items],
                key=lambda x: (-self.frequent_items[x], x)
            )
            if sorted_items:
                self._insert_tree(sorted_items, self.root)
            print(f"\nFP-Tree after inserting T{i}:")
            self._print_tree(self.root)

    def _insert_tree(self, items, node):
        \"\"\" Insert a transaction into the FP-tree. \"\"\"
        if items:
            item = items[0]
            if item in node.children:
                node.children[item].count += 1
            else:
                new_node = FPNode(item, 1, node)
                node.children[item] = new_node
                if item not in self.header_table:
                    self.header_table[item] = new_node
                else:
                    current = self.header_table[item]
                    while current.next:
                        current = current.next
                    current.next = new_node
            self._insert_tree(items[1:], node.children[item])

    def _print_tree(self, node, indent=""):
        \"\"\" Print the FP-tree structure. \"\"\"
        if node.item:
            print(f"{indent}{node.item}:{node.count}")
        for child in sorted(node.children.values(), key=lambda x: x.item):
            self._print_tree(child, indent + " ")

def get_conditional_pattern_base(node):
    \"\"\" Retrieve the conditional pattern base for a given node. \"\"\"
    patterns = []
    while node:
        path = []
        support = node.count
        current = node.parent
        while current.parent:
            path.append(current.item)
            current = current.parent
        if path:
            patterns.append((list(reversed(path)), support))
        node = node.next
    return patterns

# Example usage
transactions = [
    ['E', 'K', 'M', 'N', 'O', 'Y'],
    ['D', 'E', 'K', 'N', 'O', 'Y'],
    ['A', 'E', 'K', 'M'],
    ['C', 'K', 'M', 'U', 'Y'],
    ['C', 'E', 'I', 'K', 'O']
]
min_support = 3

# Create FP-Tree
fp_tree = FPTree(transactions, min_support)
print("\nFinal FP-Tree Structure:")
fp_tree._print_tree(fp_tree.root)

print("\nConditional Pattern Bases:")
for item in sorted(fp_tree.header_table.keys()):
    patterns = get_conditional_pattern_base(fp_tree.header_table[item])
    print(f"{item}: {patterns}")
    """

    apriori = """ 
from itertools import combinations

# Helper function to calculate support for an itemset
def calculate_support(itemset, transactions):
    count = sum(1 for transaction in transactions if itemset.issubset(transaction))
    return count / len(transactions)

# Generate all candidate itemsets of a specific length
def generate_candidates(frequent_itemsets, length):
    candidates = set()
    for itemset1 in frequent_itemsets:
        for itemset2 in frequent_itemsets:
            union_itemset = itemset1 | itemset2  # Union of two itemsets
            if len(union_itemset) == length:  # Only keep itemsets of the desired length
                candidates.add(frozenset(union_itemset))
    return candidates

# Apriori algorithm implementation
def apriori(transactions, min_support=0.5):
    # Step 1: Convert transactions to list of sets
    transactions = [set(transaction) for transaction in transactions]

    # Step 2: Generate frequent 1-itemsets
    itemsets = set()
    for transaction in transactions:
        for item in transaction:
            itemsets.add(frozenset([item]))

    # Step 3: Prune infrequent itemsets
    frequent_itemsets = []
    for itemset in itemsets:
        support = calculate_support(itemset, transactions)
        if support >= min_support:
            frequent_itemsets.append((itemset, support))

    # Print frequent 1-itemsets
    print("Frequent 1-itemsets:")
    for itemset, support in frequent_itemsets:
        print(f"{set(itemset)}: {support:.2f}")

    # Step 4: Generate higher-order itemsets (2-itemsets, 3-itemsets, etc.)
    k = 2
    while frequent_itemsets:
        candidates = generate_candidates([itemset for itemset, _ in frequent_itemsets], k)
        frequent_itemsets = []
        for candidate in candidates:
            support = calculate_support(candidate, transactions)
            if support >= min_support:
                frequent_itemsets.append((candidate, support))

        # Print frequent k-itemsets
        if frequent_itemsets:
            print(f"\nFrequent {k}-itemsets:")
            for itemset, support in frequent_itemsets:
                print(f"{set(itemset)}: {support:.2f}")

        k += 1

# Sample transaction dataset
transactions = [
    ['A', 'B', 'C'],
    ['A', 'B'],
    ['A', 'C'],
    ['B', 'C'],
    ['A', 'B', 'C'],
]

# Run the Apriori algorithm with minimum support 0.5
apriori(transactions, min_support=0.5)
    """
    
    pagerank= """ 

import numpy as np


def pagerank(graph, max_iterations, damping_factor=0.8):
    num_pages = len(graph)
    pr = {page: 1 / num_pages for page in graph}
   
    for _ in range(max_iterations):
        new_pr = {}
        for page in graph:
            incoming_pr = sum(pr[i] / len(graph[i]) for i in graph if page in graph[i])
            new_pr[page] = (1 - damping_factor) + damping_factor * incoming_pr
            pr[page] = new_pr[page]  # Update PR immediately
   
    return pr


def get_graph_input():
    graph = {}
    while True:
        page = input("Enter a page name (or press Enter to finish): ").strip()
        if not page:
            break
        links = input(f"Enter outgoing links for {page} (comma-separated): ").split(',')
        graph[page] = [link.strip() for link in links if link.strip()]
    return graph


def main():
    print("Enter the graph structure:")
    graph = get_graph_input()
   
    max_iterations = int(input("Enter the maximum number of iterations: "))
   
    result = pagerank(graph, max_iterations)
   
    print("\nFinal PageRank values:")
    for page, rank in result.items():
        print(f"{page}: {rank:.4f}")


if __name__ == "__main__":
    main()


    """

    kmeans = """ 
import numpy as np


def kmeans(X, k, initial_centroids, max_iters=100):
    centroids = initial_centroids.copy()
   
    for _ in range(max_iters):
        # Assign each point to the nearest centroid
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(distances, axis=0)
       
        # Update centroids
        new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
       
        # Check for convergence
        if np.all(centroids == new_centroids):
            break
       
        centroids = new_centroids
   
    return labels, centroids


def get_user_input():
    # Get number of data points
    n = int(input("Enter the number of data points: "))
   
    # Get data points
    X = []
    print("Enter the coordinates for each data point:")
    for i in range(n):
        point = list(map(float, input(f"Point {i+1} (space-separated): ").split()))
        X.append(point)
    X = np.array(X)
   
    # Get number of clusters
    k = int(input("Enter the number of clusters: "))
   
    # Get initial centroids
    centroids = []
    print("Enter the coordinates for each initial centroid:")
    for i in range(k):
        centroid = list(map(float, input(f"Centroid {i+1} (space-separated): ").split()))
        centroids.append(centroid)
    initial_centroids = np.array(centroids)
   
    return X, k, initial_centroids


if __name__ == "__main__":
    # Get user input
    X, k, initial_centroids = get_user_input()
   
    # Run K-means
    labels, centroids = kmeans(X, k, initial_centroids)
   
    print("\nResults:")
    # Group data points by cluster
    clusters = {i: [] for i in range(k)}
    for i, label in enumerate(labels):
        clusters[label].append(X[i])
   
    for i in range(k):
        print(f"Cluster {i+1}: {clusters[i]}")
   
    print("Final centroids:")
    for i, centroid in enumerate(centroids):
        print(f"Centroid {i+1}: {centroid}")
    """
    
    id3 = """
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

# Sample dataset
data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Rain', 'Overcast', 'Sunny', 'Sunny', 'Rain'],
    'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Mild', 'Mild', 'Hot', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal'],
    'Windy': [False, True, False, False, False, True, True, False, True, True],
    'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Convert categorical variables to numerical
df['Outlook'] = df['Outlook'].map({'Sunny': 0, 'Overcast': 1, 'Rain': 2})
df['Temperature'] = df['Temperature'].map({'Hot': 0, 'Mild': 1, 'Cool': 2})
df['Humidity'] = df['Humidity'].map({'High': 0, 'Normal': 1})
df['Windy'] = df['Windy'].map({False: 0, True: 1})
df['Play'] = df['Play'].map({'No': 0, 'Yes': 1})

# Features and target variable
X = df.drop('Play', axis=1)
y = df['Play']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the ID3 decision tree classifier
clf = DecisionTreeClassifier(criterion='entropy', random_state=42)
clf.fit(X_train, y_train)

# Print the tree structure
tree_rules = export_text(clf, feature_names=list(X.columns))
print("Decision Tree Rules:\n", tree_rules)

# Make predictions
predictions = clf.predict(X_test)

# Display predictions
print("\nPredictions:", predictions)
    """
    
    naivebayes = """
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Sample weather data
data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Rain', 'Overcast', 'Sunny', 'Sunny', 'Rain'],
    'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Mild', 'Mild', 'Hot', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'High', 'Normal'],
    'Windy': [False, True, False, False, True, True, False, False, True, True],
    'Play': ['No', 'No', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Encode categorical features
df_encoded = pd.get_dummies(df.drop('Play', axis=1), drop_first=True)
X = df_encoded.values
y = df['Play'].map({'No': 0, 'Yes': 1}).values  # Convert labels to binary

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create and fit the model
model = GaussianNB()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)
print("Predictions:", predictions)
print("Accuracy:", accuracy)
"""

    def __init__(self):
        pass  

