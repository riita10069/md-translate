import os
import json
import yaml
import re

from modules import const
from modules import translate


def next_alphabet(current):
    """
    Return the next alphabet after the current alphabet.

    Args:
    current (str): The current alphabet.

    Returns:
    str: The next alphabet after the current alphabet.
    """
    if current == "":
        return "a"
    last_char = current[-1]
    if last_char != "z":
        return current[:-1] + chr(ord(last_char) + 1)
    else:
        return next_alphabet(current[:-1]) + "a"


def does_dict_has_key(dicts, key):
    """
    Args:
        dicts (list[dict]): 辞書型の配列
        key (str): 確認するキー

    Returns:
        bool: 全ての要素について指定されたキーの値が存在する場合はTrue、そうでない場合はFalseを返す。
    """
    for d in dicts:
        if key not in d:
            return False
    return True


def merge(before, lookup_table):
    ret = ""

    after = []
    for leaf in before:
        if leaf[const.TYPE_TYPE] in [const.TYPE_STRONG, const.TYPE_EMPHASIS, const.TYPE_INLINE_CODE, const.TYPE_LINK]:

            id = "http://no-translate-" + next_alphabet(lookup_table['current_alphabet']) + ".dev"
            lookup_table['current_alphabet'] = next_alphabet(lookup_table['current_alphabet'])
            lookup_table["ids"].append(id)

            if leaf[const.TYPE_TYPE] in [const.TYPE_INLINE_CODE]:
                lookup_table[id] = {
                    "leaf_types": [leaf[const.TYPE_TYPE]],
                    "leaf_value": leaf[const.VALUE_TYPE]
                }

            # 中にある in-line 要素を考慮
            elif leaf[const.TYPE_TYPE] == const.TYPE_LINK:
                after_in_url, merged_children_id = merge(leaf[const.CHILDREN_TYPE], lookup_table)
                lookup_table[id] = {
                    "leaf_types": [leaf[const.TYPE_TYPE]],
                    "leaf_url": leaf[const.URL_TYPE],  # https:// ~
                    "leaf_value": merged_children_id or after_in_url[0][const.VALUE_TYPE]  # URLの中身
                }

            # ネストを考慮 # strong # emphasis
            elif leaf[const.TYPE_TYPE] in [const.TYPE_STRONG, const.TYPE_EMPHASIS]:
                leaf_types = [leaf[const.TYPE_TYPE]]
                if not does_dict_has_key(leaf[const.CHILDREN_TYPE], const.VALUE_TYPE):
                    merged_leaf, merged_children_id = merge(leaf[const.CHILDREN_TYPE], lookup_table)
                    lookup_table[id] = {
                        "leaf_types": [leaf[const.TYPE_TYPE]],
                        "leaf_value": merged_children_id or merged_leaf[0][const.VALUE_TYPE]
                    }
                else:
                    lookup_table[id] = {
                        "leaf_types": leaf_types,
                        "leaf_value": leaf[const.CHILDREN_TYPE][0][const.VALUE_TYPE]
                    }

            ret += id

        elif leaf[const.TYPE_TYPE] in [const.TYPE_TEXT, const.TYPE_HTML]:
            ret += leaf[const.VALUE_TYPE]
        else:
            if ret != "":
                after.append({
                    "type": const.TYPE_TEXT,
                    "value": ret
                })
                ret = ""
            after.append(leaf)

    if ret != "":
        after.append({
            "type": const.TYPE_TEXT,
            "value": ret
        })
    return after, ret


def distinguish_html_tag(input_string):
    if input_string.startswith("<!--") and input_string.endswith("-->"):
        return const.HTML_TAG_TYPE_COMMENT
    elif input_string.startswith("<") and input_string.endswith("/>"):
        return const.HTML_TAG_TYPE_SELF_CLOSING_TAG
    elif input_string.startswith("</") and input_string.endswith(">"):
        return const.HTML_TAG_TYPE_CLOSING_TAG
    elif input_string.startswith("<") and input_string.endswith(">"):
        return const.HTML_TAG_TYPE_BEGINNING_TAG
    else:
        print("以下の想定外のHTMLタグが含まれています。管理者へ連絡してください。")
        print(input_string)
        return ""


