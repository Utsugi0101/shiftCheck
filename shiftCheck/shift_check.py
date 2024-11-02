import tkinter as tk
from datetime import datetime
import csv
import os

root = tk.Tk()
root.title("シフト管理システム")

users = ["寺嶋友海", "関智亮", "小野隼士", "山田美浩", "前沢壮栄", "吉岡秀人", "橘田真優", "小澤満月", "吉田吏玖", "阿部吉宏", "吉森光", "高橋空希"]
passwords = {"寺嶋友海": "202412025", "関智亮": "202410854", "小野隼士": "202312990", "山田美浩": "202311655", "前沢壮栄": "202310956", "吉岡秀人": "202312959", "橘田真優": "202410305", "小澤満月": "202411068", "吉田吏玖": "202411057", "阿部吉宏": "202311873", "吉森光": "202312169", "高橋空希": "202310355"}

# ユーザーの選択
selected_user = tk.StringVar(root)
selected_user.set(users[0])
label_user = tk.Label(root, text="ユーザーを選択:")
label_user.pack()
dropdown_user = tk.OptionMenu(root, selected_user, *users)
dropdown_user.pack()

# パスワード入力
label_password = tk.Label(root, text="学籍番号を入力:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# ユーザーごとのボタンの有効/無効状態を管理
button_enabled_users = {user: {"check_in": True, "check_out": True} for user in users}

# shiftCsvフォルダのパス
folder_name = "shiftCsv"
os.makedirs(folder_name, exist_ok=True)  # フォルダが存在しない場合は作成

def check_in_out(action):
    user_name = selected_user.get()  # 選択されたユーザー名を取得
    entered_password = entry_password.get()  # 入力されたパスワードを取得
    
    # パスワードの確認
    if entered_password != passwords[user_name]:
        label_status.config(text=f"{user_name}のパスワードが間違っています")
        return

    # ボタンの有効/無効を確認
    if not button_enabled_users[user_name][action]:
        label_status.config(text=f"{user_name}の{action}ボタンは少し待ってから再度試してください")
        return

    # 現在の時刻とユーザー名を取得
    current_datetime = datetime.now()
    date_str = current_datetime.strftime("%Y-%m-%d")
    time_str = current_datetime.strftime("%H:%M")

    # ファイルパスをshiftCsvフォルダ内に設定
    file_name = os.path.join(folder_name, f"{user_name}_shift_records.csv")
    
    # ファイルが存在しない場合のみ、列名を追加
    file_exists = os.path.isfile(file_name)
    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["日付", "時刻", "ユーザー名", "ステータス"])  # 見出しを追加
        # 記録するデータ
        status = "出勤" if action == "check_in" else "退勤"
        writer.writerow([date_str, time_str, user_name, status])
    
    # 確認メッセージ
    label_status.config(text=f"{user_name}の{status}記録が{date_str} {time_str}に保存されました")
    
    # 該当アクションのボタンを無効化し、1分間の待機を設定
    button_enabled_users[user_name][action] = False
    root.after(60000, lambda: enable_button(user_name, action))  # 60000ミリ秒 = 1分

def enable_button(user_name, action):
    # 該当アクションのボタンを再び有効化
    button_enabled_users[user_name][action] = True
    action_name = "出勤" if action == "check_in" else "退勤"

# 入出勤ボタンと退勤ボタン、状態表示ラベル
btn_check_in = tk.Button(root, text="出勤", command=lambda: check_in_out("check_in"))
btn_check_in.pack(pady=5)

btn_check_out = tk.Button(root, text="退勤", command=lambda: check_in_out("check_out"))
btn_check_out.pack(pady=5)

label_status = tk.Label(root, text="ユーザーを選択し、パスワードを入力して出勤・退勤ボタンを押してください")
label_status.pack()

# メインループ
root.mainloop()
