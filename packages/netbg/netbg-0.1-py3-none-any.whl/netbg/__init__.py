def help():
    help_code = '''
    1. crud()
    2. logistic() 
    3. pipeline()
    4. shingles_word() or shingles_char()
    5. minhash()
    6. minhashpro() : For k-shingles with minhash
    7. martin()
    8. bloom()
    9. ams()
    10. bipartite()
    11. social()
    12. pcy()
    '''
    print("Available methods in netbg package:\nExample :\n\timport netbg as ng\n\tng.social()")
    print(f"\n{help_code}")

def crud():
    code = '''
from pyspark.sql import SparkSession
from pyspark.sql import Row

# Initialize Spark session
spark = SparkSession.builder.appName("CRUD Operations with TempView").getOrCreate()

# Manually creating a DataFrame using Row
data = [
    Row(ID=1, Name="Alice", Age=25),
    Row(ID=2, Name="Bob", Age=30),
    Row(ID=3, Name="Charlie", Age=35)
]

# Create DataFrame
df_manual = spark.createDataFrame(data)

# Create a temporary view for SQL queries
df_manual.createOrReplaceTempView("people")

# Select records where Age is greater than 25
filtered_records = spark.sql("SELECT * FROM people WHERE Age > 25")
filtered_records.show()

# Insert new records
new_data = [
    Row(ID=4, Name="David", Age=40),
    Row(ID=5, Name="Eva", Age=28)
]
df_new = spark.createDataFrame(new_data)
df_combined = df_manual.union(df_new)
df_combined.createOrReplaceTempView("people_combined")
spark.sql("SELECT * FROM people_combined").show()

# Update Age for the person with ID = 2
updated_query = """
SELECT ID, Name,
    CASE
        WHEN ID = 2 THEN 32
        ELSE Age
    END AS Age
FROM people_combined
"""
df_updated = spark.sql(updated_query)
df_updated.createOrReplaceTempView("people_updated")
spark.sql("SELECT * FROM people_updated").show()

# Delete records where ID = 1
df_deleted = spark.sql("SELECT * FROM people_updated WHERE ID != 1")
df_deleted.createOrReplaceTempView("people_updated")
spark.sql("SELECT * FROM people_updated").show()    
    '''
    print(code)

def logistic():
    code = '''
# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler, StandardScaler, Imputer
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col, when

# Download CSV
!wget https://raw.githubusercontent.com/neelamdoshi/Spark_neelam/main/diabetes.csv

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("DiabetesLogisticRegressionWithoutPipeline") \
    .getOrCreate()

# Load and inspect the data
data = spark.read.csv("diabetes.csv", header=True, inferSchema=True)
data.printSchema()
data.show(5)

# Step 1: Replace zero values with nulls in specific columns where zero is invalid
columns_with_zero_as_missing = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

# Replace zero values with null in specified columns
for column in columns_with_zero_as_missing:
    data = data.withColumn(column, when(col(column) == 0, None).otherwise(col(column)))

# Check data after replacing zeros
data.show(5)

# Step 2: Impute missing (null) values using the median strategy
# List of all feature columns excluding the label (Outcome)
feature_cols = [col for col in data.columns if col != 'Outcome']

# Create an Imputer instance to fill missing values with the median
imputer = Imputer(inputCols=feature_cols, outputCols=[f"{col}_imputed" for col in feature_cols])\
    .setStrategy("median")  # Set strategy to median

# Apply the Imputer
imputed_data = imputer.fit(data).transform(data)
imputed_data.show(5)  # Inspect imputed data

# Step 3: Assemble the features (manually without pipeline)
# Use imputed columns for feature assembling
imputed_feature_cols = [f"{col}_imputed" for col in feature_cols]

# Assemble the feature columns into a single vector
assembler = VectorAssembler(inputCols=imputed_feature_cols, outputCol="features")
assembled_data = assembler.transform(imputed_data)
assembled_data.select("features").show(5)

# Step 4: Standardize the feature vectors (scaling manually)
scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")
scaler_model = scaler.fit(assembled_data)
scaled_data = scaler_model.transform(assembled_data)
scaled_data.select("scaledFeatures").show(5)

# Step 5: Prepare label column
# Create the label column from Outcome (cast it to double type)
final_data = scaled_data.withColumn("label", col("Outcome").cast("double"))

# Step 6: Split data into training and test sets
train_data, test_data = final_data.randomSplit([0.8, 0.2], seed=42)

# Step 7: Train a Logistic Regression model
lr = LogisticRegression(featuresCol="scaledFeatures", labelCol="label")
lr_model = lr.fit(train_data)

# Step 8: Make predictions on the test data
predictions = lr_model.transform(test_data)
predictions.select("label", "prediction", "probability").show(5)

# Step 9: Evaluate the model using BinaryClassificationEvaluator
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label")
accuracy = evaluator.evaluate(predictions)
print("Accuracy:", {accuracy}")

# Stop Spark session
spark.stop()    
    '''
    print(code)

