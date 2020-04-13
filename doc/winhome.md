# Windows 10 homeの場合
## 環境構築に必要なもの
- Visual Studio Code
    - remote container(VSCodeの拡張機能)
- Docker
- VirtualBox(DockerToolBoxインストール時に自動でインストールされます)
- ファイル(githubからforkやclone)
    - Dockerfile
    - docker-compose.yml
    - devcontainer.json

## 1. Dockerをインストールする

　Windows Homeの場合は現状Docker for Windowsが使用できないので、DockerToolBoxを使用します。
[こちら](https://qiita.com/idani/items/fb7681d79eeb48c05144)を参照してDockerToolBoxをインストールして起動を確認してください。VirturlBoxをインストールするかどうかを聞かれるので、チェックを入れるのを忘れないようにしてください。

## 2. RemoteCointainerをインストールする。
 
 VSCodeの拡張機能の**remote container**をインストールしておきます。VSCodeの拡張機能のタブから検索すれば見つかると思います。
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
### case1. DockerToolBoxが起動しない
1. BIOSの設定からVT-xを有効にしてください。
2. それでも起動しない場合はコマンドプロンプトで、
`docker-machine create -d virtualbox --virtualbox-memory=2048 --virtualbox-no-vtx-check default`
で起動できる場合があります。([この現象の詳細についてのリンク](https://github.com/docker/toolbox/issues/830))
### case2. コンテナ起動時にエラーが発生する
1. コンテナをReBuildしてみてください。それでもダメそうならVirtualBoxとDockerを再インストールしてもう一度試してみてください。