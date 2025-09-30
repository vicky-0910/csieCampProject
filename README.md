# 網站筆記 Note of the Website
> [!TIP]
> 網站連結 Link：[東華資工宿營2025](https://csiecamp-0919-21.ts.r.appspot.com/) (Due Time：2025-10-11)\
> 架構 Architecture：Django(Python), GoogleAppEngine, CloudSQL(MySQL)\
> 從各種資料慢慢找 + ChatGPT，不保證內容正確，總之網站會動🐄

## 檔案摘要 Files
```
- csieCampProject
  - [static]               #靜態檔案
  - [templates]            #模板(.html)
  - [csieCampProject]
      - \__init__.py
      - settings.py
      - urls.py
      - asgi.py
      - wsgi.py            #GAE框架類似nginx，main.py引入wsgi.py
  - [csieCampApp]
      - \__init__.py
      - admin.py
      - apps.py            #跟設定內的app名稱相關
      - models.py
      - tests.py
      - views.py
      - [migrations]
          - \__init__.py
  - manage.py
  - db.sqlite3
  - app.yaml
  - main.py
  - requirements.txt       #專案所需的python套件
```
