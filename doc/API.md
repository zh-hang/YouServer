# chatroom

## 聊天室列表(finished)

### API

http://124.70.97.253:5000/chatroom/list

### 返回值JSON

| 字段      | 内容       | 备注     |
| --------- | ---------- | -------- |
| room_list | 聊天室列表 | list结构 |

#### room_list字段

| 字段       | 内容           | 备注    |
| ---------- | -------------- | ------- |
| name       | 聊天室名称     |         |
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



## 创建聊天室(to do)

### API

http://124.70.97.253:5000/chatroom/create

### 参数

| 参数名 | 内容       | 备注 |
| ------ | ---------- | ---- |
| name   | 聊天室名字 |      |

### 返回值JSON

| 字段   | 内容               | 备注                   |
| ------ | ------------------ | ---------------------- |
| status | 创建结果           | 1：成功<br />0：失败   |
| name   | 创建的聊天室的名字 | 失败的情况下名称为空串 |

#### 示例

```josn
{
	"status":0,
	"name":"",
}
```

## 聊天(doing)

### 进入和退出聊天室(finished)

进入和退出聊天室的时候需要提前向服务器发送一次请求

#### API

http://124.70.97.253:5000/chatroom/room

#### 参数

| 参数名 | 内容       | 备注                             |
| ------ | ---------- | -------------------------------- |
| name   | 聊天室名称 |                                  |
| status | 进出标识   | 0：退出聊天室<br />1：进入聊天室 |

#### 返回值JSON

| 字段 | 内容   | 备注                                                         |
| ---- | ------ | ------------------------------------------------------------ |
| res  | 返回值 | join chatroom：进入聊天室<br />leave chatroom：离开聊天室<br />invalid room：聊天室对象已消失<br />invalid status：无法识别的状态<br />full room：房间满员 |

#### 示例

```json
{
    "res":"full room"
}
```

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
| user_name | 用户名称   | type为error时可以为空           |
| room_name | 聊天室名称 | type为join,leave和msg时不能为空 |
| msg       | 用户消息   | type为msg时不能为空             |

#### 示例

```json
{
    "type":"",
    "data":{
        "user_name":"",
        "room_name":"",
        "msg":"",
    }
}
```

### 错误信息

| 内容            | 含义                         |
| --------------- | ---------------------------- |
| invalid message | 缺失type或data字段           |
| invalid msg     | 缺失msg字段                  |
| invalid data    | 缺失user_name或room_name字段 |
| illegal data    | user_name或roo_name字段为空  |
| null message    | msg字段为空                  |

### 请求

#### create

##### 示例

```json
{
    "type":"join",
    "data":{
        "user_name":"test",
        "room_name":"TEST",
        "msg":""
    }
}
```

##### 返回值

```json
{
    'type': 'user', 
    'data': {
        'user_name': 'test',
        'room_name': 'TEST',
        'msg': 'create'
    }
}
```

#### join

##### 示例

```json
{
    "type":"join",
    "data":{
        "user_name":"test",
        "room_name":"TEST",
        "msg":""
    }
}
```

##### 返回值

```json
{
    'type': 'user', 
    'data': {
        'user_name': 'test',
        'room_name': 'TEST',
        'msg': 'join'
    }
}
```

#### leave

##### 示例

```json
{
    "type":"leave",
    "data":{
        "user_name":"test",
        "room_name":"TEST",
        "msg":""
    }
}
```

##### 返回值

```json
{
    'type': 'user', 
    'data': {
        'user_name': 'test',
        'room_name': 'TEST',
        'msg': 'leave'
    }
}
```

#### msg

##### 示例

```json
{
    "type":"msg",
    "data":{
        "user_name":"test",
        "room_name":"TEST",
        "msg":"hello"
    }
}
```

##### 返回值

```json
{
    "type":"msg",
    "data":{
        "user_name":"test",
        "room_name":"TEST",
        "msg":"hello"
    }
}
```

