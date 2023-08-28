# GPT Utility Library and Applications

This repository contains a set of utility functions and tools for working with GPT (Generative Pre-trained Transformer) models in different contexts. It includes applications like AnkiGPT for flashcard creation and Slide Tools for lecture slide processing.

## Table of Contents

- [GPT Utility Library and Applications](#gpt-utility-library-and-applications)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Util Functions](#util-functions)
    - [gpt.py](#gptpy)
    - [input.py](#inputpy)
    - [tokens.py](#tokenspy)
  - [Applications](#applications)
    - [AnkiGPT](#ankigpt)
    - [Slide Tools](#slide-tools)
  - [Examples](#examples)
    - [Simple Example](#simple-example)
    - [Parallel Example](#parallel-example)
  - [Contributing](#contributing)

## Installation

1. Clone the repository

   ```bash
   git clone https://github.com/BertilBraun/GPT-Tools.git
   ```

2. Install the requirements

   ```bash
   pip install -r requirements.txt
   ```

3. Place your OpenAI API key in a file named `openai-api-key.txt` at the root of the project.

## Util Functions

### gpt.py

```python
chat_completion(messages: list[str], system_message: str = SYSTEM_PROMPT, model: str = DEFAULT_MODEL, stream_output: bool = False) -> str
```

Chat completion function.

```python
gpt_in_parallel(messages: list[list[str]], system_message: str = SYSTEM_PROMPT, model: str = DEFAULT_MODEL) -> list[str]
```

Run multiple GPT sessions in parallel.

```python
create_embedding(input: str) -> list[float]
```

Create an embedding of the input text.

### input.py

```python
input_from_clipboard(prompt: str = CLIPBOARD_PROMPT) -> str
```

Reads input from the clipboard.

```python
multiline_input(prompt: str) -> str
```

Allows multiline input from the user.

### tokens.py

```python
count_tokens_in_messages(messages: list[str]) -> int
```

Counts the tokens in a list of messages.

```python
count_tokens(text: str) -> int
```

Counts tokens in a given text.

```python
chunk_string_by_tokens(s, start_words=3000, max_tokens=4000)
```

Chunks a string by token count.

## Applications

### AnkiGPT

Automatically generates flashcards for learning content. Great for summarizing lectures or creating study materials.

### Slide Tools

Processes lecture slides to extract relevant topics and summarize lectures.

## Examples

### Simple Example

```python
from util.gpt import chat_completion

# Define your prompts template
PROMPT_TEMPLATE = "The topic you should summarize: {}"

# Topics to summarize
TOPICS = ["Math", "Physics", "Chemistry"]

# Loop through each topic
for topic in TOPICS:
    prompt = PROMPT_TEMPLATE.format(topic)

    # Get summary from GPT using chat_completion
    summary = chat_completion([prompt])

    print(f"Topic: {topic}\nSummary: {summary}\n\n")

```

### Parallel Example

```python
from util.gpt import gpt_in_parallel

# Define your prompts template
PROMPT_TEMPLATE = "The topic you should summarize: {}"

TOPICS = ["Math", "Physics", "Chemistry"]

# Generate prompts based on the topics
prompts = [[PROMPT_TEMPLATE.format(topic)] for topic in TOPICS]

# Get summaries from GPT
summaries = gpt_in_parallel(prompts)

for topic, summary in zip(TOPICS, summaries):
    print(f"Topic: {topic}\nSummary: {summary}\n\n")
```

## Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!
