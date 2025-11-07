
# PROMPTING STRATEGIES TO ENCOURAGE EXPLORATION OF DIFFERENT METHODS ON DIFFERENT LARGE-LANGUAGE MODELS
Group 15

## Abstract (150)

In this project, we demonstrate an alternative prompting strategy to the classic chain-of-thought prompting when dealing with fixed-answer math problems. The prompting strategy is a multi-agent/multi-role strategy for structuring how the model reasons and force the model to show a vast solution space. Among our most effective role-based strategy is the "Solver + Rejector" strategy where the "Solver" role must generate a set of unique answers. Then, the rejector's job is to reject whatever the solver outputs and encourages to explore further to solve the problem. This is to counteract a common issues where a model gets stuck on early suggestions. 

Finally, the Model is asked to rank each of the answers it had suggested so far which we show, can be used to solve problems in the dataset that the model couldn't previously solve.


## Contributions

Our contributions are twofold. Firstly, we demonstrate that current models are capable of providing correct answers to the questions that could not be solved previously in the MathArena dataset by replacing the standard reasoning "let's verify it step-by-step" prompt with a role-based-multi-agent that "encourages" exploration of a vast solution space.

Secondly, we demonstrate that the raw performance of a selected set of models is increased by making the model map out the most plausible answer out of the subset of answers it had generated previously.

This directly addresses one of the core issues that the authors of the MathArena competition mentioned (cite paper), where models get stuck/too confident on a single answer and cannot continue to explore new answers.

## MathArena Dataset and paper

We used the MathArena Dataset that consists of Math Problems asked in various competitions, compiled by Huggingface, it is a dataset specifically made to test different LLMs of their mathematical reasoning capabilities. For this project, we drop all the proof-answer-based and image-based questions as we cannot study and verify those questions with our current resources. While the dataset is not huge, our free language model API usage are limited, thus, we select a subset of problems based on difficulty and (in the future) category as well as a subset of models.

## Methods 

We use a prompting strategies involving multiple agents, possibly even different LLMs in future. Our most promising multi-agent strategy is an actor-critic inspired method commonly seen in Reinforcement Learning. 

The basic setup is to have a Solver Agent (Actor) in charge of finding and providing the reasoning of various solutions. The crucial part is the addition of a Rejector Agent (critic). This agent will act as if it knows the correct answer, but, will reject any output and reasoning of the solver and encourage it to keep trying for new solutions with emphasis on "uniqueness, exploration and low-confidence". The uniqueness constraint enforces that a conversation of n-steps yields n-unique solutions.

After this, we must extract the correct answer among the n-proposed answers. For now, we just use a simple method of just asking the model to rank each of the answers.

In future, we will add more nuance to the roles where we might test the possibility of multiple LLMs taking different roles and adding other role-types.

## Code

For the preprocessing of the dataset as well as a few visualizations, we refer to the notebook [main.ipynb](main.ipynb). In addition, we have provided a short demo of our method in action, used on the *Deepseek-R1* model. We showcase two problems that the model, when tested in the competitions, never got those right even once; but, with this method, it can solve those problems.

## Timeline

In the Bibliography, we have listed a number of sources. Since our P3 delivery requires a rigourous testing setup, we will use the papers for inspiration. 

For this project, we propose the following tentative timeline

- Week 46: A discussion on feedback from Project Milestone P2 and further literature research.
- Week 47: Implement multi-agents for different LLMs and see their feasibility. Find ways to tweak the result to make it less computationally expensive.
- Week 48: Decide on final selection of models to test and also decide on which methods to use and abbreviation studies to focus on.
- Week 49: Decide on the final problems to be tested. Start writing report.
- Week 50: Run tests, write report.
- Week 51: Final report writing and confirmation.


## Bibliography

- [Evaluating LLMs on Uncontaminated Math Competitions](https://arxiv.org/pdf/2505.23281)
- [A Survey Of Self-Evolving Agents: On Path To Artificial Super Intelligence](https://arxiv.org/abs/2507.21046)
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/pdf/2201.11903)
- [Let’s Verify Step by Step](https://arxiv.org/pdf/2305.20050)

## Appendix

For appendix, see appendix.md