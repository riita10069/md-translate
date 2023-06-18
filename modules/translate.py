import os
import re
import boto3
import botocore
import click
import requests
import json
import datetime

from modules import const
from modules import processing

# init amazon translate client
boto3Client = boto3.client(service_name='translate')

DEEPL_API_FREE_ENDPOINT = 'https://api-free.deepl.com/v2/translate'
DEEPL_API_PRO_ENDPOINT = 'https://api.deepl.com/v2/translate'


class Translator:
    def __init__(self, dictionary_path, src_lang, dest_lang, deepl_free, deepl_pro, lookup_table, custom_dictionary_path):
        self.dictionary_path = dictionary_path
        self.translate_history = {}  # <src_word>: <tgt_word>
        self.custom_words = {}  # <src_word>: <tgt_word>
        self.custom_words_patterns = {}  # <src_word>: <re:pattern>
        self.src_lang = src_lang
        self.dest_lang = dest_lang
        self.deepl_free = deepl_free
        self.deepl_pro = deepl_pro
        self.lookup_table = lookup_table

        if dictionary_path != "":

            if custom_dictionary_path:
                with open(custom_dictionary_path, 'r', encoding="utf-8") as f:
                    custom_dictionary = json.load(f)
                    for k, v in custom_dictionary.items():
                        self.custom_words[k] = v

            with open(os.path.join(self.dictionary_path, 'base_custom_words.json'), 'r', encoding="utf-8") as f:
                for k, v in json.load(f).items():
                    self.custom_words[k] = v

            with open(os.path.join(self.dictionary_path, 'base_ignore_words.json'), 'r', encoding="utf-8") as f:
                for n in json.load(f):
                    self.custom_words[n] = n

            self.custom_words = {k: v for k, v in
                            sorted(self.custom_words.items(), key=lambda item: len(item[0]), reverse=True)}
            for w in self.custom_words:
                self.custom_words_patterns[w] = re.compile(r"(?:^|\b)" + re.escape(w) + r"(?:$|\b)")

    def save_dictionaries(self):
        if self.dictionary_path != "":
            saving_history = self.translate_history.copy()
            with open(os.path.join(self.dictionary_path,
                                   datetime.datetime.now().strftime('translation_history_%Y-%m-%d_%H:%M:%S.json')), "w+",
                      encoding="utf-8") as fp:
                json.dump(saving_history, fp, ensure_ascii=False, indent=4)

    def translate(self, text):
        # 辞書利用がない場合は、特に処理なし。
        if self.dictionary_path == "":
            return self.translate_text(text)

        # テキストを単文に分割。ピリオドで区切るが、区切りたくないピリオドもあるので（Mt. Fuji など）、泥臭く分割する
        sentences = re.sub(r"\b(Mr|Ms|Dr|Mt|Jr|Sr|Dept|Co|Corp|Inc|Ltd|Univ|etc|or its affiliates|\d)\.", r"\1#PERIOD#",
                           text)
        sentences = [s.replace("#PERIOD#", ".").strip() for s in re.split(r"(?<=\.)\s+", sentences) if
                     len(s.strip()) > 0]

        translated_text = ""
        results = []
        for sentence in sentences:
            # すでに同じ文を翻訳経験あるなら、その履歴を流用
            if sentence in self.translate_history.keys():
                tgt_sentence = self.translate_history[sentence]
            # おなじ文がまるまる辞書にあるなら、そのまま訳語を流用
            elif sentence in self.custom_words.keys():
                tgt_sentence = self.custom_words[sentence]
            # 文のなかの一部の単語が辞書にあるなら、キーワード有りの翻訳を実施
            elif any(self.custom_words_patterns[key].search(sentence) for key in self.custom_words.keys()):
                tgt_sentence = self.translate_text_with_keyword(sentence)
            # 文のなかに辞書にある単語が含まれていないなら、普通に翻訳を実施
            else:
                tgt_sentence = self.translate_text(sentence)
            # 翻訳履歴に追加
            self.translate_history[sentence] = tgt_sentence
            results.append(tgt_sentence)

        translated_text = "".join(results)
        return translated_text

    def translate_text_with_keyword(self, src_text):
        # 辞書登録されているキーワードのうち、どれがsrc_text 中に含まれるか判定する
        # 複数ヒットする可能性もあるので、forを継続。
        for src_word in self.custom_words.keys():
            # key: src_word の時の値が、src_textに含まれているかどうかをチェック
            if self.custom_words_patterns[src_word].search(src_text):
                # lookup_table を使って変換する
                id = "http://no-translate-" + processing.next_alphabet(self.lookup_table['current_alphabet']) + ".dev"
                self.lookup_table['current_alphabet'] = processing.next_alphabet(self.lookup_table['current_alphabet'])
                self.lookup_table["ids"].append(id)
                src_text = re.sub(self.custom_words_patterns[src_word], id, src_text)

                # lookup_tableの中身を代入する。
                print(self.custom_words[src_word])
                self.lookup_table[id] = {
                    "leaf_types": [const.TYPE_TEXT],
                    "leaf_value": self.custom_words[src_word]
                }
        # 翻訳の実行
        translated_text = self.translate_text(src_text)

        return translated_text

    def translate_text(self, text):
        transaltedText = ""
        if self.deepl_free or self.deepl_pro:
            # use DeepL
            if os.getenv('DEEPL_API_KEY') is None:
                raise Exception(
                    "Please provide authentication key via the DEEPL_API_KEY environment variable"
                )
            params = {
                'auth_key': os.environ.get('DEEPL_API_KEY'),
                'text': text,
                'source_lang': str.upper(self.src_lang),
                'target_lang': str.upper(self.dest_lang)
            }

            try:
                response = requests.post(DEEPL_API_FREE_ENDPOINT if self.deepl_free else DEEPL_API_PRO_ENDPOINT,
                                         data=params)
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
                    SourceLanguageCode=self.src_lang,
                    TargetLanguageCode=self.dest_lang)
                transaltedText = result.get('TranslatedText')

            except botocore.exceptions.ClientError as e:
                print('Failed to translate by Amazon Translate.')
                raise e

            except botocore.exceptions.ParamValidationError as e:
                raise ValueError('The parameters you provided are incorrect: {}'.format(e))

        return transaltedText

    def translateAst(self, ast):
        result_children = []

        for child_node in ast[const.CHILDREN_TYPE]:
            if child_node[const.TYPE_TYPE] in ["leafDirective", "containerDirective"] \
                    and child_node[const.NAME_TYPE] == const.TYPE_CODE:
                result_children.append(child_node)
            else:
                if const.CHILDREN_TYPE in child_node.keys():
                    result_children.append(self.translateAst(child_node))
                else:
                    result_children.append(self.translateNode(child_node))

        ast[const.CHILDREN_TYPE] = result_children

        return ast

    def translateNode(self, node):
        if node[const.TYPE_TYPE] in [const.TYPE_CODE, const.TYPE_STRONG, const.TYPE_EMPHASIS, const.TYPE_INLINE_CODE,
                                     const.TYPE_HTML]:
            pass
        else:
            if const.VALUE_TYPE in node.keys():
                translatedValue = self.translate(node[const.VALUE_TYPE])
                node[const.VALUE_TYPE] = translatedValue

        return node
