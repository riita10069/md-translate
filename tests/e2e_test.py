import os
import shutil
import pytest
import subprocess

TEST_PATH = 'test_dir'
SAMPLE_PATH = f'{TEST_PATH}/sample_dir'
NESTED_PATH = f'{SAMPLE_PATH}/nested_dir'
OUTPUT_PATH = f'{TEST_PATH}/output_dir'
CASE_PATH = f'{TEST_PATH}/case_dir'

@pytest.fixture
def e2e_test(scope='session'):
    # Remove test directory and files
    if os.path.isdir(TEST_PATH):
        shutil.rmtree(TEST_PATH)

    # Create test directory and files
    os.makedirs(TEST_PATH)
    os.makedirs(SAMPLE_PATH)
    os.makedirs(NESTED_PATH)
    os.makedirs(OUTPUT_PATH)
    os.makedirs(CASE_PATH)

    with open(f'{SAMPLE_PATH}/sample1.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: sample1
weight: 1
---

Hello, world!
''')
    with open(f'{SAMPLE_PATH}/sample2.en.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: sample2
weight: 2
---

Hello, world!
''')
    with open(f'{SAMPLE_PATH}/sample3.ja.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: サンプル3
weight: 3
---

こんにちは、世界!
''')
    with open(f'{NESTED_PATH}/sample4.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: sample4
weight: 4
---

Hello, world!
''')
    with open(f'{NESTED_PATH}/sample5.ja.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: サンプル5
weight: 5
---

こんにちは、世界!
''')

    with open(f'{CASE_PATH}/filename with space.md', 'w', encoding='utf-8') as f:
        f.write('''---
chapter: true
title: filename with space
weight: 6
---

Hello, world!
''')

    # Run tests
    yield


def test_path_option_1(e2e_test):
    print('specify file path / from en to ja')
    subprocess.run(f'mdt --path {SAMPLE_PATH}/sample1.md', shell=True)
    assert os.path.exists(f'{SAMPLE_PATH}/sample1.ja.md')
    os.remove(f'{SAMPLE_PATH}/sample1.ja.md')


def test_path_option_2(e2e_test):
    print('specify file path / from en (file path contains "en") to ja')
    subprocess.run(f'mdt --path {SAMPLE_PATH}/sample2.en.md', shell=True)
    assert os.path.exists(f'{SAMPLE_PATH}/sample2.ja.md')
    os.remove(f'{SAMPLE_PATH}/sample2.ja.md')


def test_path_option_3(e2e_test):
    print('specify file path / from ja to en')
    subprocess.run(f'mdt --path {SAMPLE_PATH}/sample3.ja.md --from ja --to en', shell=True)
    assert os.path.exists(f'{SAMPLE_PATH}/sample3.md')
    os.remove(f'{SAMPLE_PATH}/sample3.md')


def test_path_option_4(e2e_test):
    print('specify file path / from ja to zh')
    subprocess.run(f'mdt --path {SAMPLE_PATH}/sample3.ja.md --from ja --to zh', shell=True)
    assert os.path.exists(f'{SAMPLE_PATH}/sample3.zh.md')
    os.remove(f'{SAMPLE_PATH}/sample3.zh.md')


def test_path_option_5(e2e_test):
    print('specify file path with output directory / from en to ja')
    subprocess.run(f'mdt --path {SAMPLE_PATH}/sample1.md --output {OUTPUT_PATH}', shell=True)
    assert os.path.exists(f'{OUTPUT_PATH}/sample1.md')
    os.remove(f'{OUTPUT_PATH}/sample1.md')


def test_path_option_6(e2e_test):
    print('specify file path with output directory / from ja to en')
    subprocess.run(f'mdt --path {SAMPLE_PATH}/sample3.ja.md --output {OUTPUT_PATH} --from ja --to en', shell=True)
    assert os.path.exists(f'{OUTPUT_PATH}/sample3.md')
    os.remove(f'{OUTPUT_PATH}/sample3.md')


def test_path_option_7(e2e_test):
    print('specify directory path / from en to ja')
    subprocess.run(f'mdt --path {SAMPLE_PATH}', shell=True)
    assert os.path.exists(f'{SAMPLE_PATH}/sample1.ja.md')
    assert os.path.exists(f'{SAMPLE_PATH}/sample2.ja.md')
    os.remove(f'{SAMPLE_PATH}/sample1.ja.md')
    os.remove(f'{SAMPLE_PATH}/sample2.ja.md')


def test_path_option_8(e2e_test):
    print('specify directory path / from ja to en')
    subprocess.run(f'mdt --path {SAMPLE_PATH} --from ja --to en', shell=True)
    assert os.path.exists(f'{SAMPLE_PATH}/sample3.md')
    os.remove(f'{SAMPLE_PATH}/sample3.md')


def test_path_option_9(e2e_test):
    print('specify directory path with -r option / from en to ja')
    subprocess.run(f'mdt --path {SAMPLE_PATH} -r', shell=True)
    assert os.path.exists(f'{SAMPLE_PATH}/sample1.ja.md')
    assert os.path.exists(f'{SAMPLE_PATH}/sample2.ja.md')
    assert os.path.exists(f'{NESTED_PATH}/sample4.ja.md')
    os.remove(f'{SAMPLE_PATH}/sample1.ja.md')
    os.remove(f'{SAMPLE_PATH}/sample2.ja.md')
    os.remove(f'{NESTED_PATH}/sample4.ja.md')


def test_path_option_10(e2e_test):
    print('specify directory path with -r option / from ja to en')
    subprocess.run(f'mdt --path {SAMPLE_PATH} -r --from ja --to en', shell=True)
    assert os.path.exists(f'{SAMPLE_PATH}/sample3.md')
    assert os.path.exists(f'{NESTED_PATH}/sample5.md')
    os.remove(f'{SAMPLE_PATH}/sample3.md')
    os.remove(f'{NESTED_PATH}/sample5.md')


def test_path_option_11(e2e_test):
    print('specify directory path with output directory / from en to ja')
    subprocess.run(f'mdt --path {SAMPLE_PATH} --output {OUTPUT_PATH}', shell=True)
    assert os.path.exists(f'{OUTPUT_PATH}/sample1.md')
    assert os.path.exists(f'{OUTPUT_PATH}/sample2.en.md')
    os.remove(f'{OUTPUT_PATH}/sample1.md')
    os.remove(f'{OUTPUT_PATH}/sample2.en.md')


def test_path_option_12(e2e_test):
    print('specify file path contains space / from en to ja')
    subprocess.run(f'mdt --path "{CASE_PATH}/filename with space.md"', shell=True)
    assert os.path.exists(f'{CASE_PATH}/filename with space.ja.md')
    os.remove(f'{CASE_PATH}/filename with space.ja.md')


def test_no_hugo_option(e2e_test):
    print('use --no-hugo options and translate normal markdown file')
    subprocess.run(f'mdt --path README.md --no-hugo', shell=True)
    assert os.path.exists(f'README.ja.md')
    os.remove(f'README.ja.md')


def test_deepl_option(e2e_test):
    print('use --deepl-free option')
    subprocess.run(f'mdt --path {SAMPLE_PATH}/sample1.md --deepl-free', shell=True)
    assert os.path.exists(f'{SAMPLE_PATH}/sample1.ja.md')
    os.remove(f'{SAMPLE_PATH}/sample1.ja.md')
