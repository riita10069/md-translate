import os
import shutil
import pytest
import subprocess

TEST_DIR = 'test_dir'
SAMPLE_DIR = 'sample_dir'
NESTED_DIR = 'nested_dir'
OUTPUT_DIR = 'output_dir'
CASE_DIR = 'case_dir'

@pytest.fixture
def e2e_test(scope='session'):
    # Remove test directory and files
    if os.path.isdir(TEST_DIR):
        shutil.rmtree(TEST_DIR)

    # Create test directory and files
    os.makedirs(TEST_DIR)
    os.makedirs(f'{TEST_DIR}/{SAMPLE_DIR}')
    os.makedirs(f'{TEST_DIR}/{OUTPUT_DIR}')
    os.makedirs(f'{TEST_DIR}/{CASE_DIR}')
    os.makedirs(f'{TEST_DIR}/{SAMPLE_DIR}/{NESTED_DIR}')

    with open(f'{TEST_DIR}/{SAMPLE_DIR}/sample1.md', 'w') as f:
        f.write('''---
chapter: true
title: sample1
weight: 1
---

Hello, world!
''')
    with open(f'{TEST_DIR}/{SAMPLE_DIR}/sample2.en.md', 'w') as f:
        f.write('''---
chapter: true
title: sample2
weight: 2
---

Hello, world!
''')
    with open(f'{TEST_DIR}/{SAMPLE_DIR}/sample3.ja.md', 'w') as f:
        f.write('''---
chapter: true
title: サンプル3
weight: 3
---

こんにちは、世界!
''')
    with open(f'{TEST_DIR}/{SAMPLE_DIR}/{NESTED_DIR}/sample4.md', 'w') as f:
        f.write('''---
chapter: true
title: sample4
weight: 4
---

Hello, world!
''')
    with open(f'{TEST_DIR}/{SAMPLE_DIR}/{NESTED_DIR}/sample5.ja.md', 'w') as f:
        f.write('''---
chapter: true
title: サンプル5
weight: 5
---

こんにちは、世界!
''')

    with open(f'{TEST_DIR}/{CASE_DIR}/filename with space.md', 'w') as f:
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
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR}/sample1.md', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample1.ja.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample1.ja.md')


def test_path_option_2(e2e_test):
    print('specify file path / from en (file path contains "en") to ja')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR}/sample2.en.md', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample2.ja.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample2.ja.md')


def test_path_option_3(e2e_test):
    print('specify file path / from ja to en')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR}/sample3.ja.md --from ja --to en', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample3.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample3.md')


def test_path_option_4(e2e_test):
    print('specify file path / from ja to zh')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR}/sample3.ja.md --from ja --to zh', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample3.zh.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample3.zh.md')


def test_path_option_5(e2e_test):
    print('specify file path with output directory / from en to ja')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR}/sample1.md --output {TEST_DIR}/{OUTPUT_DIR}', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{OUTPUT_DIR}/sample1.md')
    os.remove(f'{TEST_DIR}/{OUTPUT_DIR}/sample1.md')


def test_path_option_6(e2e_test):
    print('specify file path with output directory / from ja to en')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR}/sample3.ja.md --output {TEST_DIR}/{OUTPUT_DIR} --from ja --to en', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{OUTPUT_DIR}/sample3.md')
    os.remove(f'{TEST_DIR}/{OUTPUT_DIR}/sample3.md')


def test_path_option_7(e2e_test):
    print('specify directory path / from en to ja')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR}', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample1.ja.md')
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample2.ja.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample1.ja.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample2.ja.md')


def test_path_option_8(e2e_test):
    print('specify directory path / from ja to en')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR} --from ja --to en', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample3.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample3.md')


def test_path_option_9(e2e_test):
    print('specify directory path with -r option / from en to ja')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR} -r', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample1.ja.md')
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample2.ja.md')
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/{NESTED_DIR}/sample4.ja.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample1.ja.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample2.ja.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/{NESTED_DIR}/sample4.ja.md')


def test_path_option_10(e2e_test):
    print('specify directory path with -r option / from ja to en')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR} -r --from ja --to en', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample3.md')
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/{NESTED_DIR}/sample5.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample3.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/{NESTED_DIR}/sample5.md')


def test_path_option_11(e2e_test):
    print('specify directory path with output directory / from en to ja')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR} --output {TEST_DIR}/{OUTPUT_DIR}', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{OUTPUT_DIR}/sample1.md')
    assert os.path.exists(f'{TEST_DIR}/{OUTPUT_DIR}/sample2.en.md')
    os.remove(f'{TEST_DIR}/{OUTPUT_DIR}/sample1.md')
    os.remove(f'{TEST_DIR}/{OUTPUT_DIR}/sample2.en.md')


def test_path_option_12(e2e_test):
    print('specify file path contains space / from en to ja')
    subprocess.run(f'mdt --path "{TEST_DIR}/{CASE_DIR}/filename with space.md"', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{CASE_DIR}/filename with space.ja.md')
    os.remove(f'{TEST_DIR}/{CASE_DIR}/filename with space.ja.md')


def test_no_hugo_option(e2e_test):
    print('use --no-hugo options and translate normal markdown file')
    subprocess.run(f'mdt --path README.md --no-hugo', shell=True)
    assert os.path.exists(f'README.ja.md')
    os.remove(f'README.ja.md')


def test_deepl_option(e2e_test):
    print('use --deepl-free option')
    subprocess.run(f'mdt --path {TEST_DIR}/{SAMPLE_DIR}/sample1.md --deepl-free', shell=True)
    assert os.path.exists(f'{TEST_DIR}/{SAMPLE_DIR}/sample1.ja.md')
    os.remove(f'{TEST_DIR}/{SAMPLE_DIR}/sample1.ja.md')