def html_merge(before, lookup_table):
    beginning_tags = []
    is_in_html = False

    html_text = ""
    after = []

    for node in before:
        if is_in_html:
            if node[const.TYPE_TYPE] in [const.TYPE_STRONG]:
                for strong_children in node[const.CHILDREN_TYPE]:
                    if strong_children[const.TYPE_TYPE] in [const.TYPE_TEXT]:
                        html_text += make_strong(strong_children[const.VALUE_TYPE])
            if node[const.TYPE_TYPE] in [const.TYPE_EMPHASIS]:
                for emphasis_children in node[const.CHILDREN_TYPE]:
                    if emphasis_children[const.TYPE_TYPE] in [const.TYPE_TEXT]:
                        html_text += make_emphasis(emphasis_children[const.VALUE_TYPE])
            if node[const.TYPE_TYPE] in [const.TYPE_TEXT]:
                html_text += node[const.VALUE_TYPE]
            if node[const.TYPE_TYPE] in [const.TYPE_INLINE_CODE]:
                html_text += make_inlinecode(node[const.VALUE_TYPE])

        if node[const.TYPE_TYPE] == const.TYPE_HTML:
            tag_type = distinguish_html_tag(node[const.VALUE_TYPE])
            if tag_type == const.HTML_TAG_TYPE_BEGINNING_TAG:
                beginning_tags.append(node)
                is_in_html = True
                html_text += node[const.VALUE_TYPE]
            elif tag_type == const.HTML_TAG_TYPE_CLOSING_TAG:
                html_text += node[const.VALUE_TYPE]
                beginning_tags.pop()
                if len(beginning_tags) == 0:
                    id = "http://no-translate-" + next_alphabet(lookup_table['current_alphabet']) + ".dev"
                    lookup_table['current_alphabet'] = next_alphabet(lookup_table['current_alphabet'])
                    lookup_table["ids"].append(id)

                    lookup_table[id] = {
                        "leaf_types": [const.TYPE_HTML],
                        "leaf_value": html_text
                    }

                    is_in_html = False
                    after.append({
                        "type": const.TYPE_HTML,
                        "value": id
                    })
                    html_text = ""
            elif tag_type in [const.HTML_TAG_TYPE_SELF_CLOSING_TAG, const.HTML_TAG_TYPE_COMMENT] and not is_in_html:
                id = "http://no-translate-" + next_alphabet(lookup_table['current_alphabet']) + ".dev"
                lookup_table['current_alphabet'] = next_alphabet(lookup_table['current_alphabet'])
                lookup_table["ids"].append(id)

                lookup_table[id] = {
                    "leaf_types": [const.TYPE_HTML],
                    "leaf_value": node[const.VALUE_TYPE]
                }

                after.append({
                    "type": const.TYPE_HTML,
                    "value": id
                })

        elif not is_in_html:
            after.append(node)

    # <i class=\"far fa-eye\" style=\"color:#262262\"></i>, etc. may be mapped to a single Node as a whole.
    # The specification changes depending on whether it belongs to Paragraph or not. In that
    # case, this part is important because it is solved by stepping here.
    if html_text != "":
        after.append({
            "type": const.TYPE_HTML,
            "value": html_text
        })
    return after, html_text


def html_dfs(ast, lookup_table):
    root = ast[const.CHILDREN_TYPE]

    if isinstance(root, list):
        for node in root:
            if const.CHILDREN_TYPE in node:
                html_dfs(node, lookup_table)
            if node[const.TYPE_TYPE] == const.TYPE_HTML:
                new_node, _ = html_merge(root, lookup_table)
                ast[const.CHILDREN_TYPE] = new_node
    elif isinstance(root, dict):
        node = root
        if const.CHILDREN_TYPE in node:
            html_dfs(node, lookup_table)
        if node[const.TYPE_TYPE] == const.TYPE_HTML:
            new_node, _ = html_merge(root, lookup_table)
            ast[const.CHILDREN_TYPE] = new_node


