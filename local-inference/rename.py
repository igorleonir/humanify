import guidance
import outlines.text as text

mname = "meta-llama/Llama-2-7b-chat-hf"
guidance.llm = guidance.llms.Transformers(mname, device="mps", caching=False, temperature=0.5)

@text.prompt
def prompt(system_prompt, user_message):
    """
    <s>[INST] <<SYS>>
    {{ system_prompt }}
    <</SYS>>

    {{ user_message }} [/INST]
    Sure! Here's the code with more descriptive variable and function names:"""

def do_prompt(code):
  return prompt("""Task: Rename variables and functions in the given JavaScript code while maintaining its functionality.

Constraints: Use descriptive names. Follow camelCase naming convention.""",
  """Prompt:
Given the following JavaScript code:
"""+code+"""

Rename the variables and functions in the code to make it more readable and maintain its functionality. Use appropriate variable names and follow the camelCase naming convention.""")

def rename(code_before, code_after):
   p = do_prompt(code_before + code_after) + "\n" + code_before + '''{{gen "varname" temperature=0.5 stop_regex="[^a-zA-Z0-9]"}}'''
   print(p)
   result = guidance(p)()
   return result['varname']
