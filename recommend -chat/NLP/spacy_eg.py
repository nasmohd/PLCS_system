import spacy

# Load the language model
nlp = spacy.load("en_core_web_sm")

# Define the text to analyze
text = "Apple is looking at buying U.K. startup for $1 billion"

# Apply the model to the text
doc = nlp(text)

# Extract the named entities
entities = [(ent.text, ent.label_) for ent in doc.ents]

# Print the results
print(entities)
#[('Apple', 'ORG'), ('U.K.', 'GPE'), ('$1 billion', 'MONEY')]