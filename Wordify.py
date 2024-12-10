"""

file: Wordify.py

Description: A reusable library for text analysis and comparison
The framework supports any collection of texts
of interest 

Possible sources of texts

- gutenburg texts
- political speech
- tweet compilations
- corporate filings
- philosophy treatises
- letters, journals, diaries
- blogs
- news articles


The core data structure:

Input: "A" --> raw text,  "B" --> another text

Extract wordcounts:
        "A" --> wordcounts_A,   "B" --> wordcounts_B, ......

What get stored:

        "wordcounts"  --->   {"A" --> wordcounts_A,
                              "B" --> wordcounts_B, etc.}

        e.g., dict[wordcounts][A] --> wordcounts_A



"""

import plotly.graph_objects as go
from collections import defaultdict, Counter
import random as rnd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Wordify_parsers import clean_text


class Wordify:

    def __init__(self):
        """ Constructor

        datakey --> (filelabel --> datavalue)
        """
        self.data = defaultdict(dict)
        self.stop_words = set()
        self.max_files = 10  # Limit to 10 files
        self.file_count = 0


    def default_parser(self, filename):
        """ Parse a standard text file and produce
        extracted data results in the form of a dictionary,
        while filtering out stop words. """
        with open(filename, 'r') as file:
            text = file.read()
        
        # Split the text into words
        text = clean_text(text)
        words = text.split()
        
        # Filter out stop words (convert words to lowercase for comparison)
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        
        # Create results dictionary with word count and total word count
        results = {
            'wordcount': Counter(filtered_words),
            'numwords': len(filtered_words)
        }

        return results


    def load_stop_words(self, stopwords_file):
            """ Load a list of stop words from a file """
            with open(stopwords_file, 'r') as file:
                self.stop_words = {word.strip() for word in file if word.strip()}


    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework.
        Extract and store data to be used later by
        the visualizations """


        if self.file_count >= self.max_files:
            print("Maximum file limit reached. Cannot load more files.")
            return
        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v
        
        self.file_count += 1



    def create_sankey_diagram(self, word_list=None, k=5):
        # Extract data
        file_labels = list(self.data['wordcount'].keys())
    


        # Collect topk unique words across files
        if word_list is None:
            unique_words = set()
            for label in file_labels:
                top_words = [word for word, _ in self.data['wordcount'][label].most_common(k)]
                unique_words.update(top_words)
        else:
            unique_words = set(word_list)
        
        # Convert to a list to define nodes
        word_list = list(unique_words)
        labels = file_labels + word_list

        # Define links for Sankey diagram
        sources = []
        targets = []
        values = []

        # Add links for File1
        for file_idx, file_label in enumerate(file_labels):
            for word, count in self.data['wordcount'][file_label].items():
                if word in word_list:
                    sources.append(file_idx)  # File index as source
                    targets.append(len(file_labels) + word_list.index(word))  # Word index as target
                    values.append(count)  # Word frequency as value

            # Create Sankey diagram
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels

            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        ))

        # Show the figure
        fig.update_layout(title_text="Basic Text-to-Word Sankey Diagram", font_size=10)
        fig.show()

    def create_heatmap(self, top_n=10):
        """
        Create a heatmap based on word frequencies across multiple files.
        
        Parameters:
        - tt: An instance of Textastic with loaded text files.
        """
        # Extract file labels and all unique words
        file_labels = list(self.data['wordcount'].keys())


        total_word_counts = Counter()
        for label in file_labels:
            total_word_counts.update(self.data['wordcount'][label])

        # Get the top N words
        top_words = [word for word, _ in total_word_counts.most_common(top_n)]

        # Build the frequency matrix
        frequency_matrix = []
        for word in top_words:
            row = [self.data['wordcount'][file].get(word, 0) for file in file_labels]
            frequency_matrix.append(row)

        # Convert to DataFrame for easier plotting
        df = pd.DataFrame(frequency_matrix, index=top_words, columns=file_labels)

        # Create the heatmap
        plt.figure(figsize=(10, 8))
        plt.imshow(df, aspect='auto', cmap='viridis')
        plt.colorbar(label='Frequency')
        plt.xticks(ticks=np.arange(len(file_labels)), labels=file_labels, rotation=45)
        plt.yticks(ticks=np.arange(len(top_words)), labels=top_words)
        plt.title('Word Frequency Heatmap')
        plt.xlabel('Files')
        plt.ylabel('Words')
        plt.tight_layout()
        plt.show()

    def create_word_length_hist(self, num_cols=2):
        """
        Create a histogram of word lengths, giving each song its own subplot.
        
        Parameters:
        - data (dict): A dictionary where keys are song labels and values are tokens (list of words).
        - num_cols (int): Number of columns in the subplot grid.
        """
        # Extract song labels and word tokens
        file_labels = list(self.data['wordcount'].keys())
        num_songs = len(file_labels)

        # Determine subplot grid dimensions
        num_rows = int(np.ceil(num_songs / num_cols))

        # Create subplots
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
        axes = axes.flatten()  # Flatten to easily iterate over all subplots

        # Plot histograms
        for i, label in enumerate(file_labels):
            ax = axes[i]
            word_lengths = [len(word) for word in self.data['wordcount'][label]]  # Calculate word lengths
            ax.hist(word_lengths, bins=range(1, max(word_lengths) + 2), color='blue', alpha=0.7)
            ax.set_title(f"Word Lengths in {label}")
            ax.set_xlabel("Word Length")
            ax.set_ylabel("Frequency")

        # Turn off unused subplots
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')

        # Adjust layout
        
        plt.subplots_adjust(wspace=0.3, hspace=0.4)  # Add more space between plots

        plt.show()

