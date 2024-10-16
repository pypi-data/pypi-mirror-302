<div align="center">
<img src="https://raw.githubusercontent.com/leiyi2000/amock/main/docs/logo.png" style="width:200px; height:200px;"/>
</div>

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/leiyi2000/amock/publish.yml)


# aimock

借助AI自动生成测试数据

## 快速开始
```python
from mock import MockModel, Field

class User(MockModel):
    name: str = Field(description="用户名")
    age: int = Field(description="年龄")
    email: str = Field(description="邮箱")
    phone: str = Field(description="电话")

api_key = "xxx"
base_url = "xxx"
MockModel.init(api_key, base_url, model="gpt-3.5-turbo")
print(User.create())
```