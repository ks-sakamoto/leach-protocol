# leach-protocol
 leachプロトコル実装検討用のリポジトリ

 ## leachプロトコルの実装がmicropythonで使用できるように修正する
 ## 最終的に使用する実装のみresearch-fversionに移動する予定

 *検討する実装一覧*
 - pashashahbaz/leach-main: leach is a routing protocol in wireless sensor network which is used to extend the lifetime of wireless sensor network by reducing the energy consumption. (github.com)
   - ~~使えそうだけど修正が必要~~
   - ~~Energy2.py,line 99/FindReceiver2.py,line 16/でエラーが出る~~
   - ~~tuple indices must be integers or slices, not str~~
   - エラーは修正できたが、実装としては微妙
   - 変数名の単純なミスなどが多すぎる、グラフも変な感じ、作成者は動作確認していないのでは？
 - HritwikSinghal/LEACH-PY: Leach code in Python (github.com)
 - zerokay/LEACH-master: WSN の LEACH ルーティングプロトコル (github.com)
 - bernardkkt/wsn-leach: Assignment for WSN on LEACH protocol and its improvements (github.com)
 -  IshrakAbedin/LEACHClusterHeadSim: A simple Python Simulation for understanding the behavioral pattern of LEACH cluster heads (github.com)
 - LEACH-Project/Start.py at master · kkgarai/LEACH-Project (github.com)
 - manasjohri/Leach-Energy-Model (github.com)
