# jetbrains_pubtrends

### GEO Dataset Clustering from PMIDs
This project implements a pipeline to cluster GEO dataset descriptions using TF-IDF and Affinity Propagation. It reads a list of PubMed PMIDs from a text file, retrieves the corresponding GEO IDs and dataset details from the NCBI eUtils API, constructs combined text documents from selected fields, vectorizes them using TF-IDF, and clusters the datasets based on their text similarity.

## Overview
The pipeline performs the following steps:
1. Input Processing:
Reads a file containing PubMed PMIDs (one per line).

2. Data Retrieval:
For each PMID, uses the NCBI eUtils API to fetch associated GEO IDs.
For each GEO ID, retrieves dataset details (Title, Summary, Experiment Type, Organism) via the efetch API.

4. Text Representation:
Constructs a combined document for each dataset by concatenating the fields.

6. TF-IDF Vectorization:
Uses scikit-learn’s TfidfVectorizer to convert the documents into numerical vectors (ignoring common English stop words).

7. Similarity and Clustering:
Computes cosine similarity (and a derived distance matrix) between datasets.
Clusters the datasets using Affinity Propagation, which automatically determines the optimal number of clusters.

## Installation
### Prerequisites
Python 3.6 or higher

### Dependencies
Install the required Python packages using the provided requirements.txt:

pip install -r requirements.txt


The requirements.txt contains:

requests>=2.25.1
scikit-learn>=0.24.2

## Usage
### Prepare the Input File
Create a text file (e.g., PMIDs_list.txt) with one PubMed PMID per line.

### Run the Script
Execute the script from the command line by specifying your PMIDs file:
python script.py PMIDs_list.txt

## Output

The script prints the list of collected GEO IDs.
It retrieves dataset details and builds combined documents.
TF-IDF vectors, cosine similarity, and a derived distance matrix are computed.
Finally, Affinity Propagation clusters the datasets and prints the cluster labels.
