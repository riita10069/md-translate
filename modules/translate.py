import re
import boto3
import click

from modules import const

# init amazon translate client
boto3Client = boto3.client(service_name='translate')


def translate(text, src_lang, dest_lang):
    # 翻訳
    result = boto3Client.translate_text(
        Text=text,
        SourceLanguageCode=src_lang,
        TargetLanguageCode=dest_lang)
    transaltedText = result.get('TranslatedText')

    return transaltedText


def translateAst(ast, src_lang, dest_lang):
    result_children = []

    for child_node in ast[const.CHILDREN_TYPE]:
        if child_node[const.TYPE_TYPE] in ["leafDirective", "containerDirective"] and child_node[const.NAME_TYPE] == const.TYPE_CODE:
            result_children.append(child_node)
        else:
            if const.CHILDREN_TYPE in child_node.keys():
                result_children.append(translateAst(child_node, src_lang, dest_lang))
            else:
                result_children.append(translateNode(child_node, src_lang, dest_lang))

    ast[const.CHILDREN_TYPE] = result_children

    return ast


def translateNode(node, src_lang, dest_lang):
    if node[const.TYPE_TYPE] in [const.TYPE_CODE, const.TYPE_STRONG, const.TYPE_EMPHASIS, const.TYPE_INLINE_CODE]:
        pass
    else:
        if const.VALUE_TYPE in node.keys():
            translatedValue = translate(node[const.VALUE_TYPE], src_lang, dest_lang)
            node[const.VALUE_TYPE] = translatedValue

    return node
