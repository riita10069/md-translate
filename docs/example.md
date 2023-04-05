# Workshop-translator command examples
This command line tool minumum requires `--path` option to designate a file or folder as the translation targate.

The default translation source language regarded as English and translation targate language is Japanese. User can choose source language and targate language by using `--from` and `--to` options with translation language codes.

1. To translate a index.md file from English to Japanese
```
mdt --path index.md
```
2. To translate a index.md file from English to Chinese
```
mdt --path index.md --from en --to zh
```

3. To translate all .md files in folder samples recursively from English to Japanese
```
mdt -r --path samples
```

4. To translate a file and output to a designated folder (name: translated) from English to Chinese
```
mkdir translated
mdt --path index.md --from en --to zh --output translated
```
