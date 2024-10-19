def bda():
    num = int(input())
    if(num==1):
        print(
            '''
######################## pySpark Create DataFrame #############################
 
# data frame
from pyspark.sql import SparkSession
 
# Create a Spark session
spark = SparkSession.builder \
    .appName("Spark SQL Basics") \
    .getOrCreate()
 
#Manual Create of Dataframe
data = [("Alice", 30), ("Bob", 25), ("Cathy", 29)]
columns = ["Name", "Age"]
 
# Create DataFrame
df = spark.createDataFrame(data, schema=columns)
# print(df)
# Show the DataFrame
# df.show()
 
# Register the DataFrame as a temporary view
df.createOrReplaceTempView("people")
 
#Create dataframe form csv file
# Read a CSV file into a DataFrame
df_csv = spark.read.csv("employees.csv", header=True, inferSchema=True)
 
# Show the DataFrame
df_csv.show()
 
# Write the DataFrame to a Parquet file
# df.write.mode("overwrite").parquet("path/to/output/file.parquet")
 
# Read the Parquet file into a DataFrame
# df_parquet = spark.read.parquet("path/to/output/file.parquet")
 
# Show the DataFrame
# df_parquet.show()

'''
        )
    elif(num==2):
        print(
            '''
############################ Join ###################################
# join
# Create two DataFrames
data1 = [("Alice", 30), ("Bob", 25), ("Cathy", 29)]
columns1 = ["Name", "Age"]
df1 = spark.createDataFrame(data1, schema=columns1)
 
data2 = [("Alice", "F"), ("Bob", "M"), ("David", "M")]
columns2 = ["Name", "Gender"]
df2 = spark.createDataFrame(data2, schema=columns2)
 
# Inner join
joined_df = df1.join(df2, on="Name", how="inner")
joined_df.show()
 
# Left join
left_joined_df = df1.join(df2, on="Name", how="left")
left_joined_df.show()
 
# Right join
right_joined_df = df1.join(df2, on="Name", how="right")
right_joined_df.show()
 
# Full outer join
full_joined_df = df1.join(df2, on="Name", how="full")
full_joined_df.show()
'''
        )
    elif(num==3):
        print(
            '''
######################## Grouping ########################################
# Grouping
# Create a DataFrame for aggregation
data3 = [("Alice", 30), ("Bob", 25), ("Alice", 35), ("Bob", 20)]
columns3 = ["Name", "Age"]
df3 = spark.createDataFrame(data3, schema=columns3)
 
# Group by Name and calculate average age
grouped_df = df3.groupBy("Name").agg({"Age": "avg"}).alias("Average Age")
grouped_df.show()
grouped_df.printSchema()
 
# Using multiple aggregations
aggregated_df = df3.groupBy("Name").agg(
    {"Age": "avg", "Age": "count"}
)
aggregated_df.show()
'''
        )
    elif(num==4):
        print(
            '''
################################ Aggragation ##############################
 
# aggragation
from pyspark.sql import functions as F
 
# Create a sample DataFrame
data = [("Alice", 30), ("Bob", 25), ("Cathy", 29), ("David", 35)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, schema=columns)
 
# Perform aggregate functions
aggregates = df.agg(
    F.max("Age").alias("Max_Age"),
    F.min("Age").alias("Min_Age"),
    F.avg("Age").alias("Avg_Age"),
    F.sum("Age").alias("Total_Age")
)
 
aggregates.show()
'''
        )
    elif(num==5):
        print(
            '''
######################### Various Function ##################################
# various function
# Run a SQL query
result = spark.sql("SELECT Name, Age FROM people WHERE Age > 26")
result.show()
 
# Filter DataFrame for ages greater than 30
filtered_df = df3.filter(df3.Age > 30)
filtered_df.show()
 
# Order by Age in descending order
ordered_df = df3.orderBy(df3.Age.desc())
ordered_df.show()
 
# Step 6: Complex Queries
# Count total number of people
count_df = spark.sql("SELECT COUNT(*) AS Total_People FROM people_table")
print("Total People:")
count_df.show()
 
# Step 7: Window Function Example
from pyspark.sql.window import Window
 
# Adding a rank column
window_spec = Window.orderBy("Age")
ranked_df = people_df.withColumn("Rank", F.rank().over(window_spec))
ranked_df.show()
 
# Step 8: User-Defined Function (UDF)
def increment_age(age):
    return age + 1
 
increment_age_udf = F.udf(increment_age, IntegerType())
df_with_incremented_age = final_df.withColumn("Age", increment_age_udf(final_df.Age))
print("Table with Incremented Ages:")
df_with_incremented_age.show()
 
# Step 9: Read from CSV (example path, replace with your actual path)
# df_from_csv = spark.read.csv("path/to/file.csv", header=True, inferSchema=True)
 
# Step 10: Write to Parquet
final_df.write.parquet("people_table_parquet.parquet")
 
# Step 11: Data Sampling
sampled_df = final_df.sample(fraction=0.5)
print("Sampled Data:")
sampled_df.show()
 
# Step 12: Data Cleaning (example: filling missing values)
cleaned_df = final_df.fillna({'Age': 0})  # Fill missing Age values with 0
print("Cleaned DataFrame:")
cleaned_df.show()
 
# Stop the Spark session
spark.stop()
'''
        )
    elif(num==6):
        print(
            '''
############################## Operation on Table
# operation on table 
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
 
# Create Spark session
spark = SparkSession.builder \
    .appName("Combined Table Operations") \
    .getOrCreate()
 
# Step 1: Create a Table
# Sample data for the initial table
data = [("Alice", 30), ("Bob", 25), ("Cathy", 29)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, schema=columns)
 
# Create a permanent table
df.write.saveAsTable("people_table")
 
# Step 2: Add Values to the Table
# New data to add
new_data = [("David", 35), ("Eva", 28)]
new_df = spark.createDataFrame(new_data, schema=columns)
 
# Append new data to the existing table
new_df.write.insertInto("people_table")
 
# Step 3: Update Table Values
# Read the existing table into a DataFrame
people_df = spark.table("people_table")
 
# Update the age for "Alice"
updated_df = people_df.withColumn("Age",
                                    F.when(people_df.Name == "Alice", 32).otherwise(people_df.Age))
 
# Overwrite the existing table with the updated DataFrame
updated_df.write.mode("overwrite").saveAsTable("people_table")
 
# Step 4: Delete Values from the Table
# Read the existing table into a DataFrame
people_df = spark.table("people_table")
 
# Delete entries for "Bob"
filtered_df = people_df.filter(people_df.Name != "Bob")
 
# Overwrite the existing table with the filtered DataFrame
filtered_df.write.mode("overwrite").saveAsTable("people_table")
 
# Step 5: Show the Final Table
final_df = spark.table("people_table")
final_df.show()
 
# Stop the Spark session
spark.stop()
'''
        )
    elif(num==7):
        print(
            '''
############################ RDD Operation ##################################
# RDD 
from pyspark import SparkConf, SparkContext
 
# Initialize Spark
conf = SparkConf().setAppName("RDD Operations").setMaster("local[*]")  # Use all available cores
sc = SparkContext(conf=conf)
 
# Step 1: Create an RDD
data = [("Alice", 30), ("Bob", 25), ("Cathy", 29), ("David", 35)]
rdd = sc.parallelize(data)  # Create an RDD from a list
 
# Step 2: Show RDD contents
print("Original RDD:")
print(rdd.collect())  # Collect and print all elements in the RDD
 
# Step 3: Map Operation
# Increment age by 1
incremented_rdd = rdd.map(lambda x: (x[0], x[1] + 1))
print("After Incrementing Ages:")
print(incremented_rdd.collect())
 
# Step 4: Filter Operation
# Filter out people older than 30
filtered_rdd = rdd.filter(lambda x: x[1] > 30)
print("People Older than 30:")
print(filtered_rdd.collect())
 
# Step 5: Reduce Operation
# Calculate total age
total_age = rdd.map(lambda x: x[1]).reduce(lambda x, y: x + y)
print(f"Total Age: {total_age}")
 
# Step 6: Count Operation
# Count the number of entries in the RDD
count = rdd.count()
print(f"Count of People: {count}")
 
# Step 7: GroupByKey Operation
# Group by age
grouped_rdd = rdd.groupByKey()
print("Grouped by Age:")
for key, values in grouped_rdd.collect():
    print(f"Age: {key}, Names: {list(values)}")
 
# Step 8: Join Operation
# Create another RDD
data2 = [("Alice", "F"), ("Bob", "M"), ("Cathy", "F"), ("David", "M")]
rdd2 = sc.parallelize(data2)
 
# Perform join
joined_rdd = rdd.join(rdd2)
print("Joined RDD:")
print(joined_rdd.collect())
 
# Step 9: Save RDD to Text File
output_path = "output/people.txt"  # Specify your output path
rdd.saveAsTextFile(output_path)
 
# Step 10: Stop the SparkContext
sc.stop()
'''
        )
    elif(num==8):
        print(
            '''
############################# pySpark Pipeline #######################
# pyspark pipeline
 
from pyspark.sql import SparkSession
from pyspark.sql import types as tp
from pyspark.ml import Pipeline
from pyspark.ml.feature import Imputer, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.sql.functions import when, col
 
# Create Spark session
spark = SparkSession.builder.appName("DiabetesPipeline").getOrCreate()
 
# Read CSV file with schema
my_data = spark.read.csv('/content/drive/MyDrive/diabetes.csv', header=True, schema=my_schema)
 
# Show data and schema
my_data.printSchema()
my_data.show()
 
# Define schema
my_schema = tp.StructType([
    tp.StructField('Pregnancies', tp.IntegerType(), True),
    tp.StructField('Glucose', tp.IntegerType(), True),
    tp.StructField('BloodPressure', tp.IntegerType(), True),
    tp.StructField('SkinThickness', tp.IntegerType(), True),
    tp.StructField('Insulin', tp.IntegerType(), True),
    tp.StructField('BMI', tp.FloatType(), True),
    tp.StructField('DiabetesPedigreeFunction', tp.FloatType(), True),
    tp.StructField('Age', tp.IntegerType(), True),
    tp.StructField('Outcome', tp.IntegerType(), True)
])
 
# Show and schema
my_data.printSchema()
 
# Replace zero with null for filling missing values
def replace_zero_with_null(df):
    for i, column_name in enumerate(df.columns):
        if i == 0 or i == len(df.columns) - 1:
            continue
        df = df.withColumn(column_name, when(col(column_name) == 0, None).otherwise(col(column_name)))
    return df
 
my_data = replace_zero_with_null(my_data)
my_data.show()
 
# Impute values in null places
imputer = Imputer(
    inputCols=my_data.columns[:-1],  # Exclude the outcome column
    outputCols=my_data.columns[:-1]
).setStrategy("median")
 
my_data1 = imputer.fit(my_data).transform(my_data)
 
# Specify the input and output columns of the vector assembler
assembler = VectorAssembler(
    inputCols=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'],
    outputCol='features'
)
 
final_data = assembler.transform(my_data1)
 
# Split data for train and test
train_data, test_data = final_data.randomSplit([0.8, 0.2])
 
# Train the model
lr = LogisticRegression(featuresCol='features', labelCol='Outcome', maxIter=10)
model = lr.fit(train_data)
 
# Test model
prediction = model.transform(test_data)
prediction.show(5)
 
# Create a pipeline
pipeline = Pipeline(stages=[imputer, assembler, lr])
pipeline_model = pipeline.fit(my_data1)
 
# Create new data for prediction
new_data = spark.createDataFrame(
    [(1, 166, 72, 15, 17, 33.6, 0.627, 50, 0)],
    ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
)
 
# Predict new data through the pipeline
predictions_new_data = pipeline_model.transform(new_data)
predictions_new_data.show()
'''
        )
    elif(num==9):
        print(
            '''
##################################  Bloom Filter ###################################
# bloom filter
def hash1(x):
    return (x + 1) % 17
 
def hash2(x):
    return (3 * x + 2) % 17
 
def compute_hashes(x, size):
    h1 = hash1(x)
    h2 = hash2(x)
    index1 = h1 % size
    index2 = h2 % size
    return h1, h2, index1, index2
 
# Initialize bit array with 0
size = 18
bit_array = [0] * size
 
# Elements to add
elements = [15, 10, 3]
print("Element | h1(x) | h2(x) | Bit Index 1 | Bit Index 2")
print("---------------------------------------------------")
for element in elements:
    h1, h2, index1, index2 = compute_hashes(element, size)
    bit_array[index1] = 1
    bit_array[index2] = 1
    print(f"{element:7} | {h1:5} | {h2:5} | {index1:11} | {index2:11}")
 
# Display the bit array
print("\nBit array after adding elements:")
print(bit_array)
 
# Check new element
new_element = 7
new_h1, new_h2, new_index1, new_index2 = compute_hashes(new_element, size)
 
print(f"\nNew Element: {new_element}")
print(f"Hash1: {new_h1}, Bit Index 1: {new_index1}")
print(f"Hash2: {new_h2}, Bit Index 2: {new_index2}")
 
# Check if the new element is likely present
is_present = bit_array[new_index1] and bit_array[new_index2]
print(f"Is the new element {new_element} in the Bloom filter? {'Yes' if is_present else 'No'}")
 
# Display the updated bit array
print("\nBit array after checking new element:")
print(bit_array)
'''
        )
    elif(num==10):
        print(
            '''
############################### Flajolet Martin ###################################
# flajolet martin
def hash_function1(x):
    return (3 * x + 7) % 32
 
def hash_function2(x):
    return (5 * x + 11) % 32
 
def to_binary_string(value, bit_length=5):
    return format(value, f'0{bit_length}b')
 
def count_trailing_zeros(binary_value):
    return len(binary_value) - len(binary_value.rstrip('0'))
 
# Elements to process
elements = [3, 1, 4, 3, 7, 8]
 
# Prepare table data
table_data = []
max_power_of_two1 = 0  # Initialize the maximum value of 2^r for hash function 1
max_power_of_two2 = 0  # Initialize the maximum value of 2^r for hash function 2
 
for element in elements:
    # Compute hash values for both functions
    hash_value1 = hash_function1(element)
    hash_value2 = hash_function2(element)
 
    # Convert hash values to binary
    binary_value1 = to_binary_string(hash_value1)
    binary_value2 = to_binary_string(hash_value2)
 
    # Count trailing zeros
    r1 = count_trailing_zeros(binary_value1)
    r2 = count_trailing_zeros(binary_value2)
 
    # Compute power of two
    power_of_two1 = 2 ** r1
    power_of_two2 = 2 ** r2
 
    # Update maximum power of two values
    max_power_of_two1 = max(max_power_of_two1, power_of_two1)
    max_power_of_two2 = max(max_power_of_two2, power_of_two2)
 
    # Append row data
    table_data.append((element, hash_value1, binary_value1, r1, power_of_two1,
                       hash_value2, binary_value2, r2, power_of_two2))
 
# Print table headers
print(f"{'Element':<8} | {'Hash 1 Value':<12} | {'Binary 1 Value':<14} | {'Trailing Zeros 1':<17} | {'2^r1':<6} | {'Hash 2 Value':<12} | {'Binary 2 Value':<14} | {'Trailing Zeros 2':<17} | {'2^r2':<6}")
print("-" * 90)
 
# Print table rows
for element, hash_value1, binary_value1, r1, power_of_two1, hash_value2, binary_value2, r2, power_of_two2 in table_data:
    print(f"{element:<8} | {hash_value1:<12} | {binary_value1:<14} | {r1:<17} | {power_of_two1:<6} | {hash_value2:<12} | {binary_value2:<14} | {r2:<17} | {power_of_two2:<6}")
 
# Compute and print the average of the maximum values of 2^r for both hash functions
average_max_power_of_two = (max_power_of_two1 + max_power_of_two2) / 2
print(f"\nMaximum value of 2^r for Hash Function 1: {max_power_of_two1}")
print(f"Maximum value of 2^r for Hash Function 2: {max_power_of_two2}")
print(f"Average of the maximum values of 2^r: {average_max_power_of_two}")
'''
        )
    elif(num==11):
        print(
            '''
################################## Bipartitle Matching #####################################
!pip install networkx
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
        )
    elif(num==12):
        print(
            '''
########################## Betweeness and centrality #######################
# !pip install networkx pandas matplotlib numpy
%matplotlib inline
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import networkx as nx
from IPython.display import display, HTML
 
#Add csv file
twitch_data = pd.read_csv('employees.csv')
twitch_data.head()
 
# Create Graph
G = nx.from_pandas_edgelist(twitch_data,
                            source='FirstName',
                            target='Gender',
                            create_using=nx.DiGraph())
 
#Print Degree
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Average Degree:", np.mean(list(dict(G.degree()).values())))
print("Average In Degree:", np.mean(list(dict(G.in_degree()).values())))
print("Average Out Degree:", np.mean(list(dict(G.out_degree()).values())))
 
#plot graph
nx.draw_networkx(G)
 
# Assuming you have your graph `G` ready
# Example: G = nx.erdos_renyi_graph(100, 0.05)
 
# Compute centrality measures
pagerank = nx.pagerank(G)
betweenness = nx.betweenness_centrality(G)
degree_centrality = nx.degree_centrality(G)
closeness = nx.closeness_centrality(G)
 
# Create a DataFrame to store centrality measures
centrality_df = pd.DataFrame({
    'Node': list(pagerank.keys()),
    'PageRank': list(pagerank.values()),
    'Betweenness': list(betweenness.values()),
    'Degree': list(degree_centrality.values()),
    'Closeness': list(closeness.values())
})
 
# Set the style for the scrollable table (HTML)
scrollable_table_style = """
<style>
    .scrollable-table {
        height: 300px;
        overflow-y: scroll;
        display: block;
    }
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
        text-align: center;
    }
    th {
        background-color: #black;
    }
</style>
"""
 
# Convert DataFrame to HTML and add scrollable div
html_table = centrality_df.to_html(index=False, classes='scrollable-table')
 
# Display the scrollable table with CSS in a Jupyter environment
display(HTML(scrollable_table_style + html_table))
'''
        )
    elif(num==13):
        print(
            '''
######################### Min Hashing shingles ##############################
import pandas as pd
import numpy as np
 
# Define the documents
doc1 = "Today is Monday."
doc2 = "Today is a good day."
doc3 = "Good day."
doc4 = "Tomorrow will be a good day."
documents = [doc1, doc2, doc3, doc4]
 
# Function to generate shingles from text
def generate_shingles(text, kval, token_type):
    if token_type == 'word':
        tokens = text.split()
        shingles = [' '.join(tokens[i:i + kval]) for i in range(len(tokens) - kval + 1)]
    else:  # Assume 'letter'
        shingles = [text[i:i + kval] for i in range(len(text) - kval + 1)]
    return shingles
 
# User inputs
token_type = input("Choose token type (word/letter): ").strip().lower()
kval = int(input("Enter k-value (length of shingles): "))
 
# Generate and print shingles for each document
doc_shingles = []
 
print("\nShingles for each document:")
for doc_index, doc in enumerate(documents):
    shingles = generate_shingles(doc, kval, token_type)
    doc_shingles.append(shingles)
    print(f"\nShingle {doc_index + 1}: {shingles}")
 
# Create a set of all unique shingles
all_shingles = set(shingle for shingles in doc_shingles for shingle in shingles)
 
# Create a DataFrame for shingles
df = pd.DataFrame(columns=["Shingle"] + [f"doc{i + 1}" for i in range(len(documents))])
df["Shingle"] = list(all_shingles)
 
# Fill the DataFrame to indicate presence of shingles
for doc_index, shingles in enumerate(doc_shingles):
    for shingle in shingles:
        df.loc[df["Shingle"] == shingle, f"doc{doc_index + 1}"] = 1
 
# Fill NaN with 0
df = df.fillna(0).astype({'doc1': 'int', 'doc2': 'int', 'doc3': 'int', 'doc4': 'int'})
 
# Hashing
df["Hash1"] = df.index.map(lambda x: (17 * int(x) + 11) % len(df))
df["Hash2"] = df.index.map(lambda x: (7 * int(x) + 11) % len(df))
 
# Create the signature matrix
sig = np.full((2, len(documents)), np.inf)
for index, row in df.iterrows():
    for doc_index in range(len(documents)):
        if row[f"doc{doc_index + 1}"] == 1:
            sig[0, doc_index] = min(sig[0, doc_index], row["Hash1"])
            sig[1, doc_index] = min(sig[1, doc_index], row["Hash2"])
 
# Print the final DataFrame in a formatted table
print("\nShingle Table:")
print(df.to_string(index=False))
 
# Print the signature matrix last
print("\nSignature matrix:")
print(sig)
'''
        )
    elif(num==14):
        print(
            '''
############################### PCY #################################################
 
# PCY
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
 
# Step 1: Get unique items and count occurrences
unique = []
count = {}
 
for transaction in transactions:
    for item in transaction:
        if item not in count:
            count[item] = 0
        count[item] += 1
 
# Filter out items with occurrences <= 1
filtered_unique = [item for item in count if count[item] > 1]
 
print("Filtered unique items (occurrence > 1):", filtered_unique)
 
# Step 2: Create pairs of each unique item from filtered list
pairs = [(filtered_unique[i], filtered_unique[j]) for i in range(len(filtered_unique)) for j in range(i + 1, len(filtered_unique))]
 
print("Pairs of unique items:", pairs)
 
# Step 3: Check if pair is available in transaction and count its occurrences
pair_counts = {}
for pair in pairs:
    count = sum(pair[0] in transaction and pair[1] in transaction for transaction in transactions)
    pair_counts[pair] = count
 
print("Counts of each pair in transactions:", pair_counts)
 
# Step 4: Apply threshold and hash function
threshold = 4
bucket_size = int(input("Enter Bucket Size value: "))
# Hash function
def hash_function(i, j):
    return (i * j) % bucket_size
 
# Filter pairs based on threshold and calculate hash values using item values, not their indices
hash_table = []
for pair, count in pair_counts.items():
    if count >= threshold:
        hash_value = hash_function(pair[0], pair[1])
        hash_table.append((pair, count, hash_value))
 
print("\nFiltered pairs, counts, and hash values:")
for entry in hash_table:
    print(f"Pair: {entry[0]}, Count: {entry[1]}, Hash Value: {entry[2]}")
 
# Step 5: Create a table of pairs, their counts, and their hash values
print("\nTable of pairs, counts, and hash values:")
print("Pair\t\tCount\tHash Value")
for entry in hash_table:
    print(f"{entry[0]}\t{entry[1]}\t{entry[2]}")
'''
        )
    elif(num==15):
        print(
            '''
############################### AMS ####################################################
# AMS
import pandas as pd
 
# Sample data points
data_points = [1 ,2, 7, 1, 4, 9, 4, 6, 1, 6, 4, 4, 5, 5, 5, 9, 8, 7, 2, 2, 4, 4]
 
# Create a DataFrame to store the data points
df = pd.DataFrame({'datapoints': data_points})
 
# Input x_indices from user (1-based index)
x_indices = [2, 5, 8]
 
# Create a new table with X.value, X.element, Occurrences, and Second Moment
output_table = pd.DataFrame(columns=['X.value', 'X.element', 'Occurrences', 'Second Moment'])
 
n = len(data_points)  # Total number of data points
 
for x in x_indices:
    if x - 1 < len(data_points):  # Ensure index is within bounds
        x_value = x
        x_element = df['datapoints'][x - 1]  # Use (x - 1) to adjust for 1-based index
        occurrences = (df['datapoints'] == x_element).sum()  # Count occurrences
 
        # Calculate the second moment
        second_moment = n * (2 * occurrences - 1)
 
        # Append row to output_table using pd.concat
        new_row = pd.DataFrame({
            'X.value': [x_value],
            'X.element': [x_element],
            'Occurrences': [occurrences],
            'Second Moment': [second_moment]
        })
        output_table = pd.concat([output_table, new_row], ignore_index=True)
 
# Calculate the average of the second moments
average_second_moment = output_table['Second Moment'].mean()
 
# Print the output table and average second moment
print(output_table)
print("\nAverage Second Moment:", average_second_moment)
'''
        )
    elif(num==16):
        print('''
################### Min hashing using file upload #########################
import pandas as pd
import numpy as np
 
# Function to read documents from multiple text files
def read_documents_from_files(file_paths):
    documents = []
    for file_path in file_paths:
        docs = pd.read_csv(file_path, header=None, sep="\n")[0].tolist()
        documents.extend(docs)  # Add documents from each file to the list
    return documents
 
# List of file paths
file_paths = ["documents1.txt", "documents2.txt", "documents3.txt"]
 
# Read all documents
documents = read_documents_from_files(file_paths)
 
# Function to generate shingles from text
def generate_shingles(text, kval, token_type):
    if token_type == 'word':
        tokens = text.split()
        shingles = [' '.join(tokens[i:i + kval]) for i in range(len(tokens) - kval + 1)]
    else:  # Assume 'letter'
        shingles = [text[i:i + kval] for i in range(len(text) - kval + 1)]
    return shingles
 
# User inputs
token_type = input("Choose token type (word/letter): ").strip().lower()
kval = int(input("Enter k-value (length of shingles): "))
 
# Generate and print shingles for each document
doc_shingles = []
 
print("\nShingles for each document:")
for doc_index, doc in enumerate(documents):
    shingles = generate_shingles(doc, kval, token_type)
    doc_shingles.append(shingles)
    print(f"\nShingle {doc_index + 1}: {shingles}")
 
# Create a set of all unique shingles
all_shingles = set(shingle for shingles in doc_shingles for shingle in shingles)
 
# Create a DataFrame for shingles
df = pd.DataFrame(columns=["Shingle"] + [f"doc{i + 1}" for i in range(len(documents))])
df["Shingle"] = list(all_shingles)
 
# Fill the DataFrame to indicate presence of shingles
for doc_index, shingles in enumerate(doc_shingles):
    for shingle in shingles:
        df.loc[df["Shingle"] == shingle, f"doc{doc_index + 1}"] = 1
 
# Fill NaN with 0
df = df.fillna(0).astype({f'doc{i+1}': 'int' for i in range(len(documents))})
 
# Hashing
df["Hash1"] = df.index.map(lambda x: (17 * int(x) + 11) % len(df))
df["Hash2"] = df.index.map(lambda x: (7 * int(x) + 11) % len(df))
 
# Create the signature matrix
sig = np.full((2, len(documents)), np.inf)
for index, row in df.iterrows():
    for doc_index in range(len(documents)):
        if row[f"doc{doc_index + 1}"] == 1:
            sig[0, doc_index] = min(sig[0, doc_index], row["Hash1"])
            sig[1, doc_index] = min(sig[1, doc_index], row["Hash2"])
 
# Print the final DataFrame in a formatted table
print("\nShingle Table:")
print(df.to_string(index=False))
 
# Print the signature matrix last
print("\nSignature matrix:")
print(sig)

''')
    elif(num == 17):
        print(
            '''
########################## pyParkPiple Updated ##################################
 
# Import necessary modules
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, DoubleType, StructType, StructField
from pyspark.ml import Pipeline
from pyspark.ml.feature import Imputer, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import pyspark.sql.functions as F
 
# Create a Spark session
spark = SparkSession.builder.appName("DiabetesPredictionPipeline").getOrCreate()
 
# Define the schema for the dataset
schema = StructType([
    StructField('Pregnancies', IntegerType(), True),
    StructField('Glucose', IntegerType(), True),
    StructField('BloodPressure', IntegerType(), True),
    StructField('SkinThickness', IntegerType(), True),
    StructField('Insulin', IntegerType(), True),
    StructField('BMI', DoubleType(), True),
    StructField('DiabetesPedigreeFunction', DoubleType(), True),
    StructField('Age', IntegerType(), True),
    StructField('Outcome', IntegerType(), True)
])
 
# Load the data using the defined schema
data = spark.read.csv("C:/Users/harshvardhan bhosale/Downloads/diabetes.csv", schema=schema, header=True)
 
# Show data and schema
data.printSchema()  # Corrected: Call printSchema() on the DataFrame object
data.show()         # Display the first few rows of the DataFrame
 
# Columns where 0 values are invalid
zero_invalid_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
 
# Replace 0 values with nulls in invalid columns
for col in zero_invalid_cols:
    data = data.withColumn(col, F.when(F.col(col) == 0, None).otherwise(F.col(col)))
 
# Define the feature columns
features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
 
# Imputer to fill missing values (zeros replaced by nulls)
imputer = Imputer(inputCols=features, outputCols=[f"{c}_imputed" for c in features])
 
# Assemble features into a single vector column
assembler = VectorAssembler(inputCols=[f"{c}_imputed" for c in features], outputCol='features')
 
# Logistic Regression classifier
lr = LogisticRegression(featuresCol='features', labelCol='Outcome', maxIter=100)
 
# Create a pipeline with imputation, assembling features, and logistic regression
pipeline = Pipeline(stages=[imputer, assembler, lr])
 
# Split the dataset into training (70%) and test (30%) sets
xtrain, xtest = data.randomSplit([0.7, 0.3], seed=42)
 
# Fit the pipeline model on the training data
model = pipeline.fit(xtrain)
 
# Make predictions on the test data
predictions = model.transform(xtest)
 
# Evaluate the accuracy of the model
evaluator = MulticlassClassificationEvaluator(labelCol="Outcome", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
 
# Output the accuracy
print(f"Model Accuracy: {accuracy}")
 
# Stop the Spark session
spark.stop()

'''
        )
    elif(num == 18):
        print(
            '''
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
 
# Load the CSV data
df = pd.read_csv('/content/Book1.csv')
 
# Create an empty graph
B = nx.Graph()
 
is_bipartite = nx.is_bipartite(B)
print(f"Is the graph bipartite? {is_bipartite}")   ##########extra
 
# Add nodes with the bipartite attribute
B.add_nodes_from(df['source'], bipartite=0)  # Set 1
B.add_nodes_from(df['target'], bipartite=1)  # Set 2
 
# Add edges between the nodes
edges = list(zip(df['source'], df['target']))
B.add_edges_from(edges)
 
# Draw the bipartite graph
pos = nx.bipartite_layout(B, df['source'])
 
 # Position layout for bipartite graph
nx.draw(B, pos, with_labels=True, node_color=['lightblue' if n in df['source'].values else 'lightgreen' for n in B.nodes()])
plt.show()
'''
        )
    else:
        print(
            '''
        1=SparklSQL Create DataFrame and spark session
        2=SparklSQL Join
        3=SparklSQL Grouping
        4=SparklSQL Aggreagation
        5=SparklSQL Various Function
        6=SparkSQL Operations on Table
        7=SparkSQl RDD operations
        8=PySpark with pipline and logistic
        9=Bloom Filter
        10=Flajolet-Martin
        11=Bipartite Matching
        12=Betweenness and Centrality
        13=Min Hashing shingles
        14=PCY
        15=AMS
        16=Min Hashing using file 
        17=pyspark Pipeline Updated code for accuracy
        18 = Bipartite using file

'''
        )