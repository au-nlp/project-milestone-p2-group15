# Appendix


## Repo organisation

### P2 Delivery
For the P2 Delivery, we need the TA's to look into the Jupyter file [main.ipynb](main.ipynb) and [multi_agent_demo.ipynb](multi_agent_demo.ipynb)

### Utility
For clean code, we also created several Python functions spread out through different modules. We do not expect the TA to look into this.

### other_notebooks
For our experiments, we created many different notebooks that are only for development. These are stores in the [other_notebooks](other_notebooks) folder. Again, we do not expect the TA to look into this.

### Data
We store our MathArena data and Conversations with the Large langauge models in a folder called data. For github, we only upload the conversations. The data can be generated using the script in main.ipynb. 

## Category 
We tried two approaches to generate Category Labels for the MathArena dataset. We do not expect the TA to look into this, but here are the files, if they are interested: 
1) One approach is using keyword matching, see [train_4_tiny_models](other_notebooks\train_4_tiny_models.ipynb) - code is still a sketch, but is likely dropped for P3.
2) One approach is trying in context learning - see [in_context_learning](other_notebooks/in_context_learning/incontext_demo.ipynb). Achieves 73 % accuracy. 