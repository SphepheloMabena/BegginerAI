from sentence_transformers import SentenceTransformer, util
import pickle

# Load a pre-trained Sentence-BERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Define your list of sentences
sentences = ["This is a sample sentence.", "Another example sentence."]

# Compute Sentence-BERT embeddings for your sentences
embeddings = model.encode(sentences, convert_to_tensor=True)

# Specify the file path where you want to save the embeddings
output_file = "sentence_bert_embeddings.pkl"

# Serialize and save the embeddings to the file using pickle
with open(output_file, "wb") as f:
    pickle.dump(embeddings, f)

print(f"Sentence-BERT embeddings saved to {output_file}")