def pipeline():
    code = '''
!pip install pyspark
# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler, StandardScaler, Imputer
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col, when

# Download CSV
!wget https://raw.githubusercontent.com/neelamdoshi/Spark_neelam/main/diabetes.csv

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("DiabetesLogisticRegressionWithImputer") \
    .getOrCreate()

# Load and inspect the data
data = spark.read.csv("diabetes.csv", header=True, inferSchema=True)
data.printSchema()
data.show(5)

# Step 1: Replace zero values with nulls in specific columns where zero is invalid
columns_with_zero_as_missing = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

# Replace zero values with null in specified columns
for column in columns_with_zero_as_missing:
    data = data.withColumn(column, when(col(column) == 0, None).otherwise(col(column)))

# Step 2: Impute missing (null) values using the median strategy
feature_cols = [col for col in data.columns if col != 'Outcome']
imputer = Imputer(inputCols=feature_cols, outputCols=[f"{col}_imputed" for col in feature_cols])\
    .setStrategy("median")  # Set strategy to median

# Apply the Imputer
imputed_data = imputer.fit(data).transform(data)
imputed_data.show(5)  # Inspect imputed data

# Step 3: Feature assembly and scaling
# Use imputed columns for feature assembling
imputed_feature_cols = [f"{col}_imputed" for col in feature_cols]

# Assemble the feature columns into a single vector
assembler = VectorAssembler(inputCols=imputed_feature_cols, outputCol="features")

# Standardize the feature vectors (scaling)
scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")

# Create the label column from Outcome (cast it to double type)
imputed_data = imputed_data.withColumn("label", col("Outcome").cast("double"))

# Step 4: Create a Logistic Regression model
lr = LogisticRegression(featuresCol="scaledFeatures", labelCol="label")

# Step 5: Create a Pipeline with stages: Imputer -> Assembler -> Scaler -> Logistic Regression
pipeline = Pipeline(stages=[imputer, assembler, scaler, lr])

# Step 6: Train-test split
train_data, test_data = imputed_data.randomSplit([0.8, 0.2], seed=42)

# Step 7: Train the model
model = pipeline.fit(train_data)

# Step 8: Make predictions on the test data
predictions = model.transform(test_data)
predictions.select("label", "prediction", "probability").show(5)

# Step 9: Evaluate the model using BinaryClassificationEvaluator
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label")
accuracy = evaluator.evaluate(predictions)
print(f"Accuracy: {accuracy}")

# Stop Spark session
spark.stop()    
    '''
    print(code)


