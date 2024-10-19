# pyxltree

エクセルのワークシートの境界線を使って、ツリー構造図を描画します

# 例１：ディレクトリー・パス

Output:  

![View](https://github.com/muzudho/pyxltree/raw/main/docs/img/202410__pg__18--1815-XltreeDrive.png)  

👆　わたしのWindows PCのCドライブの例です  

Input:  

![Data](https://github.com/muzudho/pyxltree/raw/main/docs/img/202410__pg__18--1832-XltreeDriveData.png)  

```csv
no,node0,node1,node2,node3,node4,node5,node6,node7,node8
1,C,Users,Muzudho,OneDrive,Documents,Tools,GitHub,,
2,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro,Engine,Lesserkai.exe
3,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro,Engine,Lesserkai_ja.txt
4,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro,Engine,public.bin
5,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro,ja,Shogidokoro.resources.dll
6,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro,Engine.xml,
7,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro,GameResult.xml,
8,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro,Shogidokoro.exe,
9,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro,Shogidokoro.xml,
10,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro,お読みください.txt,
11,C,Users,Muzudho,OneDrive,Documents,Tools,Shogidokoro.zip,,
12,C,Users,Muzudho,OneDrive,Documents,Tools,Visual Studio 2022,,
13,C,Users,Muzudho,OneDrive,Documents,Tools,Default.rdp,,
```

👆　さきほどの Output の図は、上図の CSV ファイルを読込ませると描いてくれます。  
`node` 列は 0 から始まる連番で増やすことができます。常識的な長さにしてください  

Script:  

```py
from xltree import WorkbookControl


def execute():

    # 出力先ワークブック指定
    wbc = WorkbookControl(target='./tests/temp/tree_drive.xlsx', mode='w')

    # ワークシート描画
    wbc.render_worksheet(target='Drive', based_on='./examples/data/tree_drive.csv')

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
```

👆　上記はスクリプトの記述例です  

# 例２：しりとり

Output:  

![View](https://github.com/muzudho/pyxltree/raw/main/docs/img/202410__pg__19--0020-XltreeWordChainGameView.png)  

👆　しりとりというゲームの記録です。図（Diagram）の辺（Edge）にテキストを書くのはオプションです  

Input:  

![Data](https://github.com/muzudho/pyxltree/raw/main/docs/img/202410__pg__19--0021-XltreeWordChainGameData.png)  

```csv
no,node0,edge1,node1,edge2,node2,edge3,node3,edge4,node4,edge5,node5,edge6,node6,edge7,node7,edge8,node8,edge9,node9
1,Word Chain Game,Ea,Eagle,E,Euler,R,Rex,$,ended with x,,,,,,,,,,
2,Word Chain Game,Eb,Ebony,Y,Yellow,W,Wood,D,Door,R,Rocket,T,Tax,$,ended with x,,,,
3,Word Chain Game,Ec,Eclair,R,Road,D,Dungeon,N,News,S,Sex,$,ended with x,,,,,,
4,Word Chain Game,Ed,Edelweiss,S,Sox,$,ended with x,,,,,,,,,,,,
7,Word Chain Game,En,English,Ha,Hand,Dog,Dog,G,Gorilla,A,Arm,M,Moon,N,Nice,$,adjective,,
6,Word Chain Game,En,English,Ha,Hand,Doo,Door,R,Ring,G,Grape,E,Egg,G,Golf,F,Fox,$,ended with x
5,Word Chain Game,En,English,Ha,Hand,Dr,Dragon,N,Nob,B,Box,$,ended with x,,,,,,
8,Word Chain Game,En,English,He,Hex,$,ended with x,,,,,,,,,,,,
9,Word Chain Game,En,English,Ho,Hook,Kit,Kitchen,N,Nickel,L,Lemon,N,Nickel,$,time up,,,,
10,Word Chain Game,En,English,Ho,Hook,Kin,King,G,Goal,L,Lemon,N,Nickel,L,Lemon,$,repetition,,
```

👆　`edge` 列は 1 から始まる連番で増やすことができます。 `node` 列より深い番号を付けても無視されます  
