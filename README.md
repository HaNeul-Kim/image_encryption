# image_encryption
画像暗号化の勉強のためのリポジトリです。

This is a repository for my study on image encryption.

## Prerequisites
+ OpenCV(for python) >= 2.4.13
+ python 2.x or 3.x
+ Required python libraries:
  
  - numpy
  - scipy

## Usage
```
python main.py [-e|-d] --key [KEY] --input [INPUT]
```
+ `-e | -d`: Select encrypt/decrypt mode (`-e`: encrypt, `-d`: decrypt)
+ `KEY`: 32-digit hexadecimal encryption key

  - default: `"e5 da 75 0b 4c 1f 78 d3 28 ea 25 e6 b1 5c f9 43"`
  - カスタムキーを使う場合は、2文字ごとに半角スペースを入れてください。
  - A-E(10-15)は小文字で入力してください(大文字で認識できるかをまだ確認していないため)。
  
+ `INPUT`: Input image file path (Unix form)

##  References
[1] Pareek, N.K. & Patidar, V. Soft Comput (2016) 20: 763. https://doi.org/10.1007/s00500-014-1539-7
