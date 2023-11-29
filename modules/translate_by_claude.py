import boto3
import json
from bs4 import BeautifulSoup
from botocore.config import Config
from modules import prompt

bedrock_runtime_client = boto3.client(service_name='bedrock-runtime',
                                      region_name='us-east-1',
                                      config=Config(connect_timeout=300, read_timeout=300, retries={'max_attempts': 1}))

def translate_by_claude(content):
    body = json.dumps({
        "prompt": "\n\nHuman: " + prompt.prompt.format(content) + "\n\nAssistant:",
        "max_tokens_to_sample": 8000,
        "temperature": 0.1,
        "stop_sequences": ["\n\nHuman"],
    })

    response = bedrock_runtime_client.invoke_model(
        body = body,
        modelId="anthropic.claude-instant-v1",
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response.get('body').read()).get('completion')

    soup = BeautifulSoup(response_body, 'html.parser')
    
    translated_text = str(soup.find('translated'))
    return translated_text.replace("<translated>", "").replace("</translated>", "").lstrip()
