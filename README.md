

# 电商平台招标数据采集工具

#### 介绍

本项目主要用于获取电商平台招标数据，核心功能是解决瑞数（Ruishi）网站的Cookie防护问题。通过模拟浏览器环境获取Cookie，实现对招标数据的自动化采集。

#### 功能特性

- **瑞数Cookie解密**：解决瑞数网站反爬虫的Cookie防护机制
- **自动化数据采集**：自动获取招标公告数据
- **数据持久化**：支持将采集的数据保存为CSV格式
- **请求重试机制**：支持失败自动重试，提高采集成功率
- **代理IP支持**：支持配置代理IP进行请求

#### 项目结构

```
HN-E-Commerce-Platform/
├── browwer.js          # 浏览器环境模拟与Cookie获取
├── main.py             # 主程序入口
├── data_cleaning.py    # 数据清洗模块
└── README.md           # 项目说明文档
```

#### 环境要求

- Python 3.x
- Node.js（用于执行 browwer.js）

#### 安装教程

1. 克隆项目到本地：
   ```bash
   git clone https://gitee.com/liu-changkai/hn-e-commerce-platform.git
   ```

2. 安装Python依赖：
   ```bash
   pip install requests
   pip install lxml
   pip install execjs
   ```

3. 确保已安装Node.js环境

#### 使用说明

1. **配置参数**：在 `main.py` 中修改 `index_url` 、`data_url` 和 `detail_url` 为首页地址、数据地址和详情页地址

2. **运行程序**：
   ```bash
   python main.py
   ```

3. **数据输出**：采集的数据将保存为 `招标公告.csv` 文件

#### 模块说明

- **browwer.js**：负责模拟浏览器环境，获取瑞数Cookie
  - `get_cookie()`：获取防护Cookie

- **main.py**：核心采集逻辑
  - `HN` 类：主采集器
  - `get_data()`：获取指定页数据，支持重试
  - `parse_data()`：解析数据
  - `detail_request()`：详情页获取
  - `save_data()`：保存数据到CSV

- **data_cleaning.py**：数据清洗处理

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

#### 许可证

本项目仅供学习交流使用，请勿用于商业目的。采集数据时请遵守目标网站的使用条款和 robots.txt 规定。