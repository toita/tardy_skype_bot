tardy_skype_bot
===============

概要
------

* 某チームでは、遅刻者には罰金が課せられる。これは、罰金総額を算出するbotである。

ルール
------

* 定時を9:30とみなす
* 年齢が20代の人は10円/分、30代の人は20円/分
* 当日休＆半休は、3000円

機能
----

* "@come"と打つと、打った時間から打った人の罰金が計算され昨日までの分に加算される
* "@plus toita 1000"と打つと、toitaの罰金に1000円加算される
* "@minus toita 1000"と打つと、toitaの罰金から1000円引かれる
* "@absent toita"と打つと、toitaの罰金に3000円加算される
