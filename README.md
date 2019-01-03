# calc_timer
日々の業務記録をまとめるやつ

# 新バージョン

## 使い方
```
set FLASK_APP=rest_endpoint.py
flask run
```

## 使えるAPI

|URL|機能|パラメータ|
|---|---|---|
|GET /calc/daily|日付計算|day: 日付<br>path: ファイルのパス|
|POST /record/start|業務スタートを記録|val: 値|
|GET /record/start|スタート記録取得| - |
|POST /record/end|業務終了記録|day: 日付<br>path: ファイルのパス<br>subj: 業務内容<br>val: 作業開始、終了時刻|
|POST /setting/path|記録ファイルpath更新|path: ファイルのパス|
|GET /setting/path|記録ファイルpath取得|-|
|GET /record/get|業務記録取得|day: 日付<br>path: ファイルのパス|
|POST /record/edit|業務記録編集|day: 日付<br>path: ファイルのパス<br>val: 編集後Json文字列|

---

# 旧バージョン

## 使い方
`python calc_timer.py -f 記録しているjsonファイルのパス [-d 日付] [-p]` <br>
> `-p` : jsonファイル内のすべてのデータを集計して円グラフで出力する．

## jsonファイルの中身の書き方
```
{
    "日付":{
        "業務内容":"開始時刻-終了時刻",
        "業務内容":"開始時刻-終了時刻",
        "業務内容":"開始時刻-終了時刻"
    },
    "日付":{
        "業務内容":"開始時刻-終了時刻",
        "業務内容":"開始時刻-終了時刻"
    },
                    .
                    .
                    .
    "日付":{
        "業務内容":"開始時刻-終了時刻",
        "業務内容":"開始時刻-終了時刻"
    }
}
```
#### 業務内容の書き方
`業務内容` もしくは，`業務の大きなくくり/細かい内容`

#### 時刻のフォーマット
`HH:MM`

## 出力内容
```
- 業務内容: 1h30m
- 業務内容: 30m
- 業務の大きなくくり=>細かい内容: 1h
```
