import os
import re
import boto3
import botocore
import click
import requests
import json

from modules import const

# init amazon translate client
boto3Client = boto3.client(service_name='translate')

DEEPL_API_FREE_ENDPOINT = 'https://api-free.deepl.com/v2/translate'
DEEPL_API_PRO_ENDPOINT = 'https://api.deepl.com/v2/translate'

def translate(text, src_lang, dest_lang, deepl_free, deepl_pro):
    transaltedText = ""

    if deepl_free or deepl_pro:
        # use DeepL
        if os.getenv('DEEPL_API_KEY') is None:
            raise Exception(
                "Please provide authentication key via the DEEPL_API_KEY environment variable"
            )
        params = {
            'auth_key': os.environ.get('DEEPL_API_KEY'),
            'text': text,
            'source_lang': str.upper(src_lang),
            'target_lang': str.upper(dest_lang)
        }

        try:
            response = requests.post(DEEPL_API_FREE_ENDPOINT if deepl_free else DEEPL_API_PRO_ENDPOINT, data=params)
            response.raise_for_status()
            result = json.loads(response.content.decode('utf-8'))
            transaltedText = result['translations'][0]['text']

        except requests.exceptions.HTTPError as e:
            print('Failed to translate by DeepL API Free.')
            raise e


    else:
        # use Amazon Translate
        try:
            result = boto3Client.translate_text(
                Text=text,
                SourceLanguageCode=src_lang,
                TargetLanguageCode=dest_lang)
            transaltedText = result.get('TranslatedText')

        except botocore.exceptions.ClientError as e:
            print('Failed to translate by Amazon Translate.')
            raise e

        except botocore.exceptions.ParamValidationError as e:
            raise ValueError('The parameters you provided are incorrect: {}'.format(e))

    return transaltedText


def translateAst(ast, src_lang, dest_lang, deepl_free, deepl_pro):
    result_children = []

    for child_node in ast[const.CHILDREN_TYPE]:
        if child_node[const.TYPE_TYPE] in ["leafDirective", "containerDirective"] and child_node[const.NAME_TYPE] == const.TYPE_CODE:
            result_children.append(child_node)
        else:
            if const.CHILDREN_TYPE in child_node.keys():
                result_children.append(translateAst(child_node, src_lang, dest_lang, deepl_free, deepl_pro))
            else:
                result_children.append(translateNode(child_node, src_lang, dest_lang, deepl_free, deepl_pro))

    ast[const.CHILDREN_TYPE] = result_children

    return ast


def translateNode(node, src_lang, dest_lang, deepl_free, deepl_pro):
    if node[const.TYPE_TYPE] in [const.TYPE_CODE, const.TYPE_STRONG, const.TYPE_EMPHASIS, const.TYPE_INLINE_CODE, const.TYPE_HTML]:
        pass
    else:
        if const.VALUE_TYPE in node.keys():
            translatedValue = translate(node[const.VALUE_TYPE], src_lang, dest_lang, deepl_free, deepl_pro)
            node[const.VALUE_TYPE] = translatedValue

    return node
