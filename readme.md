
# P3 - REJECTION SAMPLING: A GENERAL PROMPTING STRATEGY TO ENCOURAGE EXPLORATION
Group 15

## Update from P2: 

Sections like Abstract, contibutions, and other report related sectons have been moved the PDFs. We also removed the timeline and the model demo form p2. All of this can be review againing by selecting the P2 tag if desired. 

## Repository Structure

<details>
<summary>Click to expand folder structure</summary>

``` bash
├───baselines/
│   ├───reflexion/  # Folder that has the code for Reflexion
│   └───tot/ # Folder implementing ToT
├───data/
│   ├───all_answers_pd/ 
│   ├───all_problems_pd/
│   └───conversations/ # Saved conversations for all the problems using Rejection-sampling and summarized Rejection-sampling
├───data_processing/
├───models/ # Folder storing the Azure/Google API workings and prompt templates
├───multi_agent/ # Stores code for Rejection-sampling and summarized Rejection-sampling
├───results/ # Stores the results of each LLM for each method: Deepseek-R1, Gemini-2.5, GPT-5-Nano
│   └───model_stats/ # Stores code to visualize the results from each model
```

<details>

## Code

- For the preprocessing of the dataset as well as a few visualizations, we refer to the notebook [main.ipynb](main.ipynb).
- We created a setups for Tree-of-thought and Reflexion in baselines folder. This includes a modified copy of the repo [https://github.com/princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm).
- To use the official ToT implementation, we had to create a Task class for MathArena questiosn and what the promts should look like, see results/model_stats. This then used by the ToT repos BFS tree search which is only slightly modified, see [bfs.py](baselines/tot/tree_of_thought_llm_master/src/tot/methods/bfs.py). Finally, we changed the offical repo API calls to make it compatible with Azure and Google API, see [models.py](baselines/tot/tree_of_thought_llm_master/src/tot/models.py)
- Similarly, we modify the official Reflexion Repository from [https://github.com/noahshinn/reflexion](https://github.com/noahshinn/reflexion). We make it simpler and work for our use case since the official repo dealt primarily with the Wikipedia dataset. For our version of implementation see [reflexion.py](baselines\reflexion\reflexion.py).
- Code specific to our method in both Azure and googe API variant is in folder multi_agent. 
- Finally, all the sessions where the 3 selected models are run on the selected problems can be found in results folder. The data about each models reponse to each problem usign each method is saved in csv files in results/model_stats. This is then loaded in the main.ipynb file to create the barcharts which are also present in the report. 

We leave much of the preprocessing as in P2, and just load and visualuze the main resutls in the main.ipynb. 
