KHRをネット経由で操作するためのプログラム。使い方はこちらの記事をご覧ください。

新型コロナで大きな影響を受けたロボットバトル、リモートでやれんのか！
https://monoist.atmarkit.co.jp/mn/articles/2010/26/news017.html

・khr_server:
LAN内での使用を想定したバージョン。

・khr_server_nat:
NATを越えてLAN外からアクセスする必要があるときのために、GoogleのSTUNサーバーと通信し、WAN側のIPアドレスとポート番号を調べて表示しています。この機能のために、pynatというモジュールを追加で使用しています。
