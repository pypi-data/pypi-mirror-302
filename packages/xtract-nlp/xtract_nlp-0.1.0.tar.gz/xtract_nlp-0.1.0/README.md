# **xTrAct-NLP**: Code Querying with NLP Models

xTrAct-NLP is a tool for processing a codebase, generating embeddings for code chunks using pre-trained NLP models, and querying the codebase using natural language to retrieve relevant code snippets. It can be used both as a Python library and a CLI tool.

## **Features**

- Process codebases and divide them into meaningful segments (functions, classes, etc.).
- Generate embeddings for code chunks using models like CodeBERT or any Hugging Face transformer model.
- Query codebases with natural language questions and retrieve relevant code snippets.

## **Introducing TRACE: Targeted Retrieval and Contextual Embedding**

One of the key concepts behind **xTrAct-NLP** is the idea of **TRACE** (Targeted Retrieval and Contextual Embedding). The system is built to address the challenge of working with large codebases that don’t fit within a single context window of models like GPT-4. TRACE allows xTrAct-NLP to break the code down into smaller, meaningful chunks, generate embeddings for these chunks, and then retrieve the most relevant parts based on your natural language query.

Instead of overwhelming the language model with an entire codebase, TRACE ensures that only the most relevant code snippets are passed along. This approach optimizes both performance and accuracy, making it easier for models like GPT-4 to provide useful insights on large, complex codebases.

## **Installation**

Install xTrAct-NLP via `pip`:

```
pip install xtract-nlp
```

Alternatively, to install it from source for development:

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd xTrAct-NLP
   ```
3. Install the package locally in editable mode:
   ```
   pip install -e .
   ```

## **Usage**

### **CLI Usage**

xTrAct-NLP provides a CLI for processing codebases, generating embeddings, and querying code snippets.

#### **1. Process a Codebase**

To process a codebase and divide it into functions, classes, and other meaningful segments:

```
python -m xtract.cli process /path/to/codebase
```

This will save the code chunks to a file (`code_chunks.pt`) for use in subsequent steps.

#### **2. Generate Embeddings**

After processing the codebase, generate embeddings for the code chunks using a pre-trained model like CodeBERT:

```
python -m xtract.cli generate --model_name microsoft/codebert-base
```

This will generate and save the embeddings to `code_embeddings.pt`.

#### **3. Query the Codebase**

Once embeddings are generated, you can query the codebase using natural language:

```
python -m xtract.cli query "How is data loaded?" --top_k 3
```

This will return the top 3 most relevant code snippets based on the query.

### **Library Usage**

xTrAct-NLP can also be used as a Python library. Here's how to get started:

#### **1. Process a Codebase**

```
from xtract.core import process_codebase

# Process the codebase

num_chunks = process_codebase("/path/to/codebase")
print(f"Processed {num_chunks} code chunks.")
```

#### **2. Generate Embeddings**

```
from xtract.core import generate_embeddings

# Generate embeddings for the processed code

num_embeddings = generate_embeddings("microsoft/codebert-base")
print(f"Generated {num_embeddings} embeddings.")
```

#### **3. Query the Codebase**

```
from xtract.core import query_codebase

# Query the codebase with a natural language question

results = query_codebase("How is data loaded?", top_k=3)
for i, snippet in enumerate(results):
print(f"Result {i+1}: {snippet}")
```

## **Configuration**

- **Model Selection**: You can choose any Hugging Face transformer model to generate embeddings. The default is `microsoft/codebert-base`, but you can specify other models using the `--model_name` option in the CLI or in the library.

## **Requirements**

- Python 3.7+
- PyTorch
- Hugging Face Transformers
- Click (for the CLI)
- Scikit-learn (for cosine similarity)

## **License**

xTrAct-NLP is licensed under the MIT License. See `LICENSE` for more information.
