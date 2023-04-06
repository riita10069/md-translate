# Workshop-translator command examples

1. To translate a index.md file from English to Japanese with hugo header.
```
mdt --path index.md
```

2. To translate a index.md file from English to Japanese without hugo header (pure markdown file)
```
mdt --path index.md --no-hugo
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
