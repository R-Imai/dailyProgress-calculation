# calc_timer
日々の業務記録をまとめるやつ

## 使い方
`python calc_timer.py -f 記録しているjsonファイルのパス -d 日付`

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
