# 🐍 Gerrit MCP Server

[![PyPI version](https://badge.fury.io/py/gerrit-mcp-server.svg)](https://pypi.org/project/gerrit-mcp-server/)
[![Python Version](https://img.shields.io/pypi/pyversions/gerrit-mcp-server)](https://pypi.org/project/gerrit-mcp-server/)
[![License](https://img.shields.io/pypi/l/gerrit-mcp-server)](https://github.com/iceleaf916/gerrit-mcp-server)

一个用于与 Gerrit 代码审查系统交互的 MCP（Model Context Protocol）服务器。该服务器允许语言模型（如 Gemini）通过执行针对 Gerrit REST API 的 `curl` 命令来查询变更、检索详细信息和管理评审。

该服务器可以作为持久的 **HTTP 服务器**运行，也可以通过 **STDIO**按需运行。

## 📚 文档

有关详细信息，请参阅 `docs/` 目录中的文档：

*   **[配置文档](docs/configuration.md)**：`gerrit_config.json` 文件详细指南以及所有认证方式。
*   **[测试指南](docs/testing.md)**：如何运行单元测试、集成测试和 E2E 测试的说明。
*   **[Gemini CLI 设置](docs/gemini-cli.md)**：如何配置 Gemini CLI 以使用此服务器。
*   **[最佳实践](docs/best_practices.md)**：有效使用服务器的技巧。
*   **[贡献指南](docs/contributing.md)**：为项目做贡献的指南。
*   **[可用工具](docs/available_tools.md)**：所有可用工具及其描述的列表。
*   **[用例示例](docs/use_cases.md)**：演示如何使用服务器的场景。

## 🚀 快速开始

### 从 PyPI 安装（推荐）

对于快速使用，可以直接从 PyPI 安装：

```bash
# 通过 uvx 直接运行（无需安装）
uvx gerrit-mcp-server stdio

# 或安装后使用
uv pip install gerrit-mcp-server
gerrit-mcp-server stdio

# 指定端口运行 HTTP 服务器
gerrit-mcp-server --host localhost --port 6322
```

### 配置服务器

#### 方法 1：全局配置（推荐）

创建个人配置文件，所有项目通用：

```bash
# 创建配置目录
mkdir -p ~/.config

# 复制配置模板
# 如果是源码安装：
cp gerrit_mcp_server/gerrit_config.sample.json ~/.config/gerrit_config.json

# 如果是 PyPI 安装，手动创建 ~/.config/gerrit_config.json
vim ~/.config/gerrit_config.json
```

将以下内容保存到配置文件中，并根据实际情况修改：

```json
{
  "default_gerrit_base_url": "https://your-gerrit.com/",
  "gerrit_hosts": [
    {
      "name": "My Gerrit",
      "external_url": "https://your-gerrit.com/",
      "authentication": {
        "type": "http_basic",
        "username": "your-username",
        "auth_token": "your-http-password"
      }
    }
  ]
}
```

**配置说明**：
- 将 `your-username` 替换为你的 Gerrit 用户名
- 将 `your-http-password` 替换为你的 Gerrit HTTP 密码（在 Gerrit 设置 → HTTP Password 中生成）
- 将 `https://your-gerrit.com/` 替换为你的 Gerrit 服务器地址

配置完成后即可直接运行：

```bash
gerrit-mcp-server stdio
```

#### 方法 2：项目配置

在项目根目录创建 `gerrit_config.json`：

```bash
cp gerrit_mcp_server/gerrit_config.sample.json ./gerrit_config.json
vim ./gerrit_config.json
```

#### 方法 3：临时配置

使用命令行参数指定配置文件：

```bash
gerrit-mcp-server --config /path/to/your/config.json stdio
```

**💡 提示**：查看 [配置文档](docs/configuration.md) 了解所有认证方式和高级配置选项。

---

### 从源码安装

如果要从源码安装，请按以下步骤操作：

#### 1. 前置条件

在开始之前，请确保已在系统的 `PATH` 中安装并可以使用以下工具：

*   **Python 3.11+**：构建脚本需要使用现代版本的 Python。
*   **curl**：用于通过 URL 传输数据的标准命令行工具。

#### 2. 构建环境

从 `gerrit-mcp-server` 项目根目录运行构建脚本。这将创建 Python 虚拟环境，安装所有依赖项，并使服务器准备好运行。

```bash
./build-gerrit.sh
```

#### 3. 配置服务器

你需要在 `gerrit_mcp_server` 目录内创建一个 `gerrit_config.json` 文件。复制提供的示例文件 `gerrit_mcp_server/gerrit_config.sample.json` 并根据你的环境进行自定义。有关所有可用选项的详细信息，请参阅 **[配置文档](docs/configuration.md)**。

```bash
cp gerrit_mcp_server/gerrit_config.sample.json gerrit_mcp_server/gerrit_config.json
```

#### 4. 运行服务器（HTTP 模式）

要将服务器作为持久的后台进程运行，请使用 `server.sh` 脚本：

*   **启动服务器：**
    ```bash
    ./server.sh start
    ```
*   **检查状态：**
    ```bash
    ./server.sh status
    ```
*   **停止服务器：**
    ```bash
    ./server.sh stop
    ```

对于按需 STDIO 模式，请参阅 **[Gemini CLI 设置指南](docs/gemini-cli.md)**。

---

### 安全声明

这不是 Google 官方支持的产品。本项目不符合 [Google 开源软件漏洞奖励计划](https://bughunters.google.com/open-source-security) 的资格。
