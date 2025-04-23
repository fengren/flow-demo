### Fastapi + Prefect + Business-rule Demo

当前项目演示如何通过Fastapi接口，动态添加规则，通过business-rule对数据和规则进行比对后，使用prefect flow的方式进行执行。
并可以通过prefect提供的UI查看任务信息

1. 安装依赖

```shell
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

2. 初始化db

```shell
python app/init_db.py
```

3. 启动API服务

```shell
python app/main.py
```

4. 启动prefect dashboard

```shell
 prefect server start
```

4.1 启动rule_check的Deployment

```shell
 PREFECT_API_URL=http://127.0.0.1:4200/api python app/flows/rule_checker.py
 ```

4.2 启动update_ad_config的Deployment

```shell
 PREFECT_API_URL=http://127.0.0.1:4200/api python app/flows/update_ad_config.py
```

5. 添加测试数据

使用Postman 请求
POST /tasks 接口

#### case 1

```json
{
  "name": "test1",
  "rules": [
    {
      "conditions": {
        "all": [
          {
            "name": "daily_consume",
            "operator": "less_than",
            "value": 110
          },
          {
            "name": "balance",
            "operator": "greater_than",
            "value": 20
          },
          {
            "name": "roi",
            "operator": "greater_than",
            "value": 1
          }
        ]
      },
      "actions": [
        {
          "name": "update_ad_config"
        }
      ]
    }
  ]
}

```

#### case 2

```json

{
  "name": "test2",
  "rules": [
    {
      "conditions": {
        "any": [
          {
            "name": "daily_consume",
            "operator": "less_than",
            "value": 110
          },
          {
            "name": "balance",
            "operator": "greater_than",
            "value": 20
          },
          {
            "name": "roi",
            "operator": "greater_than",
            "value": 1
          }
        ]
      },
      "actions": [
        {
          "name": "update_ad_config"
        }
      ]
    }
  ]
}


```

#### case 3

```json
{
  "name": "test3",
  "rules": [
    {
      "conditions": {
        "any": [
          {
            "name": "daily_consume",
            "operator": "less_than",
            "value": 110
          },
          {
            "name": "balance",
            "operator": "greater_than",
            "value": 20
          },
          {
            "name": "roi",
            "operator": "greater_than",
            "value": 1
          }
        ]
      },
      "actions": [
        {
          "name": "update_ad_config"
        }
      ]
    }
  ]
}

```
