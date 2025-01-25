import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import chromadb
from chromadb.utils import embedding_functions
import json
import warnings
warnings.filterwarnings("ignore")
 
# Function to load the ChromaDB JSON file and create a collection if it doesn't exist
def create_collection_if_not_exists(client, json_path, collection_name, batch_size=500):
    existing_collections = [col.name for col in client.list_collections()]
    print(f"Existing collections: {existing_collections}")
    
    if collection_name in existing_collections:
        collection = client.get_collection(name=collection_name)
        print(f"Collection '{collection_name}' loaded successfully.")
    else:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        print("Creating collection...")
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        collection = client.create_collection(
            name=collection_name,
            embedding_function=sentence_transformer_ef
        )
 
        num_documents = len(data['documents'])
        for i in range(0, num_documents, batch_size):
            batch_documents = data['documents'][i:i+batch_size]
            batch_metadatas = data['metadatas'][i:i+batch_size]
            batch_ids = data['ids'][i:i+batch_size]
            collection.add(
                documents=batch_documents,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            print(f"Batch {i//batch_size + 1} of {num_documents//batch_size + 1} added successfully.")
 
        print(f"Collection '{collection_name}' created successfully from '{json_path}'.")
    
    return collection
 
# Initialize ChromaDB client
client = chromadb.Client()
 
# Define file locations
json_path = 'sentiment_analysis_collection_export.json'
collection_name = "sentiment_analysis"
 
# Create the collection if it doesn't exist
collection = create_collection_if_not_exists(client, json_path, collection_name)
 
# Function to perform the query and display results
def on_submit():
    query_text = prompt_textbox.get("1.0", tk.END).strip()
    try:
        n_results = int(number_entry.get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")
        return
 
    if not query_text or n_results <= 0:
        messagebox.showerror("Input Error", "Please provide a valid query and a positive number of results.")
        return
 
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=['documents', 'distances', 'metadatas']
        )
        
        output_textbox.config(state=tk.NORMAL)  # Temporarily enable editing
        output_textbox.delete("1.0", tk.END)
        
        if len(results['documents'][0]) == 0:
            output_textbox.insert(tk.END, "No results found.\n")
        else:
            for i, (doc, metadata, distance) in enumerate(zip(results['documents'][0], results['metadatas'][0], results['distances'][0])):
                output_textbox.insert(tk.END, f"Result {i+1}:\n", "result")
                output_textbox.insert(tk.END, f"Distance: {distance:.4f}\n", "distance")
                output_textbox.insert(tk.END, f"User: {metadata['user']}\n", "user")
                output_textbox.insert(tk.END, f"Location: {metadata['location']}\n")
                output_textbox.insert(tk.END, f"Category: {metadata['category']}\n")
                output_textbox.insert(tk.END, f"Tags: {metadata['tags']}\n")
                output_textbox.insert(tk.END, f"Sentiment Category: {metadata['sentiment_category']}\n")
                output_textbox.insert(tk.END, f"Sentiment Score: {metadata['sentiment_score']}\n")
                output_textbox.insert(tk.END, f"Likes: {metadata['likes']}\n")
                output_textbox.insert(tk.END, f"Followers: {metadata['followers']}\n")
                output_textbox.insert(tk.END, f"Caption: {metadata['cleaned_captions']}\n")
                output_textbox.insert(tk.END, f"Comments: {metadata['cleaned_comments']}\n")
                output_textbox.insert(tk.END, "-" * 70 + "\n")
        
        output_textbox.config(state=tk.DISABLED)  # Disable editing after inserting text
    
    except Exception as e:
        messagebox.showerror("Query Error", f"An error occurred during the query: {e}")
 
# Initialize the main window
window = tk.Tk()
window.title("GUI Query Application")
 
# Set initial window size
window.geometry("800x600")
 
# Set a consistent font
font = ("Arial", 12)
 
# Create main frame
main_frame = ttk.Frame(window, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)
 
# Configure grid
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(3, weight=1)
 
# Textbox for entering prompts
ttk.Label(main_frame, text="Enter Query:", font=font).grid(row=0, column=0, sticky="w", pady=(0, 5))
prompt_textbox = tk.Text(main_frame, height=5, width=50, font=font)
prompt_textbox.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
 
# Frame for number entry and submit button
input_frame = ttk.Frame(main_frame)
input_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
input_frame.columnconfigure(1, weight=1)
 
# Entry box for the number of results to return
ttk.Label(input_frame, text="Number of Results:", font=font).grid(row=0, column=0, sticky="w", padx=(0, 10))
number_entry = ttk.Entry(input_frame, width=5, font=font)
number_entry.grid(row=0, column=1, sticky="w")
 
# Style configuration
style = ttk.Style()
style.configure(
    "Submit.TButton",
    background="blue",
    foreground="white",
    font=("Arial", 12, "bold"),
    padding=(10, 5)
)

# Submit button
submit_button = ttk.Button(input_frame, text="Submit", command=on_submit, style="Submit.TButton")
submit_button.grid(row=0, column=2, sticky="e")

# Output area
ttk.Label(main_frame, text="Output:", font=font).grid(row=3, column=0, sticky="w", pady=(0, 5))
output_textbox = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=font, state=tk.DISABLED)
output_textbox.grid(row=4, column=0, sticky="nsew")
 
# Configure tag colors
output_textbox.tag_configure("result", foreground="blue", font=("Arial", 12, "bold"))
output_textbox.tag_configure("distance", foreground="green")
output_textbox.tag_configure("user", foreground="red")
 
# Create and pack the submit button
# submit_button = ttk.Button(root, text="Submit", command=submit_query, style="Submit.TButton")
# submit_button.pack(pady=(0, 10))
 
# Start the Tkinter event loop
window.mainloop() 