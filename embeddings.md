
# The OpenAI Embeddings API

## Learn how to turn text into numbers, unlocking use cases like search.

### New embedding models

- `text-embedding-3-small` and `text-embedding-3-large`, our newest and most performant embedding models are now available, with lower costs, higher multilingual performance, and new parameters to control the overall size.

### What are embeddings?

- OpenAI’s text embeddings measure the relatedness of text strings.
- Embeddings are commonly used for:
  - Search (where results are ranked by relevance to a query string)
  - Clustering (where text strings are grouped by similarity)
  - Recommendations (where items with related text strings are recommended)
  - Anomaly detection (where outliers with little relatedness are identified)
  - Diversity measurement (where similarity distributions are analyzed)
  - Classification (where text strings are classified by their most similar label)
- An embedding is a vector (list) of floating point numbers. The distance between two vectors measures their relatedness. Small distances suggest high relatedness and large distances suggest low relatedness.

### How to get embeddings

- To get an embedding, send your text string to the embeddings API endpoint along with the embedding model name (e.g. `text-embedding-3-small`). The response will contain an embedding (list of floating point numbers), which you can extract, save in a vector database, and use for many different use cases.

#### Example: Getting embeddings

```python
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-3-small"
)

print(response.data[0].embedding)
```

#### Example embedding response

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [
        -0.006929283495992422,
        -0.005336422007530928,
        ...,
        -4.547132266452536e-05,
        -0.024047505110502243
      ]
    }
  ],
  "model": "text-embedding-3-small",
  "usage": {
    "prompt_tokens": 5,
    "total_tokens": 5
  }
}
```

### Embedding models

- OpenAI offers two powerful third-generation embedding models (denoted by -3 in the model ID).

### Use cases

- The Amazon fine-food reviews dataset is used for the following examples to illustrate various use cases like obtaining embeddings, reducing embedding dimensions, and more.

### Obtaining the embeddings

- The dataset contains a total of 568,454 food reviews Amazon users left up to October 2012. A subset of 1,000 most recent reviews is used for illustration purposes.

### Reducing embedding dimensions

- Both of our new embedding models were trained with a technique that allows developers to trade-off performance and cost of using embeddings. Specifically, developers can shorten embeddings without the embedding losing its concept-representing properties by passing in the `dimensions` API parameter.

### Frequently asked questions

- **How can I tell how many tokens a string has before I embed it?**
  - In Python, you can split a string into tokens with OpenAI's tokenizer `tiktoken`.

- **How can I retrieve K nearest embedding vectors quickly?**
  - For searching over many vectors quickly, we recommend using a vector database.

- **Which distance function should I use?**
  - We recommend cosine similarity.

Peanuts...but the peanuts were actually small sized unsalted. Not sure if this was an error or if the vendor intended to represent the product as such.