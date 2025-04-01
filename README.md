# astrbot_plugin_QQProfile

## 介绍

利用napcat提供的接口配置QQ机器人的头像、昵称、签名、状态，查看点赞列表、清除未读等等

## 📦 安装

```bash
# 克隆仓库到插件目录
cd /AstrBot/data/plugins
git clone https://github.com/Zhalslar/astrbot_plugin_QQProfile

# 控制台重启AstrBot
```


## ⚙️ 配置
 
请在astrbot面板配置，插件管理 -> astrbot_plugin_QQProfile -> 操作 -> 插件配置


## 🐔 使用说明
### 指令表
|     指令     |             说明              |
|:----------:|:---------------------------:|
| [引用图片]设置头像 |        将引用的这张图片设置为头像        |
|  设置昵称 XXX  |        将Bot的昵称改为XXX         |
|  设置签名 XXX  | 将Bot的签名改为XXX，并同步空间（可在QQ里关掉） |
|  设置状态 XXX  |     设置Bot的在线状态（如“我的电量”）     |
|    点赞列表    |          查看谁赞了Bot           |
|    清除未读    |        将所有未读消息标记为已读         |

## 📌 注意事项
目前仅测试了napcat，其他Onebot协议端可能也能用，但可能部分接口用不了


## TODO
- 提供更多配置项
- 测试更多环境下的部署

## 📜 开源协议
本项目采用 [MIT License](LICENSE)

