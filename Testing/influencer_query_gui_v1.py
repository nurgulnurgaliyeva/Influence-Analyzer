import tkinter as tk
from tkinter import ttk, scrolledtext
import chromadb
from chromadb.utils import embedding_functions
import json

# Initialize ChromaDB client outside of the function
client = chromadb.PersistentClient(path="./chroma_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def load_collection(client, file_path='sentiment_analysis_collection_export.json'):
    # Check if the collection already exists
    try:
        collection = client.get_collection(name="sentiment_analysis", embedding_function=sentence_transformer_ef)
        print("Collection 'sentiment_analysis' already exists. Using existing collection.")
    except ValueError:
        # If the collection doesn't exist, create it and load the data
        print(f"Collection 'sentiment_analysis' does not exist. Creating new collection from {file_path}")
        collection = client.create_collection(name="sentiment_analysis", embedding_function=sentence_transformer_ef)
        
        with open(file_path, 'r') as f:
            export_data = json.load(f)
        
        # Split data into batches of 1000
        batch_size = 1000
        for i in range(0, len(export_data['ids']), batch_size):
            end = min(i + batch_size, len(export_data['ids']))
            collection.add(
                ids=export_data['ids'][i:end],
                embeddings=export_data['embeddings'][i:end],
                documents=export_data['documents'][i:end],
                metadatas=export_data['metadatas'][i:end]
            )
            print(f"Added batch {i//batch_size + 1}")

    return collection

# Load the collection at startup
collection = load_collection(client)

def print_results(query, results):
    output = f"\nQuery: '{query}'\n"
    output += f"Number of results: {len(results['documents'][0])}\n"
    for doc, metadata, distance in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        output += "-" * 50 + "\n\n"
        output += f"User: {metadata['user']}\n"
        output += f"Distance: {distance}\n"
        output += f"Category: {metadata['category']}\n"
        output += f"Sentiment Category: {metadata['sentiment_category']}\n"
        output += f"Sentiment Score: {metadata['sentiment_score']}\n"
        output += f"Likes: {metadata['likes']}\n"
        output += f"Followers: {metadata['followers']}\n"
        output += f"Location: {metadata['location']}\n"
        output += f"Captions: {metadata['cleaned_captions']}\n"
        output += f"Comments: {metadata['cleaned_comments']}\n"
        output += f"Tags: {metadata['tags']}\n"
    return output

def submit_query():
    prompt = prompt_text.get("1.0", tk.END).strip()
    num_influencers = num_influencers_entry.get().strip()
    
    if not prompt or not num_influencers.isdigit() or int(num_influencers) < 1 or int(num_influencers) > 99:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please enter a valid prompt and a number between 1 and 99.")
        return

    num_influencers = int(num_influencers)
    results = collection.query(
        query_texts=[prompt],
        n_results=num_influencers,
        include=['documents', 'distances', 'metadatas']
    )
    
    output = print_results(prompt, results)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)

# Create the main window
root = tk.Tk()
root.title("Influencer Query GUI")

# Create and pack the prompt input
prompt_label = ttk.Label(root, text="Enter your prompt here:")
prompt_label.pack(pady=(10, 0))
prompt_text = scrolledtext.ScrolledText(root, height=5, width=50)
prompt_text.pack(pady=(0, 10))

# Create and pack the number of influencers input
num_influencers_label = ttk.Label(root, text="Enter the number of influencers you want:")
num_influencers_label.pack()
num_influencers_entry = ttk.Entry(root, width=5)
num_influencers_entry.pack(pady=(0, 10))

# Create and pack the submit button
submit_button = ttk.Button(root, text="Submit", command=submit_query)
submit_button.pack(pady=(0, 10))

# Create and pack the result display
result_text = scrolledtext.ScrolledText(root, height=20, width=80)
result_text.pack(pady=(0, 10))

# Start the GUI event loop
root.mainloop()
