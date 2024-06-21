# Notes for Barb's Job App Assistant



### Resources

Read about [the OpenAI models](https://platform.openai.com/docs/models/gpt-3-5-turbo), which is useful for knowing which model is best to use for various tasks, e.g. generating text for documents or extracting information. 

JSON mode! ...  Extract information from text and return in a structured format:
https://platform.openai.com/docs/guides/text-generation/json-mode

The pricing page is here, it is not particulalry well linked. 
https://openai.com/api/pricing/
https://platform.openai.com/settings/organization/billing/overview


CHAT COMPLETIONS

**gpt-3.5-turbo-0125**  (this is gpt-3.5-turbo)
The latest GPT-3.5 Turbo model with higher accuracy at responding in requested formats and a fix for a bug which caused a text encoding issue for non-English language function calls. Returns a maximum of 4,096 output tokens
Input:   $0.50 /  1M tokens
Output:   $1.50 /  1M tokens


**gpt-3.5-turbo-1106**  
GPT-3.5 Turbo model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens. 
Input:   $1.50 /  1M tokens
Output:   $2.00 /  1M tokens

**gpt-4-turbo-2024-04-09**. (thisi s gpt-4-turbo)
The latest GPT-4 Turbo model with vision capabilities. Vision requests can now use JSON mode and function calling.
Input:   $10.00 /  1M tokens
Output:   $30.00 /  1M tokens


**gpt-4-0613**  (this is gpt-4)
Snapshot of gpt-4 from June 13th 2023 with improved function calling support.	
Input:   $30.00 /  1M tokens
Output:   $60.00 /  1M tokens


**gpt-4-1106-preview** 
GPT-4 Turbo preview model featuring improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens. This is a preview model.
Input:   $10.00 /  1M tokens
Output:   $30.00 /  1M tokens


**got-4o** 
Our most advanced, multimodal flagship model that’s cheaper and faster than GPT-4 Turbo. Currently points to gpt-4o-2024-05-13.	
Input:   $5.00 /  1M tokens
Output:   $15.00 /  1M tokens


**davinci-002**
Input:   $2.00 /  1M tokens
Output:   $2.00 /  1M tokens


**babbage-002**
Input:   $0.40 /  1M tokens
Output:   $0.40 /  1M tokens



<!-- 
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
    {"role": "user", "content": "Who won the world series in 2020?"}
  ]
)
print(response.choices[0].message.content)
 -->