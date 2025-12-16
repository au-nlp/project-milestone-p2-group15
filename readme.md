
# P3 - REJECTION SAMPLING: A GENERAL PROMPTING STRATEGY TO ENCOURAGE EXPLORATION
Group 15

## Update from P2: 

Sections like Abstract, contibutions, and other report related sectons have been moved the PDFs. We also removed the timeline and the model demo form p2. All of this can be review againing by selecting the P2 tag if desired. 


## Code

- For the preprocessing of the dataset as well as a few visualizations, we refer to the notebook [main.ipynb](main.ipynb).
- We created a setups for Tree-of-though and Reflexion in baselines folder. This include a modified copy of the repo https://github.com/princeton-nlp/tree-of-thought-llm.
- To use the official ToT implementation, we had to create a Task class for MathArena questiosn and what the promts should look like, see results/model_stats. This then used by the ToT repos BFS tree search which is only slightly modified, see baselines/tot/tree_of_thought_llm_master/src/tot/methods/bfs.py. Finally, we changed the offical repo API calls to make it compatable with Azure and Google API, see baselines/tot/tree_of_thought_llm_master/src/tot/models.py
-  

Code specific to our method in both Azure and googe API variant is in folder multi_agent. Finally, all the sessions where the 3 selected models are run on the selected problems can be found in results folder. The data about each models reponse to each problem usign each method is saved in csv files in results/model_stats. This is then loaded in the main.ipynb file to create the barcharts which are also present in the report. 

We leave much of the preprocessing as in P2, and just load and visualuze the main resutls in the main.ipynb. 
