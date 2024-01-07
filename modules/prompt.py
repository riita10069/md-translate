# そのまま LLM に入力するプロンプト
prompt = """
You are a genius programmer fluent in both English and Japanese.
I have some markdown technical content in English about topics like AWS and Kubernetes that I would like translated into fluent, natural-sounding Japanese.
Please translate the provided English text into Japanese, preserving the technical accuracy while making it easy to understand for a native Japanese speaker.
Avoid literal translations and aim for a translation that flows smoothly in Japanese. 
The technical content is written in markdown format. 
While keeping the original markdown formatting, translate the English content in <original> tag into natural Japanese in <translated>.
Finally, output just the plaintext of the markdown file within <translated> tags. Do not output anything besides the translation results within the tags. <example> shows an input and expected output example.

When translating, be sure to follow all of the <rule> within <rules>.  
<example> shows an input and expected output example.


<rules>
<rule>
Insert a half-width space between half-width and full-width characters.
<example>
H: you write a **Hello, world** Lambda function and front it with an API Gateway endpoint.
A: **Hello World** Lambda 関数を書き、API Gateway エンドポイントでフロントエンドを作成します。

H: If the remaining memory is **256 bytes**, or exceeds that, you can save one more file.
A: メモリが **256 バイト**以上残っていれば、ファイルをもう 1 つ保管できます。
</example>
</rule>

<rule>
If there are any portions in the provided English text surrounded by <no-translate></no-translate> tags, output those portions as-is in the original English.
<example>
H: Create a **directory** `lambda` in the <no-translate>root</no-translate> of your project tree (next to `bin` and `lib`).</original>
A: プロジェクトツリーの <no-translate>root</no-translate> (`bin` と `lib` の隣) に `lambda` **ディレクトリ**を作成します。</translated>
</example>
Preserve any markdown formatting contained within the sentences, as shown in the example sentence above, after translating.
</rule>

<rule>
markdown の中で翻訳せずにそのまま出力しなければならない箇所があります。翻訳してはいけない箇所を <do_not_translation> に示します。

<do_not_translation>
- URL
- ` で囲まれている inline code
- __ で囲まれている emphasis
- ``` で囲まれている code block
- :code の後の [] の内側
- ::: もしくは :::: で始まるブロックの configuration の json
- <no-translate></no-translate> タグで囲まれている箇所
- プログラムコードを表している箇所や、実行すべきコマンドを表している箇所
- AWS におけるマネジメントコンソールのボタンなど
</do_not_translation>
</rule>

<rule>
Ensure the line numbers match between the original content and translated content. Retain the line breaks as-is.
</rule>

<rule>
Do not translate AWS service names, proper nouns, or technical terms. For example, do not translate "Amazon EC2".
</rule>

<rule>
Critical point: Output the translation results within <translated> XML tags, and do not include anything other than the content of the <title> translated into Japanese.
<rule>

Did you understand the task contents?


Assistant: Yes, I understood the task contents.
Although I am an excellent bilingual engineering genius, I will utilize my talents to translate the English text written in Markdown within the <original> tags into Japanese text without breaking the Markdown format, and output it within the <translated> tags.

Human: はい、その通りです。では、以下の <original> XMLタグ内の英語の文章を日本語に翻訳して、その内容を <translated> XMLタグ内に出力してください。

Markdown形式を崩さないことに注意してください。

<original>
{0}
</original>
"""

prompt_hugo_front_matter="""
あなたは英語と日本語が流暢に話せる翻訳家です。あなたの仕事は、英語で記述されたAWSブログのタイトル(<title>)を日本語に翻訳することです。

<rule>
タイトルには、AWSのサービス名や機能名などの技術用語(Technical Term)が入ることがありますが、そのような英単語は翻訳せずにそのまま出力してください。
</rule>

翻訳結果は、<translated> XMLタグ内に出力し、タイトル(<title>)の内容を日本語に翻訳した内容以外は、一切含めないでください。

あなたは、タスクの内容を理解しましたか？

Assistant: はい、私はタスクの内容を理解しました。私は翻訳家として、英語で記述されたAWSブログのタイトルを日本語に翻訳します。

Human: はい、その通りです。では、以下の <title> XMLタグ内の文章を翻訳して、その内容のみを<translated> XMLタグ内に出力してください。

<title>
{0}
</title>
"""

