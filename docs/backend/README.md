# 说明

后端基于FastAPI开发。

## 使用流程

1. 进入目录

```bash
cd backend
```

2. 确保已经安装python

```bash
python --version
```

3. 确保安装pdm管理器

```bash
pdm --version
```

如果没有安装，请执行以下命令安装

```bash
pip install pdm
```

4. 安装依赖

```bash
pdm install
```

5. 启动项目

```bash
pdm run start
```

## 项目结构

```
.
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
```