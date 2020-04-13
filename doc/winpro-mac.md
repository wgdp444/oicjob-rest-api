# Windows 10 proとMacの場合
## 環境構築に必要なもの
- Visual Studio Code
    - remote container(VSCodeの拡張機能)
- Docker
- ファイル(githubからforkやclone)
    - Dockerfile
    - docker-compose.yml
    - devcontainer.json
## ファイル構成
```
作業ディレクトリ(.)
├── .devcontainer
│   ├── Dockerfile
│   ├── devcontainer.json
│   └── docker-compose.yml
├── その他のファイルやディレクトリなど自分の開発に必要なもの
```
## 1. Dockerをインストールする

　まずWindowsの場合は、
 
 **Docker for Windows**
 
 Macの場合は、
 
 **Docker for Mac**
 
 を[dockerの公式サイト](https://www.docker.com/products/docker-desktop)からダウンロードしてインストールします。
## 2. remote cointainerをインストールする。
 
 VSCodeの拡張機能の**RemoteContainer**をインストールしておきます。VSCodeの拡張機能のタブから検索すれば見つかると思います。
![](https://i.imgur.com/jzzPVNE.png)

## 3. 開発環境テンプレートの作成
 
 [これ(githubリンク)](https://github.com/wgdp444/remote-container-template.git)を自分のリポジトリにforkしてcloneしてください。
 cloneできたら自分の開発したい環境に合わせて適宜書き換えてください。
 
## 4. コンテナを立ち上げVSCodeに接続する。
RemoteContainerをインストールできていたら、
![](https://i.imgur.com/tgKAb0Z.png)
VSCodeの左下にこんな形のボタンがあるので、これを押して、
![](https://i.imgur.com/dQOHNT5.png)
から作業ディレクトリを開きます。
コンテナが立ち上がって、作業ディレクトリが正常にマウントされたら完了です！

## トラブルシューティング
### case1. コンテナ起動時にエラーが発生する
1. コンテナをReBuildしてみてください。それでもダメそうならVirtualBoxとDockerを再インストールしてもう一度試してみてください。