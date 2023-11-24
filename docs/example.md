# Workshop-translator command examples

1. To translate a index.md file from English to Japanese with hugo header.

```bash
mdt --path index.md
```

2. To translate a index.md file from English to Japanese without hugo header (pure markdown file)

```bash
mdt --path index.md --no-hugo
```

3. To translate a index.md file from English to Chinese

```bash
mdt --path index.md --from en --to zh
```

4. To translate a index.md file from English to Japanese using DeepL API Free

```bash
export DEEPL_API_KEY=<YourDeepLAPIKey>
mdt --path index.md --deepl-free
```

You can generate a DeepL API key from [this page](https://www.deepl.com/pro-api).  
The language specification method is the same when using Amazon Translate.

5. To translate a index.md file from English to Japanese using DeepL API Pro

```bash
export DEEPL_API_KEY=<YourDeepLAPIKey>
mdt --path index.md --deepl-pro
```

6. To translate a index.md file from English to Japanese using Claude v2

```bash
mdt --path index.md --claude
```

7. To translate all .md files in folder samples recursively from English to Japanese

```bash
mdt -r --path samples
```

8. To translate a file and output to a designated folder (name: translated) from English to Chinese

```bash
mkdir translated
mdt --path index.md --from en --to zh --output translated
```
