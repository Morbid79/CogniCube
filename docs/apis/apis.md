# 情绪立方后端API文档

---

## 用户认证模块

### 用户注册
**请求方式**: POST  
**路径**: `/api/v1/auth/register`

| 参数        | 类型   | 必填 | 描述                         |
|-------------|--------|------|------------------------------|
| username    | string | 是   | 3-20个字符的合法用户名       |
| password    | string | 是   | 6+字符，需包含字母和数字组合 |

**返回参数**:
| 参数        | 类型   | 描述                 |
|-------------|--------|----------------------|
| user_id     | string | 系统生成的用户唯一ID |

**示例请求**:
```json
{
  "username": "user1",
  "password": "Passw0rd123"
}
```

### 用户登录

**请求方式**: POST  
**路径**: `/api/v1/auth/login`

|参数|类型|必填|描述|
|---|---|---|---|
|username|string|是|注册用户名|
|password|string|是|账户密码|

**返回参数**:

|参数|类型|描述|
|---|---|---|
|user_id|string|用户唯一标识符|
|access_token|string|有效期一天的JWT访问令牌|
**示例请求**:
```json
{
  "username": "user1",
  "password": "Passw0rd123"
}
```

### Token刷新

**请求方式**: POST  
**路径**: `/api/v1/auth/refresh`

|参数|类型|必填|描述|
|---|---|---|---|
|access_token|string|是|有效的JWT访问令牌|

**返回参数**:

|参数|类型|描述|
|---|---|---|
|access_token|string|新生成的JWT访问令牌
## AI对话系统模块

### 发送对话消息

**请求方式**: POST  
**路径**: `/api/v1/ai/conversation`

|参数|类型|必填|描述|
|---|---|---|---|
|user_id|string|是|用户唯一标识符|
|message|string|是|1-500字符的对话内容|

**返

|参数|类型|描述|
|---|---|---|
|reply|string|AI生成的回复内容|

### 获取对话历史

**请求方式**: GET  
**路径**: `/api/v1/ai/history/`

**路径参数**:

|参数|类型|必填|描述|
|---|---|---|---|
|token|string|是|用户的JWT访问令牌|

**查询参数**:

|参数|类型|必填|描述|
|---|---|---|---|
|start_time|int|是|起始时间戳（包含）|
|end_time|int|是|结束时间戳（包含）|

**返回参数**:

|参数|类型|描述|
|---|---|---|
|history|array|包含历史对话对象的数组|
|∟ message|string|原始消息内容|
|∟∟ timestamp|int|消息时间戳（精确到秒）|