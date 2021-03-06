[TOC]

# auth

## user_data

### API

http://124.70.97.253:5000/auth/user_data

### 参数

| 参数      | 内容     | 备注 |
| --------- | -------- | ---- |
| user_name | 用户名称 | 可选 |
| user_tel  | 用户电话 | 可选 |

### 返回值JSON

| 字段 | 内容     | 备注                                                         |
| ---- | -------- | ------------------------------------------------------------ |
| res  | 返回值   | user not exist：用户不存在<br />get user data successfully：获取成功 |
| data | 返回数据 | 用户信息，获取成功时不为空                                   |

#### 示例

```json
{
    "res":"get user data successfully",
    "data":{
        "user_tel":0,
		"user_name":"admin",
        "user_password":"123456",
        "user_avatar_url":""
    }
}
```

## login

### API

http://124.70.97.253:5000/auth/login

### 参数

| 参数          | 内容     | 备注                     |
| ------------- | -------- | ------------------------ |
| user_tel      | 用户电话 |                          |
| user_password | 密码     | 后续再确定密码的加密方式 |

### 返回值JSON

| 字段 | 内容     | 备注                                                         |
| ---- | -------- | ------------------------------------------------------------ |
| res  | 返回值   | user not exist：用户不存在<br />password wrong：密码错误<br />login successfully：登录成功<br />missing parameters：参数缺失 |
| data | 返回数据 | 用户信息，成功登录时不为空                                   |

#### 示例

```json
{
    "res":"login successfully",
    "data":{
        "user_tel":0,
		"user_name":"admin",
        "user_password":"123456",
        "user_avatar_url":""
    }
}
```

## register

### API

http://124.70.97.253:5000/auth/register

### 参数

| 参数名        | 内容     | 备注 |
| ------------- | -------- | ---- |
| user_tel      | 电话号码 |      |
| user_name     | 用户名称 |      |
| user_password | 用户密码 |      |

### 返回值JSON

| 字段 | 内容   | 备注                                                         |
| ---- | ------ | ------------------------------------------------------------ |
| res  | 返回值 | register successfully：注册成功<br />user exist：用户已存在<br />missing parameters：参数缺失 |

#### 示例

```josn
{
	""res"":""register successfully""
}
```

# chatroom

## 聊天室列表

### API

http://124.70.97.253:5000/chatroom/list

### 返回值JSON

| 字段      | 内容       | 备注     |
| --------- | ---------- | -------- |
| room_list | 聊天室列表 | list结构 |

#### room_list字段

| 字段       | 内容           | 备注    |
| ---------- | -------------- | ------- |
| room_name  | 聊天室名称     |         |
| population | 聊天室现有人数 | int类型 |

#### 示例

```json
{
    "rooms":[
        {
            "name":"",
            "population":0
        }
    ]
}
```



## 创建聊天室

### API

http://124.70.97.253:5000/chatroom/create

### 参数

| 参数名    | 内容       | 备注 |
| --------- | ---------- | ---- |
| room_name | 聊天室名字 |      |

### 返回值JSON

| 字段 | 内容     | 备注                                                         |
| ---- | -------- | ------------------------------------------------------------ |
| res  | 创建结果 | chatroom create successfully：成功<br />chatroom already exist：失败<br />missing parameters：参数缺失 |

#### 示例

```josn
{
	"res":"chatroom create successfully"
}
```

## 聊天

### 进入和退出聊天室

### API

ws://124.70.97.253:2333

### 数据包格式JSON

| 字段 | 内容       | 备注                                                         |
| ---- | ---------- | ------------------------------------------------------------ |
| type | 数据包类型 | join：加入聊天室，只能由客户端发出<br />leave：离开聊天室，只能由客户端发出<br />user：用户动态，只能由服务端发出<br />msg：用户消息<br />error：错误消息 |
| data | 数据       | 不能为空                                                     |

#### data字段

| 字段      | 内容       | 备注                            |
| --------- | ---------- | ------------------------------- |
| user      | 用户       | user字段                        |
| room_name | 聊天室名称 | type为join,leave和msg时不能为空 |
| msg       | 用户消息   | type为msg时不能为空             |

##### user字段

| 字段        | 内容     | 备注 |
| ----------- | -------- | ---- |
| user_name   | 用户名称 |      |
| user_avatar | 用户头像 |      |

#### 示例

```json
{
    "type":"",
    "data":{
        "user":{
            "user_name":"",
            "user_avatar":""
        },
        "room_name":"",
        "msg":""
    }
}
```

### 错误信息

| 内容            | 含义                        |
| --------------- | --------------------------- |
| invalid message | 缺失type或data字段          |
| invalid data    | data缺失字段                |
| illegal data    | user_name或roo_name字段为空 |
| null message    | msg字段为空                 |
| room full       | 房间满员                    |
| room not exist  | 房间不存在                  |
| user not exist  | 房间无该用户                |

### 请求

#### create

**示例**

```json
{
    "type":"join",
    "data":{
        "user":{
            "user_name":"test",
            "user_avatar":""
        },
        "room_name":"TEST",
        "msg":""
    }
}
```

**返回值**

```json
{
    "type": "user", 
    "data": {
        "user":{
            "user_name":"test",
            "user_avatar":""
        },
        "room_name": "TEST",
        "msg": "create"
    }
}
```

#### join

**示例**

```json
{
    "type":"join",
    "data":{
        "user":{
            "user_name":"test",
            "user_avatar":""
        },
        "room_name":"TEST",
        "msg":""
    }
}
```

**返回值**

```json
{
    "type": "user", 
    "data": {
        "user":{
            "user_name":"test",
            "user_avatar":""
        },
        "room_name": "TEST",
        "msg": "join"
    }
}
```

#### leave

**示例**

```json
{
    "type":"leave",
    "data":{
        "user":{
            "user_name":"test",
            "user_avatar":""
        },
        "room_name":"TEST",
        "msg":""
    }
}
```

**返回值**

```json
{
    "type": "user", 
    "data": {
        "user":{
            "user_name":"test",
            "user_avatar":""
        },
        "room_name": "TEST",
        "msg": "leave"
    }
}
```

#### msg

**示例**

```json
{
    "type":"msg",
    "data":{
        "user":{
            "user_name":"test",
            "user_avatar":""
        },
        "room_name":"TEST",
        "msg":"hello"
    }
}
```

**返回值**

```json
{
    "type":"msg",
    "data":{
        "user":{
            "user_name":"test",
            "user_avatar":""
        },
        "room_name":"TEST",
        "msg":"hello"
    }
}
```

## 流程

### 获取用户信息

1. 调用API`auth/user_data`查询数据
2. 返回get user data successfully则获取成功

### 注册

1. 调用API`auth/register`注册用户
2. 返回register successfully则注册成功

### 登录

1. 调用API`auth/login`登录
2. 返回login successfully则登录成功

### 创建聊天室

1. 调用API `chatroom/create`创建聊天室资源
2. 返回chatroom create successfully则资源申请成功
3. 使用websockets发送type为join类型的包直接进入聊天室
4. 返回msg “create”则创建成功

### 进入聊天室

3. 使用websockets发送type为join类型的包进入聊天室
4. 返回msg为join则进入成功

### 退出聊天室

1. 使用websockets发送type为leave类型的包进入聊天室
2. 返回msg为leave则进入成功