def shingles_word():
    code = '''
import string

def generate_k_shingles_word(filename, k):
  shingles = set()
  with open(filename, 'r') as file:
    text = file.read()
    # Remove punctuation and brackets
    text = text.translate(str.maketrans('', '', string.punctuation + '[]'))
    words = text.split()
    # Initialize an empty list to store results
    output = []
    # Loop to generate substrings of length k
    for i in range(len(words) - k + 1):
        substring = ' '.join(words[i:i + k])
        output.append(substring)
  return output

k = 2  #value of k for k-shingles
shingles1 = generate_k_shingles_word("path", k)
print(f"Shingles for file1.txt:  \n {shingles1}\n\n")

## Character as Token
import string

def generate_k_shingles_char(filename, k):
    shingles = set()
    with open(filename, 'r') as file:
        text = file.read()
        # Remove punctuation and brackets
        text = text.translate(str.maketrans('', '', string.punctuation + '[]'))
        # Remove whitespace
        text = text.replace(" ", "").replace("\n", "")
        # Initialize an empty list to store results
        output = []
        # Loop to generate substrings of length k
        for i in range(len(text) - k + 1):
            substring = text[i:i + k]
            output.append(substring)
    return output

k = 3  # value of k for k-shingles
shingles1 = generate_k_shingles_char('path', k)
print(f"Shingles for file1.txt: \n {shingles1}\n\n")   
    '''
    print(code)


def shingles_char():
    code = '''
## Character as Token
import string

def generate_k_shingles_char(filename, k):
    shingles = set()
    text = filename
    # Remove punctuation and brackets
    text = text.translate(str.maketrans('', '', string.punctuation + '[]'))
    text = text.replace(" ", "").replace("\n", "")
    output = []
    for i in range(len(text) - k + 1):
        substring = text[i:i + k]
        output.append(substring)
    return output

k = 5  # value of k for k-shingles
shingles1 = generate_k_shingles_char('this is the random text for shingles', k)
print(f"Shingles for file1.txt:  \n {shingles1}\n\n")    
    '''
    print(code)


def minhash():
    code = '''
import numpy as np

data = np.array([
    [1, 0, 0, 1],  
    [0, 0, 1, 0],  
    [0, 1, 0, 1],  
    [1, 1, 0, 0],  
    [0, 1, 1, 0]   
])

def h1(x):
    return (x + 1) % 5

def h2(x):
    return (3 * x + 1) % 5

num_hashes = 2
num_elements = data.shape[0]

signature_matrix = np.full((num_hashes, data.shape[1]), np.inf)

for row in range(num_elements):
    hashes = [h1(row), h2(row)]
    for col in range(data.shape[1]):
        if data[row, col] == 1:  # If the element is present in the set
            for i in range(num_hashes):
                signature_matrix[i, col] = min(signature_matrix[i, col], hashes[i])

# Display the resulting signature matrix
print("Signature Matrix:")
print(signature_matrix)    
    '''
    print(code)


def minhashpro():
    code = '''
import hashlib
import random
import numpy as np

# Step 1: Extract k-shingles from text
def get_shingles(text, k):
    shingles = set()
    for i in range(len(text) - k + 1):
        shingles.add(text[i:i + k])
    return shingles

# Step 2: Hashing a shingle (for MinHash)
def hash_shingle(shingle, seed):
    return int(hashlib.md5((shingle + str(seed)).encode('utf8')).hexdigest(), 16)

# Step 3: Apply MinHash
def minhash(shingles, num_hashes=100):
    minhashes = []
    for seed in range(num_hashes):
        min_hash = min([hash_shingle(shingle, seed) for shingle in shingles])
        minhashes.append(min_hash)
    return minhashes

# Step 4: Calculate Jaccard similarity using MinHash signatures
def calculate_jaccard_similarity(minhash1, minhash2):
    matches = sum(1 for i in range(len(minhash1)) if minhash1[i] == minhash2[i])
    return matches / len(minhash1)

def load_text_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Main function to calculate similarity between 3 documents
def compare_documents(file1, file2, file3, k=5, num_hashes=100):
    doc1_text = load_text_from_file(file1)
    doc2_text = load_text_from_file(file2)
    doc3_text = load_text_from_file(file3)
    
    # Generate shingles
    doc1_shingles = get_shingles(doc1_text, k)
    doc2_shingles = get_shingles(doc2_text, k)
    doc3_shingles = get_shingles(doc3_text, k)
    
    # Apply MinHash
    doc1_minhash = minhash(doc1_shingles, num_hashes)
    doc2_minhash = minhash(doc2_shingles, num_hashes)
    doc3_minhash = minhash(doc3_shingles, num_hashes)
    
    # Compute Jaccard similarity
    similarity12 = calculate_jaccard_similarity(doc1_minhash, doc2_minhash)
    similarity13 = calculate_jaccard_similarity(doc1_minhash, doc3_minhash)
    similarity23 = calculate_jaccard_similarity(doc2_minhash, doc3_minhash)
    
    return similarity12, similarity13, similarity23

# Example usage:
file1 = "doc1.txt"
file2 = "doc2.txt"
file3 = "doc3.txt"

similarity12, similarity13, similarity23 = compare_documents(file1, file2, file3)

print(f"Similarity between doc1 and doc2: {similarity12}")
print(f"Similarity between doc1 and doc3: {similarity13}")
print(f"Similarity between doc2 and doc3: {similarity23}")    
    '''
    print(code)


