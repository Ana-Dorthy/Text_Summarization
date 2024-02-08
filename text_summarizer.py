import tkinter as tk
from tkinter import filedialog
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance 
import numpy as np
import networkx as nx

def read_article(file_name):
    with open(file_name, "r") as file:
        filedata = file.readlines()
        article = filedata[0].split(". ")
        sentences = [sentence.replace("[a-zA-Z)"," ").split(" ") for sentence in article]
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)

def gen_sim_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix

def generate_summary(file_name, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []
    sentences = read_article(file_name)
    sentence_similarity_matrix = gen_sim_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    summary = ""
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    summary = ". ".join(summarize_text)
    return summary

def browse_file():
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(tk.END, file_path)

def generate_summary_gui():
    file_path = entry.get()
    top_n = int(entry_top_n.get())
    summary = generate_summary(file_path, top_n)
    text_summary.delete(1.0, tk.END)
    text_summary.insert(tk.END, summary)

root = tk.Tk()
root.title("Text Summarization")

frame = tk.Frame(root)
frame.pack(pady=20)

label_file = tk.Label(frame, text="Select a text file:")
label_file.grid(row=0, column=0)

entry = tk.Entry(frame, width=50)
entry.grid(row=0, column=1)

button_browse = tk.Button(frame, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2)

label_top_n = tk.Label(frame, text="Number of sentences in summary:")
label_top_n.grid(row=1, column=0)

entry_top_n = tk.Entry(frame, width=10)
entry_top_n.grid(row=1, column=1)
entry_top_n.insert(tk.END, "5")

button_generate = tk.Button(frame, text="Generate Summary", command=generate_summary_gui)
button_generate.grid(row=1, column=2)

text_summary = tk.Text(root, width=60, height=10)
text_summary.pack(pady=20)

root.mainloop()
