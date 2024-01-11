import boto3
import json
from bs4 import BeautifulSoup
from botocore.config import Config
from modules import prompt
import unicodedata

bedrock_runtime_client = boto3.client(service_name='bedrock-runtime',
                                      region_name='us-west-2',
                                      config=Config(connect_timeout=300, read_timeout=300, retries={'max_attempts': 20, 'mode':'standard'}))

def translate_by_claude(content):
    body = json.dumps({
        "prompt": "\n\nHuman: " + prompt.prompt.format(content)  + "\n\nAssistant:",
        "max_tokens_to_sample": 8000,
        "temperature": 0,
        "stop_sequences": ["\n\nHuman"],
    })

    response = bedrock_runtime_client.invoke_model(
        body = body,
        modelId="anthropic.claude-v2:1",
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response.get('body').read()).get('completion')

    soup = BeautifulSoup(response_body, 'html.parser')

    translated_text = str(soup.find('translated'))
    translated_text = (translated_text.replace('re:Post', 're\:Post').
                       replace('re:post', 're\:post').
                       replace('re:Invent', 're\:Invent').
                       replace('re:invent', 're\:invent').
                       replace('&amp;', '&').
                       replace('&gt;', '>').
                       replace('&lt;', '<').
                       replace("<translated>", "").
                       replace("</translated>", "").
                       replace("<no-translate>", "").
                       replace("</no-translate>", "").strip())
    translated_text = insert_space_between_full_and_half_width_chars(translated_text)

    return translated_text

def insert_space_between_full_and_half_width_chars(text):
    new_text = ""
    prev_char = None
    for char in text:
        if prev_char is not None and prev_char != " " and char != " ":
            if ((unicodedata.east_asian_width(prev_char) in 'FWA' and unicodedata.east_asian_width(char) not in 'FWA') or
                (unicodedata.east_asian_width(prev_char) not in 'FWA' and unicodedata.east_asian_width(char) in 'FWA')):
                new_text += " "
        new_text += char
        prev_char = char
    return new_text

def translate_by_claude_for_hugo_front_matter(content):
    body = json.dumps({
        "prompt": "\n\nHuman: " + prompt.prompt_hugo_front_matter.format(content) + "\n\nAssistant:",
        "max_tokens_to_sample": 8000,
        "temperature": 0,
        "stop_sequences": ["\n\nHuman"],
    })

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId="anthropic.claude-v2:1",
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response.get('body').read()).get('completion')

    soup = BeautifulSoup(response_body, 'html.parser')

    translated_text = str(soup.find('translated'))
    return translated_text.replace("<translated>", "").replace("</translated>", "").strip()