def martin():
    code = '''
import math

def manual_hash(x):
    return (x * 31 + x) % (2 ** 32)

def hash_to_binary(x):
    return bin(manual_hash(x))[2:]

def count_trailing_zeros(binary_string):
    return len(binary_string) - len(binary_string.rstrip('0'))

# Flajolet-Martin algorithm 
def flajolet_martin(stream):
    max_trailing_zeros = 0

    for item in stream:
        
        binary_hash = hash_to_binary(item)
        
        trailing_zeros = count_trailing_zeros(binary_hash)
        
        max_trailing_zeros = max(max_trailing_zeros, trailing_zeros)

    #2 raised to the power
    estimate = 2 ** max_trailing_zeros
    return estimate, max_trailing_zeros

stream = [7, 10, 14, 15, 7, 10, 20, 25, 14]
distinct_estimate , max_zero = flajolet_martin(stream)
print(f"Estimated number of distinct items: {distinct_estimate}")
print(f"Max Traling Zero is {max_zero}")


*******************************
     Label Encoder with CSV
*******************************
import math
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def manual_hash(x):
    return (x * 31 + x) % (2 ** 32)

def hash_to_binary(x):
    return bin(manual_hash(x))[2:]

def count_trailing_zeros(binary_string):
    return len(binary_string) - len(binary_string.rstrip('0'))

def flajolet_martin(stream):
    max_trailing_zeros = 0

    for item in stream:
        binary_hash = hash_to_binary(item)
        trailing_zeros = count_trailing_zeros(binary_hash)
        max_trailing_zeros = max(max_trailing_zeros, trailing_zeros)

    #2 raised to the power 
    estimate = 2 ** max_trailing_zeros
    return estimate, max_trailing_zeros

# Example usage with a stream of numbers
le  = LabelEncoder()
df = pd.read_csv("data")
name = df["name"]
name = le.fit_transform(name)
print(name)
stream = [7, 10, 14, 15, 7, 10, 20, 25, 14]
distinct_estimate , max_zero = flajolet_martin(name)
print(f"Estimated number of distinct items: {distinct_estimate}")
print(f"Max Traling Zero is {max_zero}")
    '''
    print(code)


