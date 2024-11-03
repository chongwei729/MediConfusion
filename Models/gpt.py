import os
import base64
import openai 
from dotenv import load_dotenv
from openai import OpenAI



def get_client(max_retries=2, timeout=10):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI()

    return client

def get_response(client, deployment_name, init_prompt, prompt, temperature, max_retry=3, print_error=False):
    counter = max_retry
    response_text = None
    first_logprob = None

    while counter > 0:
        try:
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {"role": "system", "content": init_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                logprobs=True,
                top_logprobs=3,
            )

            response_text = response.choices[0].message.content

            if response.choices[0].logprobs and response.choices[0].logprobs.content:
                first_token_logprob_info = response.choices[0].logprobs.content[0]
                first_logprob = first_token_logprob_info.logprob  

            break  
        except Exception as e:
            if print_error:
                print(e)
            counter -= 1  

    return response_text, first_logprob


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def ask_question(client, image_path, question, init_prompt, deployment_name, temperature):
    base64_image = encode_image(image_path)
    content = [
        {"type": "text",
            "text": question
        },
        {"type": "image_url",
            "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }
    ]
    response, logprob = get_response(client=client,
                                deployment_name='gpt-4o', 
                                init_prompt=init_prompt, 
                                prompt=content,
                                temperature=temperature)

    return response, logprob