def dfs(ast, lookup_table):
    root = ast[const.CHILDREN_TYPE]
    if isinstance(root, list):
        for node in root:
            if node[const.TYPE_TYPE] in [const.TYPE_STRONG, const.TYPE_EMPHASIS, const.TYPE_INLINE_CODE,
                                         const.TYPE_LINK, const.TYPE_HTML]:
                if node[const.TYPE_TYPE] != const.TYPE_HTML or ast[const.TYPE_TYPE] == const.TYPE_PARAGRAPH:
                    new_node, _ = merge(root, lookup_table)
                    ast[const.CHILDREN_TYPE] = new_node
                    break
            if const.CHILDREN_TYPE in node:
                dfs(node, lookup_table)
    elif isinstance(root, dict):
        node = root
        if node[const.TYPE_TYPE] in [const.TYPE_STRONG, const.TYPE_EMPHASIS, const.TYPE_INLINE_CODE, const.TYPE_LINK,
                                     const.TYPE_HTML]:
            if node[const.TYPE_TYPE] != const.TYPE_HTML or ast[const.TYPE_TYPE] == const.TYPE_PARAGRAPH:
                new_node, _ = merge([root], lookup_table)
                ast[const.CHILDREN_TYPE] = new_node
        if const.CHILDREN_TYPE in node:
            dfs(node, lookup_table)


def mdProcessingBeforeTranslation(src_file, temp_file, translator):
    md_file = open(src_file, 'r+', encoding='utf-8')
    md_file_lines = md_file.readlines()
    md_file.close()

    hugo_header = ""
    md_content = ""
    hugo_header_delimiter_count = 0

    # separate hugo header and markdown content
    for line in md_file_lines:
        if line == const.HUGO_HEADER_DELIMITER:
            hugo_header_delimiter_count += 1
        elif hugo_header_delimiter_count == 1:
            hugo_header += line
        else:
            md_content += line

    header_yaml_data = yaml.safe_load(hugo_header)

    # translate hugo header
    if const.HUGO_HEADER_TITLE in header_yaml_data.keys():
        header_yaml_data[const.HUGO_HEADER_TITLE] = translator.translate(header_yaml_data[const.HUGO_HEADER_TITLE])
    if const.HUGO_HEADER_TAGS in header_yaml_data.keys() and isinstance(header_yaml_data[const.HUGO_HEADER_TAGS], list):
        new_tags = []
        for tag in header_yaml_data[const.HUGO_HEADER_TAGS]:
            new_tags.append(translator.translate(tag))
        header_yaml_data[const.HUGO_HEADER_TAGS] = new_tags

    # create .temp.md file with only original .md content
    md_content_file = open(temp_file, 'x', encoding='utf-8')
    md_content_file.write(md_content)
    md_content_file.flush()
    md_content_file.close()

    return header_yaml_data


def jsonProcessingBeforeTranslation(lookup_table):
    json_open = open('output.json', 'r', encoding='utf-8')
    ast = json.load(json_open)
    html_dfs(ast, lookup_table)
    dfs(ast, lookup_table)

    return ast


def make_strong(content):
    return "**" + content + "**"


def make_emphasis(content):
    return "_" + content + "_"


def make_inlinecode(content):
    return "`" + content + "`"


def make_link(content, url, translator):
    return "[" + translator.translate(content) + "]" + "(" + url + ")"


