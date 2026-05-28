from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

text = [
    "I love dogs",
    "I love puppies"
]

embedding = model.encode(text)

print("Number of embeddings:", len(embedding))

print("Shape:", embedding.shape)

print("\nFirst sentence embedding first 10 values:")
print(embedding[0][:10])

print("\nSecond sentence embedding first 10 values:")
print(embedding[1][:10])