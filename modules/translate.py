import os
import re
import boto3
import click
import requests
import json

from modules import const

# init amazon translate client
boto3Client = boto3.client(service_name='translate')

DEEPL_API_ENDPOINT = 'https://api-free.deepl.com/v2/translate'

def translate(text, src_lang, dest_lang, deepl):
    transaltedText = ""

    if deepl:
        # use DeepL
        params = {
            'auth_key': os.environ.get('DEEPL_API_KEY'),
            'text': text,
            'source_lang': str.upper(src_lang),
            'target_lang': str.upper(dest_lang)
        }
        try:
            response = requests.post(DEEPL_API_ENDPOINT, data=params)
            response.raise_for_status()
            result = json.loads(response.content.decode('utf-8'))
            transaltedText = result['translations'][0]['text']

        except requests.exceptions.HTTPError as e:
            raise e

    else:
        # use Amazon Translate
        result = boto3Client.translate_text(
            Text=text,
            SourceLanguageCode=src_lang,
            TargetLanguageCode=dest_lang)
        transaltedText = result.get('TranslatedText')

    return transaltedText


def translateAst(ast, src_lang, dest_lang, deepl):
    result_children = []

    for child_node in ast[const.CHILDREN_TYPE]:
        if child_node[const.TYPE_TYPE] in ["leafDirective", "containerDirective"] and child_node[const.NAME_TYPE] == const.TYPE_CODE:
            result_children.append(child_node)
        else:
            if const.CHILDREN_TYPE in child_node.keys():
                result_children.append(translateAst(child_node, src_lang, dest_lang, deepl))
            else:
                result_children.append(translateNode(child_node, src_lang, dest_lang, deepl))

    ast[const.CHILDREN_TYPE] = result_children

    return ast


def translateNode(node, src_lang, dest_lang, deepl):
    if node[const.TYPE_TYPE] in [const.TYPE_CODE, const.TYPE_STRONG, const.TYPE_EMPHASIS, const.TYPE_INLINE_CODE]:
        pass
    else:
        if const.VALUE_TYPE in node.keys():
            translatedValue = translate(node[const.VALUE_TYPE], src_lang, dest_lang, deepl)
            node[const.VALUE_TYPE] = translatedValue

    return node
