![PromptSearcher Logo](./assets/small_avatar.jpeg)

# PromptSearcher

PromptSearcher is an automatic tool designed to find the best prompt in both supervised and unsupervised scenarios. This project draws inspiration from traditional neural network learning techniques.

## Overview

The core concept of PromptSearcher revolves around the idea of "gradients" in prompt engineering. Here, the gradients represent the best prompts that guide the results towards improved scores.

## Key Features

- Automatic prompt optimization
- Support for both supervised and unsupervised learning
- Inspired by neural network learning principles
- Gradient-based approach to prompt improvement

## How It Works

PromptSearcher iteratively refines prompts by analyzing the performance of each variation. The system identifies the most effective prompts (the "gradients") that lead to better outcomes, allowing for continuous improvement in prompt quality.

## Applications

This tool can be particularly useful in various fields where prompt engineering plays a crucial role, such as:

- Natural Language Processing (NLP)
- Conversational AI
- Content Generation
- Information Retrieval

## Getting Started

1. Install Poetry if you haven't already:
   ```
   pip install poetry
   ```

2. Clone the repository and navigate to the project directory:
   ```
   git clone https://github.com/octaviusp/PromptSearcher.git
   cd promptsearcher
   ```

3. Install the project dependencies:
   ```
   poetry install
   ```

4. Create a `.env` file in the project root directory and add your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Run the main script:
   ```
   poetry run python prompt_searcher.py
   ```

## Example Usage

Here is an example of how to use PromptSearcher in your project:

```python
from os import getenv
from dotenv import load_dotenv

# Import core components
from prompt_searcher.core import (
    Backpropagation, 
    NaiveSimilarity, 
    ObjectivePrompt,
    PromptSearch,
)

# Import agents
from prompt_searcher.core.agents.openai_agent import OpenAIAgent
from prompt_searcher.core.agents.groq_agent import GroqAgent

load_dotenv()

if __name__ == "__main__":

    GROQ_API_KEY = getenv("GROQ_API_KEY")
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    
    gemma2_9b_it = GroqAgent(api_key=GROQ_API_KEY, model="gemma2-9b-it")
    llama_3_70b = GroqAgent(api_key=GROQ_API_KEY, model="llama-3.1-70b-versatile")
    gpt_4o = OpenAIAgent(api_key=OPENAI_API_KEY, model="gpt-4o")

    loss_function = NaiveSimilarity(evaluator=gpt_4o)
    backpropagation = Backpropagation(augmentator=llama_3_70b)

    objective_prompt = ObjectivePrompt(initial_prompt="You're a mathematical assistant")

    prompt_search = PromptSearch(
        epochs=5,
        backpropagation=backpropagation,
        loss_function=loss_function,
        objective_prompt=objective_prompt,
        student=gemma2_9b_it, 
        dataset_path="tests/data/math1.csv",
        verbose=True)
    
    prompt_search.train()
    best_prompt, best_score = prompt_search.get_results()

    print(best_score)
    print(best_prompt)

    prompt_search.plot_score_history() # Plot a matplotlib graph of the score history
```

   Result of plot score history (REMEMBER WE ARE USING NAIVE SIMILARIITY, SO HIGHER IS BETTER):

   ![Score History](./assets/plot.png)


   Interpretation of plot:

   The plot shows the score history of the prompt search. The x-axis represents the epoch number, and the y-axis represents the score. The score is calculated using the loss function. Depends on your implementation of loss function, the plot may be different. 

   We saw that with the first prompt the score is the lower, meaning that the first prompt is not good.
   In second epoch we got a very strong result, inclusive better than next ones until the last epoch.

   The last epoch is the best prompt of all, so, we can retrieve the best prompt and use it in our project with:

   ```python
   best_prompt = prompt_search.get_best_prompt()
   ```






