#!/usr/bin/env python3
import sys
import requests
import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AffinityPropagation

pmid_list = []
geo_ids = []
titles = []
summaries = []
experiment_types = []
organisms = []
documents = []


def get_geo_ids(pmid):
    uri = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=gds&linkname=pubmed_gds&id={pmid}&retmode=xml'
    response = requests.get(uri, timeout=10)
    root = ET.fromstring(response.text)
    ids = []
    for linksetdb in root.findall(".//LinkSetDb"):
        for link in linksetdb.findall("Link"):
            id_elem = link.find("Id")
            ids.append(id_elem.text)
    return ids


def get_data(geo_id):
    uri = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gds&id={geo_id}&retmode=xml'
    response = requests.get(uri, timeout=10)
    text = response.text
    lines = text.splitlines()
    titles.append(lines[1][2:].strip())
    summaries.append(lines[2][20:].strip())
    experiment_types.append(lines[4][5:].strip())
    organisms.append(lines[3][9:].strip())


def main():
    global pmid_list, geo_ids, titles, summaries, experiment_types, organisms, documents

    if len(sys.argv) < 2:
        print("Usage: python script.py <PMIDs_file>")
        sys.exit(1)
    pmid_file = sys.argv[1]

    with open(pmid_file, "r") as file:
        for line in file:
            pmid_list.append(line.strip())

    for pmid in pmid_list:
        geo_ids.extend(get_geo_ids(pmid))

    for geo_id in geo_ids:
        get_data(geo_id)

    for title, summary, organism, experiment_type in zip(titles, summaries, organisms, experiment_types):
        doc = f"{title} {summary} {organism} {experiment_type}"
        documents.append(doc)

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    cosine_sim = cosine_similarity(tfidf_matrix)
    distance_matrix = 1 - cosine_sim
    print("Distance Matrix:\n")
    print(distance_matrix)

    tfidf_dense = tfidf_matrix.toarray()
    aff_prop = AffinityPropagation(random_state=47)
    aff_prop.fit(tfidf_dense)
    cluster_labels = aff_prop.labels_
    print("Affinity Propagation Cluster Labels:\n")
    print(cluster_labels)


if __name__ == '__main__':
    main()