def bloom():
    code = '''
 size = 13  
bit_array = [0] * size

def hash1(item):
    return (item + 1) % size

def hash2(item):
    return (2*item+5) % size

def check_item(item):
    if bit_array[hash1(item)] == 0 or bit_array[hash2(item)] == 0:
        return False
    return True

present_set = [8,17,25,14,20]
for item in present_set:
    bit_array[hash1(item)] = 1
    bit_array[hash2(item)] = 1

print(f"Is 14 possibly in the Bloom filter? {check_item(7)}")
print(f"Is 15 possibly in the Bloom filter? {check_item(5)}") 
print(f"Bloom filter bit array: {bit_array}")


****************************************************
                 Bloom with CSV
****************************************************
import pandas as pd

size = 13 
bit_array = [0] * size

def hash1(item):
    return (item + 1) % size

def hash2(item):
    return (2*item+5) % size

def check_item(item):
    if bit_array[hash1(item)] == 0 or bit_array[hash2(item)] == 0:
        return False
    return True

present_set = pd.read_csv("path")
data = present_set["custid"]
for item in data:
    bit_array[hash1(item)] = 1
    bit_array[hash2(item)] = 1

# Checking for 14 and 15
print(f"Is 14 possibly in the Bloom filter? {check_item(7)}")
print(f"Is 15 possibly in the Bloom filter? {check_item(5)}") 
# Display the bit array to understand how the filter looks
print(f"Bloom filter bit array: {bit_array}")    

    '''
    print(code)


def ams():
    code = '''
import random

# Stream of numbers
stream = [1, 2, 7, 1, 4, 9, 4, 6, 1, 6, 4, 4, 5, 5, 5, 9, 8, 7, 2, 2, 4, 4, 1]

def AMS_algorithm(stream, X_indices):
    n = len(stream)
    estimates = []
    
    for X in X_indices:
        X_value = stream[X]  # Get the value from the stream at index X
        count_X_value = stream.count(X_value)  # Count occurrences of that value in the stream
        # The AMS estimate is n * (2 * count_X_value - 1)
        estimate = n * (2 * count_X_value - 1)
        estimates.append(estimate)
    return sum(estimates) / len(estimates)

# Indices X1, X2, X3
X1, X2, X3 = 3, 8, 13

# Calculate F2 using AMS algorithm
surprise_number = AMS_algorithm(stream, [X1, X2, X3])
print("Estimated Surprise Number (F2) using AMS Algorithm:", surprise_number)    
    '''
    print(code)



def bipartite():
    code = '''
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

# Create a bipartite graph
def create_bipartite_graph():
    B = nx.Graph()
    # Add nodes with the attribute "bipartite"
    top_nodes = {1, 2, 3}
    bottom_nodes = {'a', 'b', 'c'}
    B.add_nodes_from(top_nodes, bipartite=0)
    B.add_nodes_from(bottom_nodes, bipartite=1)

    # Add edges between nodes in the two sets
    edges = [(1, 'a'), (1, 'b'), (2, 'b'), (3, 'c')]
    B.add_edges_from(edges)

    return B, top_nodes, bottom_nodes

# Greedy algorithm for maximum matching
def greedy_maximum_matching(B, top_nodes, bottom_nodes):
    matching = set()  # To store the matching pairs
    matched_nodes = set()  # To keep track of matched nodes

    # Iterate over edges greedily
    for u, v in B.edges():
        if u not in matched_nodes and v not in matched_nodes:
            matching.add((u, v))
            matched_nodes.add(u)
            matched_nodes.add(v)

    return matching

# Step 1: Create a bipartite graph
B, top_nodes, bottom_nodes = create_bipartite_graph()

# Step 2: Check if the graph is bipartite
is_bipartite = bipartite.is_bipartite(B)
print(f"Is the graph bipartite? {is_bipartite}")

# Step 3: Perform greedy maximum matching if bipartite
if is_bipartite:
    # Apply the greedy maximum matching algorithm
    matching = greedy_maximum_matching(B, top_nodes, bottom_nodes)
    print(f"Greedy Maximum Matching: {matching}")

    # Step 4: Plot the graph with matching edges highlighted
    pos = nx.bipartite_layout(B, top_nodes)

    # Highlight matching edges in red
    matching_edges = list(matching)
    edge_colors = ['red' if (u, v) in matching_edges or (v, u) in matching_edges else 'black' for u, v in B.edges()]

    # Draw the graph with the highlighted matching
    nx.draw(B, pos, with_labels=True, edge_color=edge_colors, node_color=['lightblue' if n in top_nodes else 'lightgreen' for n in B.nodes()], node_size=2000, font_size=15)
    plt.title("Bipartite Graph with Greedy Maximum Matching")
    plt.show()
else:
    print("The graph is not bipartite.")   
    '''
    print(code)




