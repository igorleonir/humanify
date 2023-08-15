from transformers import AutoModelForCausalLM, AutoTokenizer
mname = "stabilityai/stablecode-instruct-alpha-3b"
#mname = "stabilityai/stablecode-completion-alpha-3b"

tokenizer = AutoTokenizer.from_pretrained(mname)
model = AutoModelForCausalLM.from_pretrained(
  mname,
  trust_remote_code=True,
  torch_dtype="auto",
)
model.to("mps")

input_code = """
###Instruction
Code a monad class in Typescript

###Response
class Monad<T> {
"""

inputs = tokenizer(input_code, return_tensors="pt", return_token_type_ids=False).to("mps")

last_printed = 0

# Generate new tokens, so that we print the new code every 10 tokens
# and feed the new tokens back into the model
for i in range(0, 100):
  tokens = model.generate(
    **inputs,
    max_new_tokens=10,
    temperature=0.2,
    do_sample=True,
    pad_token_id=0,
  )
  out = tokenizer.decode(tokens[0], skip_special_tokens=True)
  inputs = tokenizer(out, return_tensors="pt", return_token_type_ids=False).to("mps")

  # Print the new code
  print(out[last_printed:], end="")
  last_printed = len(out)