def mdProcessingAfterTranslation(dest_file_path,
                                 translated_header_yaml_data, lookup_table, translator):
    # add translated hugo header
    dest_md_file = open(dest_file_path, 'r', encoding='utf-8')
    translated_md_content_lines = dest_md_file.readlines()

    dest_md_file.close()

    # post process translated md body here [hard replacement, **.-> ** (space)]
    processed_md_body = ""

    for line in translated_md_content_lines:
        processed_line = line
        # 置き換えた strong などの文字列を、lookup_tableを使って戻します。
        for id in lookup_table["ids"]:
            if id in processed_line:
                attribute = ""
                leaf_data = lookup_table[id]
                reversed_leaf_data = leaf_data["leaf_types"][::-1]
                for leaf_type in reversed_leaf_data:
                    if leaf_type == const.TYPE_STRONG:
                        attribute = make_strong(leaf_data["leaf_value"])
                    elif leaf_type == const.TYPE_INLINE_CODE:
                        attribute = make_inlinecode(leaf_data["leaf_value"])
                    elif leaf_type == const.TYPE_EMPHASIS:
                        attribute = make_emphasis(leaf_data["leaf_value"])
                    elif leaf_type == const.TYPE_LINK:
                        attribute = make_link(leaf_data["leaf_value"], leaf_data["leaf_url"], translator)
                    elif leaf_type == const.TYPE_HTML:
                        attribute = leaf_data["leaf_value"]
                    elif leaf_type == const.TYPE_TEXT:
                        attribute = leaf_data["leaf_value"]
                    processed_line = processed_line.replace(id, attribute)

        if "&#x20;" in line:
            processed_line = processed_line.replace("&#x20;", "")
        if "***" in line:
            processed_line = processed_line.replace("***", "---")
        if "\\[" in line:
            processed_line = processed_line.replace("\\[", "[")
        if "\\_" in line:
            processed_line = processed_line.replace("\\_", "_")
        if '\\ n' in line:
            processed_line = processed_line.replace('\\ n', '\\n')
        if '\\(' in line:
            processed_line = processed_line.replace('\\(', '(')

        processed_md_body += processed_line

    # merge translated hugo header and processed_md_body
    dest_file = open(dest_file_path, 'w+', encoding='utf-8')

    contents = ""
    if translated_header_yaml_data == "":
        contents = processed_md_body
    else:
        contents = const.HUGO_HEADER_DELIMITER + yaml.dump(
            translated_header_yaml_data,
            allow_unicode=True) + const.HUGO_HEADER_DELIMITER + "\n" + processed_md_body
    dest_file.write(contents)
    dest_file.flush()
    dest_file.close()

    if translator.dictionary_path != "":
        translation_history_processing_after_translation(translator, lookup_table)


def translation_history_processing_after_translation(translator, lookup_table):
    for k, processed_line in translator.translate_history.items():
        # 置き換えた strong などの文字列を、lookup_tableを使って戻します。
        for id in lookup_table["ids"]:
            if id in processed_line:
                attribute = ""
                leaf_data = lookup_table[id]
                reversed_leaf_data = leaf_data["leaf_types"][::-1]
                for leaf_type in reversed_leaf_data:
                    if leaf_type == const.TYPE_STRONG:
                        attribute = make_strong(leaf_data["leaf_value"])
                    elif leaf_type == const.TYPE_INLINE_CODE:
                        attribute = make_inlinecode(leaf_data["leaf_value"])
                    elif leaf_type == const.TYPE_EMPHASIS:
                        attribute = make_emphasis(leaf_data["leaf_value"])
                    elif leaf_type == const.TYPE_LINK:
                        attribute = make_link(leaf_data["leaf_value"], leaf_data["leaf_url"], translator)
                    elif leaf_type == const.TYPE_HTML:
                        attribute = leaf_data["leaf_value"]
                    elif leaf_type == const.TYPE_TEXT:
                        attribute = leaf_data["leaf_value"]
                    processed_line = processed_line.replace(id, attribute)

        if "&#x20;" in processed_line:
            processed_line = processed_line.replace("&#x20;", "")
        if "***" in processed_line:
            processed_line = processed_line.replace("***", "---")
        if "\\[" in processed_line:
            processed_line = processed_line.replace("\\[", "[")
        if "\\_" in processed_line:
            processed_line = processed_line.replace("\\_", "_")
        if '\\ n' in processed_line:
            processed_line = processed_line.replace('\\ n', '\\n')
        if '\\(' in processed_line:
            processed_line = processed_line.replace('\\(', '(')

        translator.translate_history[k] = processed_line

def is_text_match(text1, text2):
    # ピリオド、行末の改行文字、前後の半角スペースを除去して、小文字に変換
    processed_text1 = re.sub(r'[.\n\s]', '', text1.lower())
    processed_text2 = re.sub(r'[.\n\s]', '', text2.lower())

    # 文章が一致しているか判断
    return processed_text1 == processed_text2
