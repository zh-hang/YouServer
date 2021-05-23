# chatroom

## 聊天室列表

api:http://124.70.97.253:5000/chatroom/list

### 返回值

```json
{
    "rooms":[{
        "id":0,
        "name":"test",
        "people_number":0
    }]
}
```

## 进入聊天室

api:http://124.70.97.253:2333

### 参数

| 参数名      | 内容     | 备注                             |
| ----------- | -------- | -------------------------------- |
| chatroom_id | 聊天室id |                                  |
| status      | 进出标识 | 1：进入聊天室<br />2：退出聊天室 |
| user_id     | 用户姓名 |                                  |

### 返回值

- chatroom id wrong：没有该聊天室
- leave chatroom:<current_chatroom_name>：离开聊天室
- something wrong：参数缺失或无法识别