def social():
    code = '''
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from IPython.display import display
from networkx.algorithms import community

# Load the nodes and edges from CSV files
nodes_df = pd.read_csv('./Documents/node.csv')
edges_df = pd.read_csv('./Documents/edge.csv')

#df = pd.read_csv('./Documents/data.csv')
#node_df = df[['id','name','age']]
#edge_df = df[['source','target']]

# Create a directed graph
G = nx.DiGraph()

# Add nodes to the graph
for index, row in nodes_df.iterrows():
    G.add_node(row['id'], name=row['name'], age=row['age'])

# Add edges to the graph
for index, row in edges_df.iterrows():
    G.add_edge(row['source'], row['target'], rel=row['relationsip'])

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1800, font_size=10, font_color='black', font_weight='bold')

# Draw edge labels (weights)
edge_labels = nx.get_edge_attributes(G, 'rel')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title('Social Network Graph')
plt.show()


degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
pagerank = nx.pagerank(G)

print(degree_centrality)
print(betweenness_centrality)
print(closeness_centrality)
print(pagerank)

# Find clusters using Girvan-Newman algorithm
comp = community.girvan_newman(G)
# Get the first set of communities
first_community = next(comp)

# Print communities
for i, community in enumerate(first_community):
    print(f"\n\nCommunity {i + 1}: {list(community)}")    
    '''
    print(code)



def pcy():
    code = '''
# Example list of transactions
transactions = [
    [1, 2, 3],
    [1, 3, 5],
    [3, 5, 6],
    [2, 3, 4],
    [2, 4, 6],
    [1, 2, 4],
    [3, 4, 5],
    [1, 3, 4],
    [2, 3, 5],
    [4, 5, 6],
    [2, 4, 5],
    [3, 4, 6]
]

# Step 1: Get unique items
unique = []
for transaction in transactions:
    for item in transaction:
        if item not in unique:
            unique.append(item)

print("Unique items:", unique)

# Step 2: Count occurrences of each unique item
count = []
for item in unique:
    item_count = sum(transaction.count(item) for transaction in transactions)
    count.append(item_count)

print("Counts of each unique item:", count)

# Step 3: Create pairs of each unique item
pairs = []
for i in range(len(unique)):
    for j in range(i + 1, len(unique)):
        pairs.append((unique[i], unique[j]))

print("Pairs of unique items:", pairs)

# Step 4: Check if pair is available in transaction and count its occurrences
pair_counts = {}
for pair in pairs:
    count = 0
    for transaction in transactions:
        if pair[0] in transaction and pair[1] in transaction:
            count += 1
    pair_counts[pair] = count

print("Counts of each pair in transactions:", pair_counts)



# Step 5: Apply threshold and hash function
threshold = 4
bucket_size = int(input("Enetr Bucket Size value: "))

# Hash function
def hash_function(i, j):
    return (i * j) % bucket_size

# Filter pairs based on threshold and calculate hash values using item values, not their indices
hash_table = []
for pair, count in pair_counts.items():
    if count >= threshold:
        # Corrected: Use the actual item values for hashing
        hash_value = hash_function(pair[0], pair[1])
        hash_table.append((pair, count, hash_value))

print("Filtered pairs, counts, and hash values:")
for entry in hash_table:
    print(f"Pair: {entry[0]}, Count: {entry[1]}, Hash Value: {entry[2]}")

# Step 6: Create a table of pairs, their counts, and their hash values
print("\nTable of pairs, counts, and hash values:")
print("Pair\t\tCount\tHash Value")
for entry in hash_table:
    print(f"{entry[0]}\t{entry[1]}\t{entry[2]}")
    '''
    print(code)