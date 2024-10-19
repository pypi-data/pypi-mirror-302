#
# python test.py
#
# エクセルで樹形図を描こう
#

import traceback
import datetime
import sys

from tests.render import test_render
from tests.render_2 import test_render as test_render_2


########################################
# コマンドから実行時
########################################
if __name__ == '__main__':
    """コマンドから実行時"""

    try:
        args = sys.argv

        if 1 < len(args):
            if args[1] == '2':
                # テスト
                test_render_2()
            
            else:
                raise ValueError(f'unsupported {args[1]=}')
        
        else:
            # テスト
            test_render()


    except Exception as err:
        print(f"""\
[{datetime.datetime.now()}] おお、残念！　例外が投げられてしまった！
{type(err)=}  {err=}

以下はスタックトレース表示じゃ。
{traceback.format_exc()}
""")
