MVDIS - 監理服務網
------------------

* TourBus: [遊覽車公司列表](https://www.mvdis.gov.tw/m3-emv-mk3/tourBus/query)
* Penalty: [法人查詢罰鍰繳納紀錄](https://www.mvdis.gov.tw/m3-emv-vil/vil/penaltyQueryPayRecord/legal)

# Quickstart Tutorial

* 查詢法人罰鍰繳納紀錄

```python
from mvdis import penalty

p = penalty.PenaltyRecord('70373538')  # 駿勝交通有限公司
p.image.show()  # 顯示 CAPTCHA
captcha = input('請輸入 CAPTCHA: ')

data = p.query(captcha)  # 查詢資料
data = p.next()          # 下一頁資料
data = p.prev()          # 上一頁資料
data = p.goto(10)        # 第 10 頁資料
```

* 查詢遊覽車公司資料

```python
from mvdis import tourbus

t = tourbus.TourBus()
data = t.next()          # 下一頁資料
data = t.prev()          # 上一頁資料
data = t.goto(10)        # 第 10 頁資料

```

