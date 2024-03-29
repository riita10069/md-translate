# Workshop Translator (Markdown Translation Tool)

A CLI tool for translating documents written in markdown.

By default this translator regard input file as **including hugo front matter**.

For markdown only translation, use `--no-hugo` option.

## Python version requirements

python 3.6 ~

## Prerequisites

```sh
brew install awscli
aws configure
npm install -g remark-cli
npm install remark-directive
```

> **Note**  
> Make sure to allow the `translate:TranslateText` action  
> And you have to specify an aws default region.

## Installation

```sh
pip3 install git+https://github.com/riita10069/md-translate.git
```

## Usage

```sh
mdt --path index.md
```

This command line tool minimum requires `--path` or `-r --path` options to designate a file or folder as the translation target.

Default translation source language settings and translation target language are English and Japanese. User can choose source language and the target language by using `--from` and `--to` options with translation language codes.

Also, by default, the translation is done by Amazon Translate, but it can be done by DeepL by using `--deepl` option. If you want to use DeepL, you need to set the API key of DeepL to the environment variable `DEEPL_API_KEY`. In addition,`--claude` option allows translation using Claude v2. However, this option is only available when `--from` is ja and `--to` is en.

User can use `--output` option to decide output folder (the folder need to exist).

For markdown file without hugo header add `--no-hugo` flag.
Is `--hugo` or neither `--hugo/--no-hugo` flag exist, then this tool regard inputs contain hugo header in .md file.

For more information see : `mdt --help`  
For command examples see [example](./docs/example.md)

### OPTIONS

```sh
Options:
  --path PATH                     Directory or file path where you want to
                                  translate  [required]
  -r, --recursive                 Translate recursively for subdirectories.
  --hugo / --no-hugo              Translate with hugo front matter, which is
                                  metadata about hugo site.  [default: hugo]
  --from [bg|cs|da|de|el|en|es|et|fi|fr|hu|id|it|ja|ko|lt|lv|nb|nl|pl|pt|ro|ru|sk|sl|sv|tr|uk|zh]
                                  Source language  [default: en]
  --to [bg|cs|da|de|el|en|es|et|fi|fr|hu|id|it|ja|ko|lt|lv|nb|nl|pl|pt|ro|ru|sk|sl|sv|tr|uk|zh]
                                  Target language  [default: ja]
  --claude                        Translate with Claude v2. Only available
                                  with options where the from parameter is ja
                                  and the to parameter is en.
  --deepl-free                    Translate with DeepL API Free. Environment variable "DEEPL_API_KEY" must be set.
  --deepl-pro                     Translate with DeepL API Pro. Environment variable "DEEPL_API_KEY" must be set.
  --output PATH                   Directory where you want to output the
                                  translated contents  [default: ./]
  --debug                         Output some ast files for debug.
  --help                          Show this message and exit.
  --dictionary-path               Dictionaries files directory
  --concurrency                   Number of concurrent threads to use for translation by Claude.
```

### How to use dictionaries

#### base_ignore_words.json

If you register words that you do not want to translate (e.g. AWS service names), they will be output as English words without translation.
Nouns and whole sentences must be registered to be output properly as sentences.

#### base_custom_words.json

If you register a specific word pair (e.g., "Region": "region") that you want to be translated, it will be replaced and output as such.
Nouns and whole sentences must be registered to be output properly as sentences.

## Acknowledgments

Many thanks to you for your tremendous contribution.
