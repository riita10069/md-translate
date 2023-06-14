import os
import shutil
import pytest

from mdt import translate_page
from modules import const

TEST_PATH = 'test_dir'
DICTIONARY_PATH = 'dictionary'


@pytest.fixture
def unit_test(scope='module'):
    # Remove test directory and files
    if os.path.isdir(TEST_PATH):
        shutil.rmtree(TEST_PATH)

    if os.path.isdir(DICTIONARY_PATH):
        shutil.rmtree(DICTIONARY_PATH)
    # Create test directory and files
    os.makedirs(TEST_PATH)
    os.makedirs(DICTIONARY_PATH)

    with open(f'{TEST_PATH}/sample1.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: sample1
weight: 1
---

<i class="far fa-thumbs-up" style="color:#008296"></i>
''')

    with open(f'{TEST_PATH}/sample2.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: sample2
weight: 2
---

<i class="far fa-thumbs-up" style="color:#008296"></i> **Congratulations!** You have successfully completed the course.
''')

    with open(f'{TEST_PATH}/nested_html.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: nested html tag
weight: 6
---

<span style="ssb_s3_white"><b>Edit/Preview data</b></span>
''')

    with open(f'{TEST_PATH}/nested_html_with_text.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: nested html tag
weight: 6
---

<div><i class="far fa-eye" style="color:#262262"></i> Navigate <a href="#lab_5_challenge_a" target="_self">**here**</a> for **a** solution.</div>
''')

    with open(f'{TEST_PATH}/base_ignore_words.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: base ignore words
weight: 7
---

Invent and Simplify
Leaders expect and require innovation and invention from their teams and always find ways to simplify. They are externally aware, look for new ideas from everywhere, and are not limited by “not invented here.” As we do new things, we accept that we may be misunderstood for long periods of time.
''')

    with open(f'{TEST_PATH}/base_custom_words.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: base custom words
weight: 8
---

There's a party today called Beer Bust.
''')

    with open(f'{DICTIONARY_PATH}/base_ignore_words.json', 'w', encoding='utf-8') as f:
        f.write('''---
[
  "They are externally aware",
  "Invent and Simplify"
]
''')

    with open(f'{DICTIONARY_PATH}/base_custom_words.json', 'w', encoding='utf-8') as f:
        f.write('''---
{
    "There's a party today called Beer Bust": "リーダーは強い判断力と優れた直感力を持ってしてよく食べます。"
}
''')

    # Run tests
    yield


def test_html_tag_1(unit_test):
    print('only HTML in the paragraph')
    translate_page(f'{TEST_PATH}/sample1', const.LANG_EN, const.LANG_JA, False, False, True, f'./', True, "")
    with open(f'{TEST_PATH}/sample1.ja.md') as f:
        content = f.read()
        assert '<i class="far fa-thumbs-up" style="color:#008296"></i>' in content


def test_html_tag_2(unit_test):
    print('not only HTML in the paragraph')
    translate_page(f'{TEST_PATH}/sample2', const.LANG_EN, const.LANG_JA, False, False, True, f'./', False, "")
    with open(f'{TEST_PATH}/sample2.ja.md') as f:
        content = f.read()
        assert '<i class="far fa-thumbs-up" style="color:#008296"></i>' in content


def test_html_tag_3(unit_test):
    print('testing nested HTML')
    translate_page(f'{TEST_PATH}/nested_html', const.LANG_EN, const.LANG_JA, False, False, True, f'./', False, "")
    with open(f'{TEST_PATH}/nested_html.ja.md') as f:
        content = f.read()
        assert '<span style="ssb_s3_white"><b>Edit/Preview data</b></span>' in content


def test_html_tag_4(unit_test):
    print('testing nested HTML with text and strong')
    translate_page(f'{TEST_PATH}/nested_html_with_text', const.LANG_EN, const.LANG_JA, False, False, True, f'./', False,
                   "")
    with open(f'{TEST_PATH}/nested_html_with_text.ja.md') as f:
        content = f.read()
        assert '<div><i class="far fa-eye" style="color:#262262"></i> Navigate <a href="#lab_5_challenge_a" ' \
               'target="_self">**here**</a> for **a** solution.</div>' in content


def test_dictionary_1(unit_test):
    print("test base_ignore_words")
    translate_page(f'{TEST_PATH}/base_ignore_words', const.LANG_EN, const.LANG_JA, False, False, True, f'./', False,
                   DICTIONARY_PATH)
    with open(f'{TEST_PATH}/base_ignore_words.ja.md') as f:
        content = f.read()
        assert "They are externally aware" in content
        assert "Invent and Simplify" in content


def test_dictionary_1(unit_test):
    print("test base_ignore_words")
    translate_page(f'{TEST_PATH}/base_custom_words', const.LANG_EN, const.LANG_JA, False, False, True, f'./', False,
                   DICTIONARY_PATH)
    with open(f'{TEST_PATH}/base_custom_words.ja.md') as f:
        content = f.read()
        assert "リーダーは強い判断力と優れた直感力を持ってしてよく食べます。" in content
