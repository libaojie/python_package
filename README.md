# Python工程

## 工程介绍
    
    用于python的公共组件、各类项目结构模板以及知识点学习
   
    
## 公共组件


- [lbj-common](./python_wheel/lbj_common/README.md) 基础工具包
- [lbj-db](./python_wheel/lbj_db/README.md) 基础数据包
- [lbj-df](./python_wheel/lbj_df/README.md) DataFrame封装包
- [lbj-excel](./python_wheel/lbj_excel/README.md)   Excel操作封装包
- [lbj-flask](./python_wheel/lbj_flask/README.md)   Flask封装包
- [lbj-word](./python_wheel/lbj_word/README.md)   Word封装包


## 工程模板

- [00_sample](./python_template/00_sample/README.md) 最简单项目
- [01_package](./python_template/01_package/README.md) 单纯含打包的项目
- [02_package](./python_template/02_package/README.md) 含自定义组件的项目
- [03_flask_jinja](./python_template/03_flask_jinja/README.md) Flask前后端均有的项目
- [04_flask](./python_template/04_flask/README.md) Flask后端对接SpringCLoud Socket Docker均有的项目


## 实用工具

- [01_postman_json](./python_tool/01_postman_json/README.md) 提取Postman文件的json文件中的关键信息
- [02_tensorflow](./python_tool/02_tensorflow/README.md) tensorflow学习项目
- [03_db2api](./python_tool/03_db2api/README.md) 连接数据库生成wordapi文档


## 知识学习


    
## 推荐环境
    python 3.8.8
    poetry 1.2.0

    python -m pip list
    python -m pip install poetry==1.2.0
###设置poetry路径
    poetry config --list
    1、
    C:\Users\snow\AppData\Roaming\pypoetry\config.toml
    cache-dir = "D:\\venv\\poetry"
    2、
    poetry config virtualenvs.path "D:\\venv\\poetry"

### 导出
    poetry export -f requirements.txt --output requirements.txt
    poetry run pip freeze > requirements.txt

### 加入新包
    poetry add gevent 