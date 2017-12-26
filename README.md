# twse
download data from TWSE(臺灣證券交易所)

用Python寫的小程式，
由台灣證券交易所的網站，下載特定的資料。
下載的範圍為自行指定的日期區間。

## 資料來源
* [每日市場成交資訊](http://www.twse.com.tw/zh/page/trading/exchange/FMTQIK.html)

    [CSV下載連結（以2017/12為例）](http://www.twse.com.tw/exchangeReport/FMTQIK?response=csv&date=20171201)

    ![FMTQIK](/screenshots/FMTQIK.png?raw=true "FMTQIK")


* [每5秒委託成交統計](http://www.twse.com.tw/zh/page/trading/exchange/MI_5MINS.html)

    [CSV下載連結（以2017/12/01為例）](http://www.twse.com.tw/exchangeReport/MI_5MINS?response=csv&date=20171201)

    ![MI_5MINS](/screenshots/MI_5MINS.png?raw=true "MI_5MINS")

* [每5秒指數盤後統計TWSE](http://www.twse.com.tw/zh/page/trading/exchange/MI_5MINS_INDEX.html)

    [CSV下載連結（以2017/12/01為例）](http://www.twse.com.tw/exchangeReport/MI_5MINS_INDEX?response=csv&date=20171201)

    ![MI_5MINS_INDEX](/screenshots/MI_5MINS_INDEX.png?raw=true "MI_5MINS_INDEX")


## Requirements
* Python 3

* dateutil套件

    先安裝python3-pip
    ```
    sudo apt install python3-pip
    ```
    再使用pip3安裝python-dateutil套件
    ```
    pip3 install python-dateutil
    pip3 install --upgrade pip
    ```

* pandas套件
    ```
    sudo pip3 install pandas
    ```


## Code structure
```
twse
├── all_data
├── FMTQIK
├── MI_5MINS
└── MI_5MINS_INDEX
```

File/Folder          |	Description
 --------------------| ------------------------------------------------ 
.gitignore           | gitignore
all_data	     | 清理、合併後的資料
FMTQIK               | 檔案下載的存取目錄（每日市場成交資訊）
MI_5MINS	     | 檔案下載的存取目錄（每5秒委託成交統計）
MI_5MINS_INDEX       | 檔案下載的存取目錄（每5秒指數盤後統計TWSE）
screenshots          | README.md使用的截圖
README.md            | README
download_csv.py      | 下載檔案的程式碼
pre_data.py	     | 初步處理下載的csv資料（清理、合併），並存至 all data

## 日期設定
```
start_dt = date(2017, 11, 30)
end_dt = date(2017, 12, 4)
```
由程式碼中自行輸入所需的資料區間。

檢查檔案下載的存取目錄，若該檔案存在，不會重複下載。

每次下載檔案後會等待1~10秒才繼續進行，避免短時間內大量存取，影響網頁伺服器。

## 我的開發環境：
* Ubuntu 16.04.3 LTS
* Python 3.5.2
* PyCharm Community Edition 2017.2.4

尚未在其他環境測試，不確定是否能支援。
