import os
import subprocess
import json
import shutil
import click
import re
from datetime import datetime

from pathlib import Path
from modules import const
from modules import processing
from modules import remark
from modules import translate


def get_dest_file_path(filename, from_, to, output):
    dest_file_path = ''
    output_directory = Path.resolve(Path(output))
    current_directory = Path.cwd()

    if output_directory == current_directory:
        dest_file_path = Path.resolve(Path(filename + '.md' if to == const.LANG_EN else filename + '.' + to + '.md'))
        dest_file_path = str(dest_file_path)
    else:
        md_file_name = Path(filename).name
        dest_file_path = os.path.join(output_directory, md_file_name + '.md' if to == const.LANG_EN else md_file_name + '.md')
        dest_file_path = re.sub(r"^./|/(\./)+", "/", dest_file_path)

    if dest_file_path.endswith('.' + const.LANG_EN + '.' + to + '.md'):
        return dest_file_path.replace('.' + const.LANG_EN, '')

    return str(dest_file_path)


def translate_page(filename, from_, to, deepl_free, deepl_pro, is_hugo, output, debug, dictionary_path, custom_dictionary_path):
    src_file_path = filename + '.md' if from_ == const.LANG_EN else filename + '.' + from_ + '.md'

    temp_file_path = filename + '.temp.md'
    dest_file_path = get_dest_file_path(filename, from_, to, output)

    lookup_table = {"current_alphabet": '', "ids": []}
    # 辞書の読み込み
    translator = translate.Translator(dictionary_path, from_, to, deepl_free, deepl_pro, lookup_table, custom_dictionary_path)

    # md 前処理 (hugo header の分離と翻訳)
    translated_header_yaml_data = ""
    if is_hugo:
        try:
            translated_header_yaml_data = processing.mdProcessingBeforeTranslation(
                src_file_path, temp_file_path, translator)
            # markdown to json
            remark.mdToJson(temp_file_path)
        finally:
            # delete temporary md file
            subprocess.run(f'rm "{temp_file_path}"', shell=True)
    else:
        translated_header_yaml_data = ""
        # markdown to json
        remark.mdToJson(src_file_path)

    # 検証用 json 1
    if debug:
        shutil.copyfile("output.json", "ast-from-md.json")

    # json 前処理 (語順対応のための置き換え)
    ast = processing.jsonProcessingBeforeTranslation(lookup_table)

    # 検証用 json 2
    if debug:
        with open('ast-before-translation.json', mode='wt', encoding='utf-8') as file:
            json.dump(ast, file, ensure_ascii=False, indent=2)

    # translate AST
    translated_ast = translator.translateAst(ast)

    # recreate output.json
    with open('output.json', mode='wt', encoding='utf-8') as file:
        json.dump(translated_ast, file, ensure_ascii=False, indent=2)

    # 検証用 json 3
    if debug:
        shutil.copyfile("output.json", "ast-after-translation.json")

    # translated JSON AST to md
    remark.jsonToMd(dest_file_path)

    # md 後処理 (hugo header と 翻訳済み md file のマージ)
    processing.mdProcessingAfterTranslation(
        dest_file_path, translated_header_yaml_data, lookup_table, translator)

    os.remove("output.json")

    translator.save_dictionaries()


def get_latest_translation_history_file(folder_path):
    file_prefix = 'translation_history_'
    file_suffix = '.json'

    file_names = os.listdir(folder_path)
    file_names = [f for f in file_names if f.startswith(file_prefix) and f.endswith(file_suffix)]

    if not file_names:
        return None

    latest_timestamp = max([datetime.strptime(f[len(file_prefix):-len(file_suffix)], '%Y-%m-%d_%H:%M:%S') for f in file_names])
    latest_file_name = file_prefix + latest_timestamp.strftime("%Y-%m-%d_%H:%M:%S") + file_suffix

    return latest_file_name


def mutate_path(ctx, param, value):
    return "./" + value

@click.command()
@click.option('--path', help='Directory or file path where you want to translate', required=True,
              callback=mutate_path, type=click.Path(exists=True))
@click.option('-r', '--recursive', is_flag=True, help='Translate recursively for subdirectories.', show_default=True)
@click.option('--hugo/--no-hugo',  default=True, help='Translate with hugo front matter, which is metadata about hugo site.', show_default=True)
@click.option('--from', 'from_', help='Source language', default=const.LANG_EN, show_default=True, type=click.Choice(const.LANGUAGE_LIST))
@click.option('--to', help='Target language', default=const.LANG_JA, show_default=True,
              type=click.Choice(const.LANGUAGE_LIST))
@click.option('--deepl-free', is_flag=True, default=False, help='Translate with DeepL API Free. Environment variable "DEEPL_API_KEY" must be set.', show_default=True)
@click.option('--deepl-pro', is_flag=True, default=False, help='Translate with DeepL API Pro. Environment variable "DEEPL_API_KEY" must be set.', show_default=True)
@click.option('--output', help='Directory where you want to output the translated contents', default="./",
              show_default=True, type=click.Path(exists=True))
@click.option('--debug', is_flag=True, help='Output some ast files for debug.', show_default=True)
@click.option('--dictionary-path', default="", help='Dictionaries files directory', show_default=True)
@click.option('--custom-dictionary-path', default="", help='Custom Dictionary Path', show_default=True)
def run(path, recursive, hugo, from_, to, deepl_free, deepl_pro, output, debug, dictionary_path, custom_dictionary_path):
    is_hugo = hugo
    if custom_dictionary_path == "" and dictionary_path != "":
        custom_dictionary_path = os.path.join(dictionary_path, get_latest_translation_history_file(dictionary_path))

    if path.endswith(".md"):
        if path.endswith("." + from_ + ".md") or (from_ == const.LANG_EN and "." not in path.split("/")[-1].rstrip(".md")):
            translate_page(re.sub('\.md$', '', path) if from_ == const.LANG_EN else re.sub('\.' + from_ + '.md', '', path), from_, to, deepl_free, deepl_pro, is_hugo, output, debug, dictionary_path, custom_dictionary_path)

    else:
        if recursive:
            for current_dir, dirs, files in os.walk(path):
                for filename in files:
                    if (filename.endswith("." + from_ + ".md") or (
                            from_ == const.LANG_EN and "." not in filename.rstrip(".md"))):
                        click.echo("translate " + os.path.join(current_dir, re.sub('\.md$', '', filename)))
                        translate_page(
                            re.sub('\.md$', '', os.path.join(current_dir, filename)) if from_ == const.LANG_EN else re.sub('\.' + from_ + '.md', '',  os.path.join(current_dir, filename)), from_, to, deepl_free, deepl_pro, is_hugo, output, debug, dictionary_path, custom_dictionary_path)

        else:
            for filename in os.listdir(path):
                if os.path.isfile(os.path.join(path, filename)):
                    if (filename.endswith("." + from_ + ".md") or (
                            from_ == const.LANG_EN and "." not in filename.split("/")[-1].rstrip(".md"))):
                        click.echo("translate " + os.path.join(path, re.sub('\.md$', '', filename)))
                        translate_page(
                            re.sub('\.md$', '', os.path.join(path, filename)) if from_ == const.LANG_EN else re.sub('\.' + from_ + '.md', '',  os.path.join(path, filename)), from_, to, deepl_free, deepl_pro, is_hugo, output, debug, dictionary_path, custom_dictionary_path)
if __name__ == '__main__':
    run()
