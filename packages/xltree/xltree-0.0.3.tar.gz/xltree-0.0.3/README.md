# pyxltree

エクセルのワークシートの境界線を使って、ツリー構造図を描画します

# 例：ディレクトリー・パス

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
    wbc = WorkbookControl(target='./tests/temp/tree_drive.xlsx')

    # ワークシート描画
    wbc.render_worksheet(target='Drive', based_on='./tests/data/tree_drive.csv')

    # 何かワークシートを１つ作成したあとで、最初から入っている 'Sheet' を削除
    wbc.remove_worksheet(target='Sheet')

    # 保存
    wbc.save_workbook()
```

👆　上記はスクリプトの記述例です  
