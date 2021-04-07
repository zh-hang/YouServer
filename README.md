# YouServer

## 部署

### 创建虚拟环境

```shell
python3 -m venv venv
. venv/bin/activate
```

### 安装flask

```shell
pip install Flask
```
### 配置数据库

```shell
pip install sqlite3
python3 database_init.py
```

### 运行

```shell
export FLASK_APP=app.py
flask run --host=0.0.0.0
```

