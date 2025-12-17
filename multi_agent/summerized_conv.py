from typing import Callable

from models.google_api import GoogleModel, google_assistant_format, google_user_format
from models.azure_api import Model as AzureModel, azure_user_format, azure_assistant_format

from functools import partial

from models.model_base import ModelBase
from multi_agent.multi_agent import Problem, Role
from models.prompt_template import Rejector, Solver, Summarizer

def summarized_rejection_sampling_google(model:GoogleModel, name:str, n_steps: int, problem: Problem) -> list[dict]:
     result = summarized_rejection_sampling(
          model=model, 
          name=name, 
          n_steps = n_steps, 
          problem = problem,
          user_format = google_user_format,  
          assistant_format = google_assistant_format)
     
     return result


def summarized_rejection_sampling_azure(model:AzureModel, name:str, n_steps: int, problem: Problem) -> list[dict]:
     result = summarized_rejection_sampling(
          model=model, 
          name=name, 
          n_steps = n_steps, 
          problem = problem,
          user_format = azure_user_format,  
          assistant_format = azure_assistant_format)
     
     return result



def summarized_rejection_sampling(model:ModelBase, name:str, n_steps: int, problem: Problem,user_format,  assistant_format ) -> list[dict]:
     def P(iteration: int,  role: Role, msg: list[str]) -> dict:
          return prompt(
               model=model,
                conv_name = name,
                problem_posed = problem.pose_problem(),
                user_format = user_format,
                assistant_format=assistant_format,
                iteration=iteration,
                instruction=role.instruction(),
                role_name = role.name,
                context = msg
          )
     pre_pended_problem = user_format(problem.pose_problem())
     final_summary = assistant_format(summarized_loop(n=n_steps, P=P, solver=Solver, rejecter=Rejector, summarizer=Summarizer))
     return [pre_pended_problem, final_summary]
     
 

def prompt(iteration: int, role_name: str, model: ModelBase, conv_name:str, problem_posed: str, user_format, instruction: str, context: list[str], assistant_format):
        # context = [x for x in context if x ] # rm empty string
        user_msg = user_format(f"What do you say, {role_name}")
        if isinstance(model, GoogleModel):
            messages = [user_format(problem_posed)] + context
            messages +=[user_msg]
            reply, raw = model.send_msg_and_get_contnent(msg=messages, instruction=instruction)

        else:
            messages = [{"role": "system", "content": instruction}]
            messages +=[user_format(problem_posed)]
            messages += [assistant_format("\n".join(context))]  #[assistant_format(x) for x in context] 
            messages +=[user_msg]
            reply, raw = model.send_msg_and_get_contnent(msg=messages)
        
        print(f"\n{role_name}: \n{reply}")
        model.save_conv(
             name=f"{conv_name}_{iteration}_{role_name}",
             raw =[raw],
             messages=messages + [assistant_format(reply)]
        )

        return reply


def summarized_loop(
    n: int,
    P: Callable,
    solver: Role = Solver,
    rejecter: Role = Rejector,
    summarizer: Role = Summarizer,
) -> str:


    Z_im2 = ""
    Z_im1 = ""
    R_im1 = ""
    S_im1 = ""


     

    for i in range(n):
        # Run iteration
        print(f"Iteration {i}")
        S_i = f"Solver:  {P(i, role=solver, msg=[Z_im2, S_im1, R_im1])}"
        R_i = f"Rejector:  {P(i, role=rejecter, msg=[Z_im1, S_i])}"
        Z_i = f"Summarizer:  {P(i, role=summarizer, msg=[Z_im1, S_i, R_i])}"

        # Prepare for next iteration
        S_im1 = S_i

        Z_im2 = Z_im1
        Z_im1 = Z_i

        R_im1 = R_i
    print("\n -----FINAL SUMMARY----- \n")
    print(Z_i)
    return Z_i




"""
0
S0 = S()
R0 = R(S())
Z0 = Z(S0, R0)

1
S1 = S(S0, R0)
R1 = R(Z0, S1)
Z1 = (Z0, S1, R1)

2
S2 = S(Z0, S1, R1)
R2 = R(Z1,S2)
Z2 = Z(Z1, S2, R2)

3
S3 = S(Z1, S2, R2)
R3 = R(Z2, S3)
Z3 = Z(Z2, S3, R3)


Si = (Z_im2, S_im1, R_im1)
Ri = R(Z_im1, S_i)
Z_i = Z_im1, S_i, R_i)
"""