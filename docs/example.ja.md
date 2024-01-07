# Workshop-translator コマンド例

1. hugo ヘッダーを使用して index.md ファイルを英語から日本語に翻訳する

```bash
mdt --path index.md
```

2. hugo ヘッダーなし(純粋なマークダウンファイル)の index.md ファイルを英語から日本語に翻訳する

```bash
mdt --path index.md --no-hugo
```

3. index.md ファイルを英語から中国語に翻訳する

```bash
mdt --path index.md --from en --to zh  
```

4. DeepL API Free を使用して index.md ファイルを英語から日本語に翻訳する

```bash
export DEEPL_API_KEY=<yourdeeplapikey>
mdt --path index.md --deepl-free
```

DeepL API キーは[このページ](https://www.deepl.com/pro-api)から生成できます。  
Amazon Translate を使用する場合の言語指定方法は同じです。

5. DeepL API Pro を使用して index.md ファイルを英語から日本語に翻訳する

```bash
export DEEPL_API_KEY=<yourdeeplapikey>  
mdt --path index.md --deepl-pro
```

6. Claude v2 を使用して index.md ファイルを英語から日本語に翻訳する

```bash
mdt --path index.md --claude
```

7. samples フォルダ内のすべての .md ファイルを再帰的に英語から日本語に翻訳する

```bash 
mdt -r --path samples
```

8. ファイルを翻訳して、指定したフォルダ(名前: translated)に出力する(英語から中国語)

```bash
mkdir translated
mdt --path index.md --from en --to zh --output translated
```
