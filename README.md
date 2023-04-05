# md-translate (Markdown Translation Tool)

A CLI tool for translating documents written in markdown.

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
$ mdt --path index.md --hugo
```

This command line tool minumum requires `--path` or `-r --path` options to designate a file or folder as the translation targate.

Default translation source language settings and translation targate language are English and Japanese. User can choose source language and targate language by using `--from` and `--to` options with translation language codes.

User can use `--output` option to decide output folder (the folder need to exist).

For more information see : `mdt --help`
For command examples see [example](./docs/example.md)

### OPTIONS

```
Options:
  --path PATH                     directory or file path where you want to
                                  translate  [required]
  -r, --recursive                 translate recursively for subdirectories

  --hugo                          translate with hugo front matter, which is
                                  metadata about hugo site
  --from [af|sq|am|ar|hy|az|bn|bs|bg|ca|zh|zh-TW|hr|cs|da|fa-AF|nl|en|et|fa|tl|fi|fr|fr-CA|ka|de|el|gu|ht|ha|he|hi|hu|is|id|ga|it|ja|kn|kk|ko|lv|lt|mk|ms|ml|mt|mr|mn|no|ps|pl|pt|pt-PT|pa|ro|ru|sr|si|sk|sl|so|es|es-MX|sw|sv|ta|te|th|tr|uk|ur|uz|vi|cy]

                                  source language  [default: en]
  --to [af|sq|am|ar|hy|az|bn|bs|bg|ca|zh|zh-TW|hr|cs|da|fa-AF|nl|en|et|fa|tl|fi|fr|fr-CA|ka|de|el|gu|ht|ha|he|hi|hu|is|id|ga|it|ja|kn|kk|ko|lv|lt|mk|ms|ml|mt|mr|mn|no|ps|pl|pt|pt-PT|pa|ro|ru|sr|si|sk|sl|so|es|es-MX|sw|sv|ta|te|th|tr|uk|ur|uz|vi|cy]
                                  post-translation language  [default: ja]
  --output PATH                   directory where you want to output the
                                  translated contents  [default: ./]
  --debug                         output some ast files for debug
  --help                          Show this message and exit.
```

## Acknowledgments

Many thanks to you for your tremendous contribution.
