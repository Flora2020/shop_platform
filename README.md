# 電商平台（e-commerce platform）
## demo
連結：[https://shop-platform.herokuapp.com/](https://shop-platform.herokuapp.com/)

測試帳號
- 顯示名稱：Dannye
- 密碼：12345678

測試信用卡
- 信用卡號：4000-2211-1111-1111（一次付清）
- 有效月年：任意輸入未過期的日期
- 背面末三碼：任意輸入三個數字

首頁預覽圖
![shop-platform preview image](https://github.com/Flora2020/images/blob/main/shop-platform.png?raw=true)

## 功能（features）
### 未登入的訪客
1. 可以瀏覽所有商品
2. 可以將商品放入購物車

### 已登入的一般使用者
1. 可以使用「未登入的訪客」所有功能
2. 可以將購物車中的商品結帳
3. 可以上架商品
4. 可以瀏覽兩年內的所有訂單

## 環境建置與需求（prerequisites）
### 環境
- python 3.9.7
- pipenv

### 資料庫
MySQL 8.0.23

### 套件
- flask 2.0.2
- jinja2 3.0.2
- flask-sqlalchemy 2.5.1
- flask-migrate 3.1.0
- flask-seeder 1.2.0
- flask-mail 0.9.1
- flask-wtf 0.15.1
- flask-imgur 0.1
- pycryptodome 3.11.0

### 串接 API
- [藍新金流（NewebPay）](https://www.newebpay.com/website/Page/content/download_api)
- [imgur](https://apidocs.imgur.com)

## 安裝與執行 (installation and execution)
1. 下載此專案
 
``git clone https://github.com/Flora2020/shop_platform.git``

2. 移動至本專案資料夾

``cd shop_platform``

3. 建立虛擬環境

``pipenv --three``

4. 進入虛擬環境

``pipenv shell``

5. 安裝套件

``pipenv install``

6. 參考 .env.example 檔案，建立 .env 檔案
   - MAIL_USERNAME 與 MAIL_PASSWORD：因為 `app.config['MAIL_SERVER']` 的設定值是 `smtp.gmail.com`，意思是使用 gmail 寄送通知信，所以這兩個欄位需填寫 gmail 帳號及密碼。此帳號不能啟用二階段驗證，並且 [security](https://myaccount.google.com/u/2/security) 的 Less secure app access 項目需設置為 ON，以免登入失敗
   - URL：若在本地執行此專案，URL 不可直接使用 localhost 網址，可以使用 [ngrok](https://ngrok.com/) 產生的網址。以免藍新金流使用 ReturnURL 和 NotifyURL 時，無法連接正確的伺服器
   - MerchantID、HashKey、HashIV：註冊藍新金流帳號後方可取得。藍新金流[正式網站](https://www.newebpay.com/website/Page/content/register )、[測試網站](https://cwww.newebpay.com/website/Page/content/register)
   - PORT：藍新金流指定，ReturnURL 和 NotifyURL 的 PORT 需為 80 或 443
   - IMGUR_ID：登入 imgur 帳號後，[註冊應用程式](https://api.imgur.com/oauth2/addclient )取得的 Client ID。

7. 設定資料表

``flask db upgrade``

8. 新增種子資料

``flask seed run``

9. 啟動伺服器

``flask run`` 或 ``gunicorn "app:create_app()"``

10. 打開瀏覽器，於網址列輸入上一步驟中，終端機提供的網址，即可使用此專案之電商網站
