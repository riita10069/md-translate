# Workshop Translator (Markdown Translation Tool)

A CLI tool for translating documents written in markdown.

By default this translator regard input file as **including hugo front matter**.

For markdown only translation, use `--no-hugo` option.

## Python version requirements

python 3.6 ~

## Prerequirements

```
$ brew install awscli
$ aws configure
$ npm install -g remark-cli
$ npm install -g remark-directive
```

> **Note**  
> Make sure to allow the `translate:TranslateText` action  
> And you have to specify an aws default region.

## Instalation

```
$ pip3 install git+https://github.com/riita10069/md-translate.git
```

## Usage

```
$ mdt --path index.md
```

This command line tool minumum requires `--path` or `-r --path` options to designate a file or folder as the translation targate.

Default translation source language settings and translation targate language are English and Japanese. User can choose source language and targate language by using `--from` and `--to` options with translation language codes.

Also, by default, the translation is done by Amazon Translate, but it can be done by DeepL by using `--deepl` option. If you want to use DeepL, you need to set the API key of DeepL to the environment variable `DEEPL_API_KEY`.

User can use `--output` option to decide output folder (the folder need to exist).

For markdown file without hugo header add `--no-hugo` flag.
Is `--hugo` or nither `--hugo/--no-hugo` flag exist, then this tool regard inputs contain hugo header in .md file.

For more information see : `mdt --help`  
For command examples see [example](./docs/example.md)

### OPTIONS

```
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
  --deepl                         Translate with DeepL. To use this option,
                                  you need to set the API key of DeepL to the
                                  environment variable "DEEPL_API_KEY".
  --output PATH                   Directory where you want to output the
                                  translated contents  [default: ./]
  --debug                         Output some ast files for debug.
  --help                          Show this message and exit.
```

## Acknowledgments

Many thanks to you for your tremendous contribution.
