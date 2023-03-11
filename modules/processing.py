import os
import json
import yaml

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

            if leaf[const.TYPE_TYPE] == const.TYPE_INLINE_CODE:
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

        elif leaf[const.TYPE_TYPE] == const.TYPE_TEXT:
            ret += leaf[const.VALUE_TYPE]
        else:
            if ret != "":
                after.append({
                    "type": const.TYPE_TEXT,
                    "value": ret,
                    "position": before[0][const.POSITION_TYPE]
                })
                ret = ""
                after.append(leaf)

    if ret != "":
        after.append({
            "type": const.TYPE_TEXT,
            "value": ret
        })
    return after, ret


def dfs(ast, lookup_table):
    root = ast[const.CHILDREN_TYPE]
    if isinstance(root, list):
        for node in root:
            if node[const.TYPE_TYPE] in [const.TYPE_STRONG, const.TYPE_EMPHASIS, const.TYPE_INLINE_CODE,
                                         const.TYPE_LINK]:
                new_node, _ = merge(root, lookup_table)
                ast[const.CHILDREN_TYPE] = new_node
                break
            if const.CHILDREN_TYPE in node:
                dfs(node, lookup_table)
    elif isinstance(root, dict):
        node = root
        if node[const.TYPE_TYPE] in [const.TYPE_STRONG, const.TYPE_EMPHASIS, const.TYPE_INLINE_CODE, const.TYPE_LINK]:
            new_node, _ = merge([root], lookup_table)
            ast[const.CHILDREN_TYPE] = new_node
        if const.CHILDREN_TYPE in node:
            dfs(node, lookup_table)


def mdProcessingBeforeTranslation(src_file, temp_file, src_lang, dest_lang):
    md_file = open(src_file, 'r+')
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
        header_yaml_data[const.HUGO_HEADER_TITLE] = translate.translate(header_yaml_data[const.HUGO_HEADER_TITLE],
                                                                        src_lang, dest_lang)
    if const.HUGO_HEADER_TAGS in header_yaml_data.keys() and isinstance(header_yaml_data[const.HUGO_HEADER_TAGS], list):
        new_tags = []
        for tag in header_yaml_data[const.HUGO_HEADER_TAGS]:
            new_tags.append(translate.translate(tag, src_lang, dest_lang))
        header_yaml_data[const.HUGO_HEADER_TAGS] = new_tags

    # create .temp.md file with only original .md content
    md_content_file = open(temp_file, 'x')
    md_content_file.write(md_content)
    md_content_file.flush()
    md_content_file.close()

    return header_yaml_data


def jsonProcessingBeforeTranslation():
    lookup_table = {"current_alphabet": '', "ids": []}
    json_open = open('output.json', 'r')
    ast = json.load(json_open)
    dfs(ast, lookup_table)

    return ast, lookup_table


def make_strong(content):
    return "**" + content + "**"


def make_emphasis(content):
    return "_" + content + "_"


def make_inlinecode(content):
    return "`" + content + "`"


def make_link(content, url, src_lang, dest_lang):
    return "[" + translate.translate(content, src_lang, dest_lang) + "]" + "(" + url + ")"


def mdProcessingAfterTranslation(dest_file_path, src_lang, dest_lang, translated_header_yaml_data, lookup_table):
    # add translated hugo header
    dest_md_file = open(dest_file_path, 'r')
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
                        attribute = make_link(leaf_data["leaf_value"], leaf_data["leaf_url"], src_lang, dest_lang)
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
    dest_file = open(dest_file_path, 'w+')
    contents = const.HUGO_HEADER_DELIMITER + yaml.dump(
        translated_header_yaml_data,
        allow_unicode=True) + const.HUGO_HEADER_DELIMITER + "\n" + processed_md_body
    dest_file.write(contents)
    dest_file.flush()
    dest_file.close()
