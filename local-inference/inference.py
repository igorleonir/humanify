from typing import List
from enum import Enum
from typing import Tuple
from pydantic import BaseModel, constr

import outlines.models as models
import outlines.text.generate as generate
import outlines.text as text

class Name(str, Enum):
    x = "x"
    y = "y"
    z = "z"
    a = "a"

class NameNewnamePair(BaseModel):
    name: Name
    newname: constr(min_length=5, max_length=20)


class NameNewnamePairs(BaseModel):
    name_newname_pairs: List[NameNewnamePair]

@text.prompt
def prompt(system_prompt, user_message):
    """
    <s>[INST] <<SYS>>
    {{ system_prompt }}
    <</SYS>>

    {{ user_message }} [/INST]
    Sure! Here's the code with more descriptive variable names:"""

p = prompt("""Task: Rename variables in the given JavaScript code while maintaining its functionality.

Constraints: Use descriptive variable names. Follow camelCase naming convention.""",
"""Prompt:
Given the following JavaScript code:
function a(e,t){var n=[];var r=e.length;var i=0;for(;i<r;i+=t){if(i+t<r){n.push(e.substring(i,i+t))}else{n.push(e.substring(i,r))}}return n}

Rename the variables in the code to make it more readable and maintain its functionality. Use appropriate variable names and follow the camelCase naming convention.
""")

print(p)
#mname = "meta-llama/Llama-2-7b-chat-hf"
mname = "meta-llama/Llama-2-13b-chat-hf"
#mname = "stabilityai/stablecode-instruct-alpha-3b"
#mname = "stabilityai/stablecode-completion-alpha-3b"
model = models.transformers(mname, "mps")
gen1 = generate.continuation(model, max_tokens=20)
gen2 = generate.regex(model, r"[a-z][a-zA-Z]{1,15}", max_tokens=10)

pass

