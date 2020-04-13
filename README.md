# remote-cointainer-template
リモートコンテナで開発する場合のテンプレートです。
サンプルとしてFlaskを使えるようにしていますが、自分の開発環境に合わせて書き換えてください。

## 概要
　チームで開発をするときに環境構築の構築で躓くことがよくあります。例えば
 - **OSの違い**によって環境構築の方法が違う。Macで動くものがWindowsで動かなかったりする。逆もまた然り。
 - そもそもOS同じで同じものをインストールしているはずなのに**なぜか**動かない！

などがあります。
 それを解決する手段として、
 
 　Dockerコンテナ上で開発環境を作ってVSCodeで編集&CUI直接操作ができる。
  ついでにローカルの.gitconfig勝手にコピーしてくれるから、特に何もしなくてもローカルにgitを使える環境があればコンテナ内ですぐ使える。 

  という方法があるので共有します。
## 環境構築の方法
[Windows 10 proとMacの場合](https://github.com/wgdp444/remote-container-template/blob/master/doc/winpro-mac.md)
[Windows Homeの場合](https://github.com/wgdp444/remote-container-template/blob/master/doc/winhome.md)

## 各ファイルの簡単な解説
## 各ファイルの解説
### Dockerfile
コンテナの詳細を記述します。サンプルのソースではPython3公式イメージをpullし、作業ディレクトリを指定しています。
### docker-compose.yml
複数のコンテナを一括で管理するのに必要なファイルです。
Dockerはプロセス(サービス)ごとに一つのコンテナを使用することを推奨しているので、ここで複数のコンテナを使用した開発環境を定義したりできます。
### devcontainer.json
コンテナに対するVSCodeの設定です。どの設定ファイルを読み込むのかやコンテナ起動時に実行するコマンドなどを定義できます。