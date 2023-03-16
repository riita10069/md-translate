# md-translate (Markdown Translation Tool)

A CLI tool for translating documents written in markdown.

## Prerequirements

```
npm install -g remark-cli
npm install -g remark-directive
```

## Instalation

```
pip3 install git+https://github.com/riita10069/md-translate.git
```

## Usage

`mdt --path index.md`

### OPTIONS

```
Options:
  --path PATH                     directory or file path where you want to
                                  translate  [required]
  --src-lang [af|sq|am|ar|hy|az|bn|bs|bg|ca|zh|zh-TW|hr|cs|da|fa-AF|nl|en|et|fa|tl|fi|fr|fr-CA|ka|de|el|gu|ht|ha|he|hi|hu|is|id|ga|it|ja|kn|kk|ko|lv|lt|mk|ms|ml|mt|mr|mn|no|ps|pl|pt|pt-PT|pa|ro|ru|sr|si|sk|sl|so|es|es-MX|sw|sv|ta|te|th|tr|uk|ur|uz|vi|cy]
                                  source language  [default: en]
  --dest-lang [af|sq|am|ar|hy|az|bn|bs|bg|ca|zh|zh-TW|hr|cs|da|fa-AF|nl|en|et|fa|tl|fi|fr|fr-CA|ka|de|el|gu|ht|ha|he|hi|hu|is|id|ga|it|ja|kn|kk|ko|lv|lt|mk|ms|ml|mt|mr|mn|no|ps|pl|pt|pt-PT|pa|ro|ru|sr|si|sk|sl|so|es|es-MX|sw|sv|ta|te|th|tr|uk|ur|uz|vi|cy]
                                  post-translation language  [default: ja]
  --output PATH                   directory where you want to output the
                                  translated contents  [default: ./]
  --debug                         output some ast files for debug
  --help                          Show this message and exit.
```

## Acknowledgments

Many thanks to  you for your tremendous contribution.
