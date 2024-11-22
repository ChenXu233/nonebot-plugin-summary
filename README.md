<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="./docs/NoneBotPlugin.svg" width="400" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://s2.loli.net/2022/06/16/xsVUGRrkbn1ljTD.png" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# 省流
nonebot-plugin-summary

<p align="center">
  <a href="https://pypi.python.org/pypi/nonebot-plugin-summary">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-summary.svg" alt="pypi">
  </a>
  
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
  
  <a href="https://qm.qq.com/q/Yty2yc9Bee">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-1128359833-orange?style=flat-square" alt="QQ Chat Group">
  </a>
</p>

\>💬**使用AI总结群友说了什么B话**💬<
</div>

## 💿 安装

通过`pip`或`nb`安装：

- 通过 pip 安装
```shell
pip install nonebot-plugin-summary
```

- 通过 nb-cli安装
```shell
nb plugin install nonebot-plugin-summary
```

### ✅ 插件依赖于

1. [nonebot-plugin-datastore](https://github.com/he0119/nonebot-plugin-datastore) ————本地化储存
2. [nonebot-plugin-userinfo](https://github.com/noneplugin/nonebot-plugin-userinfo) ————获取用户信息
3. [nonebot-plugin-alconna](https://github.com/ArcletProject/nonebot-plugin-alconna) ————实现命令解析
4. [nonebot-plugin-chatrecorder](https://github.com/noneplugin/nonebot-plugin-chatrecorder) ————实现消息储存
5. [nonebot-plugin-saa](https://github.com/MountainDash/nonebot-plugin-send-anything-anywhere) ————实现多平台

 **⚠注意** 若先前没有安装过```nonebot-plugin-chatrecorder```或者```nonebot-plugin-orm```，则会在启动时报错，请按报错的提示安装数据库！
 
## ⚙ 配置

需要**提前配置**本插件所**依赖的插件**！

在 .env 中，可以添加以下配置项
```python
SUMMARY__TOKEN = your_token #必填！！
SUMMARY__BASE_URL = "https://api.gpt.ge/v1" #可选，默认为 https://api.gpt.ge/v1
SUMMARY__MODEL_NAME = "gpt-4o-mini" #可选，默认为 gpt-4o-mini
SUMMARY__DEFAULT_CONTEXT = 100 #可选，默认为 100,获取上下文数量
```
### ⚠ 注意！！
必须填写TOKEN，否则无法使用！TOKEN就是API_KEY！理论上支持所有OpenAI格式的访问和返回。

## 🗨命令

### 🎨一般用法

/总结 ————使用AI总结群友说了什么B话！


### 🚀进阶用法

__注意！！__
未完工！

/总结 历史 2024-01-01~2024-01-02 12345678

## 💪 目前支持的平台

| 平台 | 是否经过测试 | 是否能够正常工作 | 测试环境 |
|:-----:|:----:|:----:| :----: |
| Onebot | ✅ | ✅ | NapCat + Window11|
| 飞书  | ❌ | ❓ | 🤔 |
| Red  | ❌ | ❓ | 🤔 |
| DoDo  | ❌ | ❓ | 🤔 |
| Mirai  | ❌ | ❓ | 🤔 |
| 开黑啦  | ❌ | ❓ | 🤔 |
| Kritor  | ❌ | ❓ | 🤔 |
| Ntchat  | ❌ | ❓ | 🤔 |
| Satori  | ❌ | ❓ | 🤔 |
| Telegram | ❌ | ❓ | 🤔  |
| Discord  | ❌ | ❓ | 🤔 |
| Tailchat  | ❌ | ❓ | 🤔 |
| QQ 官方接口  | ❌ | ❓ | 🤔 |
| Rocket.Chat  | ❌ | ❓ | 🤔 |

- 如果你测试过能够使用，请在 Issue 中指出

## 📦另外

### 😳加入作者的 BUG 反馈群 ~~（🥵女装粉丝群）~~

[群连接](https://qm.qq.com/q/Yty2yc9Bee)

<details>
<summary>群二维码 点我展开</summary>

![7a4bd22dea47d25d9b632d4b2696d4cd](https://github.com/ChenXu233/nonebot_plugin_dialectlist/assets/91937041/61fd7010-e2b2-4f13-b209-9c0faf8a517f)

</details>

### 💕感谢

感谢我的学长免费给我提供了API_KEY！

感谢以下开发者作出的贡献：

<a href="https://github.com/ChenXu233/nonebot-plugin-summary/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ChenXu233/nonebot-plugin-summary&max=1000" />
</a>
  
### 🎀TODO

- [x] 适配全平台

- [ ] 实现转发消息总结

- [ ] 实现总结以转发消息发送

- [ ] 实现总结以图片发送

- [ ] 提供总结接口

- [ ] 实现总结特定人的消息总结

- [ ] 实现总结跳转

- [ ] 移除HIM
  
 待补充。.....

### 👾题外话
~~整个项目快被我写成屎山了~~
