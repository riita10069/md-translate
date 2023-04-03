import os
import subprocess
import json
import shutil
import click
import re

from pathlib import Path
from modules import const
from modules import processing
from modules import remark
from modules import translate


def get_dest_file_path(filename, src_lang, dest_lang, output):
    dest_file_path = ''
    output_directory = Path.resolve(Path(output))
    current_directory = Path.cwd()

    if output_directory == current_directory:
        dest_file_path = Path.resolve(Path(filename + '.md' if dest_lang == const.LANG_EN else filename + '.' + dest_lang + '.md'))
        dest_file_path = str(dest_file_path)
    else:
        md_file_name = Path(filename).name
        dest_file_path = os.path.join(output_directory, md_file_name + '.md' if src_lang == const.LANG_EN else md_file_name + '.' + src_lang + '.md')
        dest_file_path = re.sub(r"^./|/(\./)+", "/", dest_file_path)
    if dest_file_path.endswith('.' + const.LANG_EN + '.' + dest_lang + '.md'):
        return dest_file_path.replace('.' + const.LANG_EN, '')
    return str(dest_file_path)


def translate_page(filename, src_lang, dest_lang, output, debug):
    src_file_path = filename + '.md' if src_lang == const.LANG_EN else filename + '.' + src_lang + '.md'
    temp_file_path = filename + '.temp.md'
    dest_file_path = get_dest_file_path(filename, src_lang, dest_lang, output)

    # md 前処理 (hugo header の分離と翻訳)
    translated_header_yaml_data = processing.mdProcessingBeforeTranslation(
        src_file_path, temp_file_path, src_lang, dest_lang)

    # markdown to json
    remark.mdToJson(temp_file_path)

    # 検証用 json 1
    if debug:
        shutil.copyfile("output.json", "ast-from-md.json")

    # delete temporary md file
    subprocess.run('rm ' + temp_file_path, shell=True)

    # json 前処理 (語順対応のための置き換え)
    ast, lookup_table = processing.jsonProcessingBeforeTranslation()

    # 検証用 json 2
    if debug:
        with open('ast-before-translation.json', mode='wt', encoding='utf-8') as file:
            json.dump(ast, file, ensure_ascii=False, indent=2)

    # translate AST
    translated_ast = translate.translateAst(ast, src_lang, dest_lang)

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
        dest_file_path, src_lang, dest_lang, translated_header_yaml_data, lookup_table)

    os.remove("output.json")


def mutate_path(ctx, param, value):
    return "./" + value


@click.command()
@click.option('--path', help='directory or file path where you want to translate', required=True,
              callback=mutate_path, type=click.Path(exists=True))
@click.option('-r', '--recursive', is_flag=True, help='translate recursively for subdirectories', show_default=True)
@click.option('--src-lang', help='source language', default=const.LANG_EN, show_default=True,
              type=click.Choice(const.LANGUAGE_LIST))
@click.option('--dest-lang', help='post-translation language', default=const.LANG_JA, show_default=True,
              type=click.Choice(const.LANGUAGE_LIST))
@click.option('--output', help='directory where you want to output the translated contents', default="./",
              show_default=True, type=click.Path(exists=True))
@click.option('--debug', is_flag=True, help='output some ast files for debug', show_default=True)
def run(path, recursive, src_lang, dest_lang, output, debug):
    if path.endswith(".md"):
        if (path.endswith("." + src_lang + ".md") or (
                    src_lang == const.LANG_EN and "." not in path.split("/")[-1].rstrip(".md"))):
            translate_page(
                re.sub('\.md$', '', path) if src_lang == const.LANG_EN else re.sub('.' + src_lang + '.md', '', path),
                src_lang, dest_lang, output, debug)
    else:
        if recursive:
            for current_dir, dirs, files in os.walk(path):
                for filename in files:
                    if (filename.endswith("." + src_lang + ".md") or (
                            src_lang == const.LANG_EN and "." not in filename.rstrip(".md"))):
                        click.echo("translate " + os.path.join(current_dir, re.sub('\.md$', '', filename)))
                        translate_page(
                            re.sub('\.md$', '', os.path.join(current_dir, filename)) if src_lang == const.LANG_EN else re.sub('\.md$', '',  os.path.join(current_dir, filename)), src_lang, dest_lang, output, debug)

        else:
            for filename in os.listdir(path):
                if os.path.isfile(os.path.join(path, filename)):
                    if (filename.endswith("." + src_lang + ".md") or (
                            src_lang == const.LANG_EN and "." not in filename.split("/")[-1].rstrip(".md"))):
                        click.echo("translate " + os.path.join(path, re.sub('\.md$', '', filename)))
                        translate_page(
                            re.sub('\.md$', '', os.path.join(current_dir, filename)) if src_lang == const.LANG_EN else re.sub('\.md$', '',  os.path.join(current_dir, filename)), src_lang, dest_lang, output, debug)

if __name__ == '__main__':
    run()
