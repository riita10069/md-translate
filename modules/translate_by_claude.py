import boto3
import json

from modules import prompt

bedrock_runtime_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def translate_by_claude(content):
    body = json.dumps({
        "prompt": "Human:" + prompt.prompt.format(content) + "\n\nAssistant:",
        "max_tokens_to_sample": 2000,
        "temperature": 0.1,
        "top_p": 0.9,
    })

    response = bedrock_runtime_client.invoke_model(
        body = body,
        modelId="anthropic.claude-v2",
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response.get('body').read()).get('completion')

    return response_body.replace("<translated>", "").replace("</translated>", "").lstrip()
