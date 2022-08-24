# leach-protocol
 ## leachプロトコル実装検討用のリポジトリ

 ## leachプロトコルの実装がmicropythonで使用できるように修正する
 ## 最終的に使用する実装のみresearch-fversionに移動する予定
 
 <br/>

 *検討する実装一覧*
 - pashashahbaz/leach-main: leach is a routing protocol in wireless sensor network which is used to extend the lifetime of wireless sensor network by reducing the energy consumption. (github.com)
   - ~~使えそうだけど修正が必要~~
   - ~~Energy2.py,line 99/FindReceiver2.py,line 16/でエラーが出る~~
   - ~~tuple indices must be integers or slices, not str~~
   - エラーは修正できたが、実装としては微妙
   - 変数名の単純なミスなどが多すぎる、グラフも変な感じ、作成者は動作確認していないのでは？
 - HritwikSinghal/LEACH-PY: Leach code in Python (github.com)
   - LEACH-Project-masterとほぼ一緒
   - こっちの方が見やすいかも?
 - zerokay/LEACH-master: WSN の LEACH ルーティングプロトコル (github.com)
   - 使えそう
 - bernardkkt/wsn-leach: Assignment for WSN on LEACH protocol and its improvements (github.com)
   - 使えるかも
 - IshrakAbedin/LEACHClusterHeadSim: A simple Python Simulation for understanding the behavioral pattern of LEACH cluster heads (github.com)
   - LEACHのクラスタヘッドの生成パターンをシミュレーションするためのシンプルな実装
   - クラスタヘッドの生成しか行ってなさそう
 - LEACH-Project/Start.py at master · kkgarai/LEACH-Project (github.com)
   - LEACH-PYとほぼ一緒
 - manasjohri/Leach-Energy-Model (github.com)
   - LEACHプロトコルを構築したとあるが、関数的に実装しておらず、どこでデータを送受信しているか、どこでクラスタヘッドを選択しているか、などが分かりにくく使いづらい
   - おそらくエネルギー量だけに焦点を当てた実装コードなのでは? 実装コードがすごく短い
