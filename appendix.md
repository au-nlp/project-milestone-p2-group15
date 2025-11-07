# Appendix


## Repo organisation
We store our MathArena data and Conversations with the Large langauge models in a folder called data. For github, we only upload the conversations. The data can be generated using the script in main.ipynb. 


## Category 
We tried two approaches: 
1) One approach is using keyword matching, see [train_4_tiny_models](other_notebooks\train_4_tiny_models.ipynb) - code is still a sketch, but is likely dropped for P3.
2) One approach is trying in context learning - see [in_context_learning](other_notebooks/in_context_learning/incontext_demo.ipynb). Achieves 73 % accuracy. 