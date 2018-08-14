## 概要

[ブロックチェ－ンを構築しながら学ぶ](https://postd.cc/learn-blockchains-by-building-one/)を[簡単にlocalhostで複数立てれるようにしてみたもの](https://github.com/aki85/python-bcserver)を、pythonで試しやすくしてみた。

## 環境
python3.6以上  
`pip install Flask==0.12.2 requests==2.18.4`  
## 実行方法
localhostで複数サーバーを立てた後  
`python bcclient.py`  
`request to: port action (options)`  
### 例  
`request to: 5000 mine`  
`request to: 5001 mine`  
`request to: 5001 send target=5000 amount=1`  


## 遊び方
ターミナルで起動して、以下のコマンドを使ってみる

|action|option|result|
|:--|:--|:--|
|mine||1回マイニングする|
|chain||自分のチェーンを見る|
|send|target=port amount=number|トランザクションを作成する|
|register|target=port|他サーバーのチェーンを確認する準備|
|register|target=port1,port2,port3|複数同時に登録も可能|
|load||他サーバーのチェーンを確認する|
|reboot||サーバーをリセットする|
  
### 例  
`request to: 5000 register target=5001`  
`request to: 5001 register target=5000`  
`request to: 5000 mine`  
`request to: 5001 mine`  
`request to: 5001 send target=5000 amount=1`  
`request to: 5001 mine`  
`request to: 5001 chain`  
`request to: 5000 chain`  
`request to: 5001 resolve`  
`request to: 5000 resolve`  

## 注意事項
不完全な部分があるため、一部補足です

* send actionは、自分とターゲットのサーバーで一度、mine actionを行う必要があります
* send actionは、所持する量の確認をしていないので、所持していなくても送信することができます
