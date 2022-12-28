import gzip
import shutil
import re
import glob
import datetime


# フォルダ内のファイル取得
gzip_folders = glob.glob('./gzfolders/*')
# 解凍後のファイルパス
unzip_logs = './files/1_unzip_log'

# ファイルの解凍
def unziplogs():
    for gzip_folder in gzip_folders:
        with gzip.open(gzip_folder, mode='rb') as gzip_file:
            with open(unzip_logs, mode='ab') as text_file:
                shutil.copyfileobj(gzip_file, text_file)
    return


# デコード用関数
def byte_to_str(byte_list: list) -> list:
    return [i.decode('utf8') for i in byte_list]


# 改行前後のファイルパス
before_search_logs = './files/1_unzip_log'
after_search_logs = './files/2_search_log'

# ログの不要な改行削除
def searchlogs():
    with open(before_search_logs, 'rb') as a:
        a_files = a.readlines()
        
        line_rm = [re.sub('^\n', '', z) for z in byte_to_str(a_files)]    # 空白行削除
        english_rm = [re.sub('^([a-zA-Z]*)$\n', r'\1', y) for y in line_rm]    # 先頭からアルファベットが並んでいる場合の行末の改行削除
        num_line_rm = [re.sub('([0-9])\n', r'\1', x) for x in english_rm]   # 数字の後の改行削除
        symbol_rm = [re.sub('\[\n', '[', yy) for yy in num_line_rm]     # 2022/10/26追記（［の後の改行削除）
        eng_rm = [re.sub('([a-zA-Z])$\n', r'\1', xx) for xx in symbol_rm]   # 2022/12/28追記（アルファベットのすぐ後の改行削除）
        
        with open(after_search_logs, 'a', encoding='CP932', errors='ignore') as b:
            return [b.write(w) for w in eng_rm]


# 昇順前後のファイルパス
before_sort_logs = './files/2_search_log'
after_sort_logs = './files/3_sort_logs'

# ログを昇順に並び替え
def sortlogs():
    with open(before_sort_logs, 'r') as c:
        lines = c.readlines()
        lines.sort()

        with open(after_sort_logs, 'w') as d:
            return [d.write(v) for v in lines]


# ファイル名の月を取得
today = datetime.date.today()
month = today.strftime('%m')

# 置換前後のファイルパス
before_rep_logs = './files/3_sort_logs'
after_rep_logs = f'./files/{month}月分ログ.txt'

# 不要な個所を置換
def replacementlogs():
    with open(before_rep_logs, 'r') as e:
        rep_lines = e.readlines()
        
        rep_line = [re.sub('^.*Z ', '', u) for u in rep_lines]
        with open(after_rep_logs, 'a', encoding='CP932', errors='ignore') as f:
            return [f.write(t) for t in rep_line]


print('ファイルの解凍スタート...')
unziplogs()
print('ファイルの解凍終了！')

print('\r\n')

print('不要な改行削除スタート...')
searchlogs()
print('不要な改行削除終了！')

print('\r\n')

print('並び替えスタート...')
sortlogs()
print('並び替え完了！')

print('\r\n')

print('置換スタート...')
replacementlogs()
print('置換終了！')

