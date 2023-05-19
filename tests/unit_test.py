import os
import shutil
import pytest

from mdt import translate_page
from modules import const

TEST_PATH = 'test_dir'

@pytest.fixture
def unit_test(scope='module'):
    # Remove test directory and files
    if os.path.isdir(TEST_PATH):
        shutil.rmtree(TEST_PATH)

    # Create test directory and files
    os.makedirs(TEST_PATH)

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

    # Run tests
    yield


def test_html_tag_1(unit_test):
    print('only HTML in the paragraph')
    translate_page(f'{TEST_PATH}/sample1', const.LANG_EN, const.LANG_JA, False, False, True, f'./', True)
    with open(f'{TEST_PATH}/sample1.ja.md') as f:
        content = f.read()
        assert '<i class="far fa-thumbs-up" style="color:#008296"></i>' in content


def test_html_tag_2(unit_test):
    print('not only HTML in the paragraph')
    translate_page(f'{TEST_PATH}/sample2', const.LANG_EN, const.LANG_JA, False, False, True, f'./', False)
    with open(f'{TEST_PATH}/sample2.ja.md') as f:
        content = f.read()
        assert '<i class="far fa-thumbs-up" style="color:#008296"></i>' in content
