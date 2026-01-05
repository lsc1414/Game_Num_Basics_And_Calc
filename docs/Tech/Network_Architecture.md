# 🌐 网络架构与协议 (Network Architecture)

> **核心理念**: 采用 **双通道架构**。非实时业务 (大厅/养成) 走 HTTP 短连接，实时业务 (战斗/组队) 走 TCP/KCP 长连接。

## 1. 📡 通信架构 (Communication Channels)

### 1.1 HTTP 通道 (Lobby & Meta)
*   **适用场景**: 登录、商城购买、邮件领取、装备强化、天赋升级。
*   **特点**: 无状态、请求-响应模式、易于扩展 (Load Balancer)。
*   **格式**: `POST /api/v1/{service}/{method}`
    *   Body: Protobuf 序列化后的二进制流 (为了省流量和防抓包，不直接用 JSON)。

### 1.2 Socket 通道 (Battle & Social)
*   **适用场景**: 实时PVP、组队副本、聊天、公会战。
*   **协议**: 
    *   **TCP**: 聊天、状态同步 (对顺序要求高)。
    *   **KCP (UDP)**: 战斗位置同步、技能释放 (对延迟敏感，允许少量丢包)。
*   **心跳 (Heartbeat)**: 每 5秒 一次，3次超时断开。

## 2. 📝 协议设计 (Protocol Design)

我们统一使用 **Google Protobuf (v3)** 作为序列化标准。

### 2.1 消息包结构 (Packet Structure)
所有 Socket 消息包遵循以下头部格式：

```cpp
struct PacketHeader {
    uint16_t length;    // 包体长度
    uint16_t msg_id;    // 消息ID (映射到具体 Proto)
    uint32_t seq;       // 序列号 (防重放/乱序)
    uint32_t checksum;  // 校验和 (CRC32)
    // Body follows...
};
```

### 2.2 Protobuf 定义示例
```protobuf
syntax = "proto3";
package Game.Protocol;

// 登录请求 (MsgID: 1001)
message C2S_Login {
    string account = 1;
    string token = 2;
    string device_id = 3;
    int32 client_version = 4;
}

// 登录响应 (MsgID: 1002)
message S2C_Login {
    int32 error_code = 1; // 0 = Success
    int64 server_time = 2;
    UserProfile profile = 3;
}
```

## 3. 🔌 API 接口规范 (API Standards)

### 3.1 幂等性 (Idempotency)
*   对于扣除资源的操作 (如抽卡、购买)，必须支持幂等。
*   **实现**: 客户端生成一个 `request_uuid`，服务器缓存该 ID 的处理结果 5-10 秒。如果收到重复请求，直接返回缓存结果，不重复扣费。

### 3.2 错误处理
*   所有回包包含 `error_code`。
*   **通用错误**:
    *   `1001`: Token 过期 (需重新登录)。
    *   `1002`: 服务器维护中。
    *   `2001`: 资源不足。

## 4. 🛡️ 安全性 (Security)

### 4.1 认证 (Authentication)
*   登录后获取 `SessionToken`。
*   后续所有 HTTP 请求 Header 必须携带 `Authorization: Bearer {token}`。
*   Socket 连接建立后的第一个包必须是 `AuthPacket`。

### 4.2 防重放 (Anti-Replay)
*   利用包头中的 `seq` (序列号)。服务器记录该连接处理过的最大 `seq`，小于等于该值的包直接丢弃。

### 4.3 数据加密
*   虽然 Protobuf 本身不可读，但为了防止逆向，关键业务 (登录/支付) 的 Body 层可再加一层 AES-128 加密。密钥在登录握手时通过 RSA 交换。
