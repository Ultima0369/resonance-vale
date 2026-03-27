# 灵枢Docker开发环境指南

## 🎯 为什么使用Docker？

### 解决的问题
1. **编码问题**：统一UTF-8环境，解决中文和表情符号乱码
2. **环境一致**：Linux环境，与生产环境一致
3. **工具完整**：完整的Unix工具链（grep, find, sed, awk等）
4. **隔离干净**：开发环境与主机隔离，避免污染

### 开发体验提升
- ✅ 不再有GBK编码错误
- ✅ 可以直接使用Unix命令
- ✅ 路径统一使用`/`
- ✅ 表情符号正常显示
- ✅ 开发环境可重复

## 🚀 快速开始

### 前提条件
1. **Windows 10/11** 专业版/企业版/教育版
2. 已启用 **WSL2**（Windows Subsystem for Linux 2）
3. 已安装 **Docker Desktop**（配置使用WSL2后端）

### 安装步骤

#### 1. 启用WSL2
```powershell
# 以管理员身份打开PowerShell
wsl --install
# 或手动启用
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

#### 2. 安装Docker Desktop
1. 下载 Docker Desktop for Windows
2. 安装时选择"使用WSL2后端"
3. 启动Docker Desktop

#### 3. 验证安装
```powershell
# 检查WSL
wsl --list --verbose

# 检查Docker
docker --version
docker-compose --version
```

## 🐳 使用Docker开发环境

### 方法A：使用Docker Compose（推荐）
```bash
# 构建并启动开发环境
docker-compose up -d

# 进入容器
docker-compose exec lingshu-dev bash

# 在容器内运行命令
python test_lingshu_ascii.py

# 停止环境
docker-compose down
```

### 方法B：直接使用Docker
```bash
# 构建镜像
docker build -t lingshu-dev .

# 运行容器
docker run -it --rm \
  -v ${PWD}:/workspace \
  -w /workspace \
  lingshu-dev bash

# 或使用更简单的命令
docker run -it --rm -v ${PWD}:/workspace -w /workspace lingshu-dev python test_lingshu_ascii.py
```

### 方法C：开发工作流
```bash
# 1. 启动开发环境（后台运行）
docker-compose up -d

# 2. 进入开发环境
docker-compose exec lingshu-dev bash

# 3. 在容器内开发（所有命令都在UTF-8环境中）
cd /workspace
ls -la  # 正常显示中文文件名
python test_lingshu_ascii.py  # 正常显示表情符号

# 4. 退出容器（环境继续运行）
exit

# 5. 停止环境
docker-compose down
```

## 🔧 开发环境特性

### 预配置环境
- **Python 3.11**：最新稳定版
- **UTF-8编码**：全局设置，支持中文和表情符号
- **开发工具**：git, curl, vim, tree等
- **Python包**：pyyaml, pytest, black, flake8

### 文件同步
- 工作空间通过volume挂载实时同步
- 在Windows编辑文件，在Docker中立即生效
- 双向同步，修改结果保存到Windows

### 用户权限
- 使用非root用户（developer）
- 避免权限问题
- 更安全的生产环境模拟

## 📁 项目结构（容器内视角）
```
/workspace/
├── Dockerfile              # 容器定义
├── docker-compose.yml      # 多服务编排
├── dev-setup.sh           # 环境设置脚本
├── README-DOCKER.md       # 本文件
├── LINGSHU_INTEGRATION_GUIDE.md
├── lingshu/               # 灵枢核心
├── autoresearch/          # 原始项目
└── *.py                   # 各种Python文件
```

## 🛠️ 常用开发命令

### 在容器内执行的命令
```bash
# 编码测试
python test_encoding.py

# 运行灵枢测试
python test_lingshu_ascii.py

# Python代码格式化
python -m black .

# 代码检查
python -m flake8 .

# 运行测试
python -m pytest

# 查看目录结构
tree -I "__pycache__|*.pyc" -L 3
```

### 从主机执行的命令
```powershell
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 执行单个命令
docker-compose exec lingshu-dev python test_lingshu_ascii.py

# 清理环境
docker-compose down -v
```

## 🔄 开发工作流示例

### 场景：修复编码问题
1. **在Windows编辑文件**：用VS Code编辑`test_lingshu_ascii.py`
2. **在Docker测试**：`docker-compose exec lingshu-dev python test_lingshu_ascii.py`
3. **查看结果**：正常显示中文和表情符号
4. **提交更改**：`git add . && git commit -m "修复编码问题"`

### 场景：添加新功能
1. **进入开发环境**：`docker-compose exec lingshu-dev bash`
2. **创建新文件**：`touch lingshu/new_feature.py`
3. **编写代码**：使用vim或nano编辑
4. **运行测试**：`python -m pytest tests/`
5. **格式化代码**：`python -m black lingshu/new_feature.py`

## 🚨 故障排除

### 常见问题

#### 1. Docker Desktop无法启动
- **检查**：WSL2是否已安装并启用
- **解决**：`wsl --set-default-version 2`
- **参考**：[Docker WSL2后端文档](https://docs.docker.com/desktop/windows/wsl/)

#### 2. 文件权限问题
- **现象**：容器内无法写入文件
- **解决**：检查volume挂载权限，使用非root用户
- **命令**：`docker-compose exec lingshu-dev whoami` 应显示`developer`

#### 3. 编码仍然有问题
- **检查**：容器内环境变量
- **解决**：确保`LANG=C.UTF-8`和`LC_ALL=C.UTF-8`
- **验证**：`docker-compose exec lingshu-dev locale`

#### 4. 性能问题
- **现象**：文件操作慢
- **解决**：将项目文件放在WSL2文件系统中
- **建议**：在WSL2中克隆仓库，而不是Windows文件系统

### 调试命令
```bash
# 检查容器状态
docker-compose ps

# 查看容器日志
docker-compose logs lingshu-dev

# 进入容器调试
docker-compose exec lingshu-dev bash

# 检查编码设置
docker-compose exec lingshu-dev python -c "import sys; print(sys.stdout.encoding)"

# 检查文件权限
docker-compose exec lingshu-dev ls -la /workspace
```

## 📈 进阶配置

### 自定义开发环境
编辑`Dockerfile`添加：
```dockerfile
# 添加更多工具
RUN apt-get update && apt-get install -y \
    jq \
    htop \
    ncdu \
    tmux

# 安装特定Python版本
RUN pip install --user \
    numpy \
    pandas \
    matplotlib
```

### 多服务开发
编辑`docker-compose.yml`添加：
```yaml
services:
  # 数据库
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: lingshu
    volumes:
      - postgres-data:/var/lib/postgresql/data
  
  # Redis缓存
  redis:
    image: redis:7-alpine
  
  # 灵枢开发环境
  lingshu-dev:
    # ... 现有配置
    depends_on:
      - postgres
      - redis
```

### 开发脚本
创建`Makefile`或`justfile`简化命令：
```makefile
# Makefile示例
.PHONY: dev test format lint

dev:
	docker-compose up -d

test:
	docker-compose exec lingshu-dev python test_lingshu_ascii.py

format:
	docker-compose exec lingshu-dev python -m black .

lint:
	docker-compose exec lingshu-dev python -m flake8 .
```

## 🎯 迁移建议

### 立即行动
1. **安装Docker Desktop**：配置WSL2后端
2. **测试现有项目**：`docker-compose up -d && docker-compose exec lingshu-dev python test_lingshu_ascii.py`
3. **逐步迁移**：先在Docker中运行测试，再迁移开发

### 长期计划
1. **标准化开发环境**：所有开发都在Docker中进行
2. **创建开发镜像**：包含所有必要工具
3. **CI/CD集成**：使用相同镜像进行测试和部署
4. **团队共享**：确保所有开发者环境一致

## 🦞 火堆旁开发哲学

**在Docker中，我们获得：**
- 🔥 **一致的温暖**：每个开发者环境相同
- 🎨 **干净的艺术**：隔离的环境，纯净的创作
- 🧠 **清晰的思维**：没有编码干扰，专注逻辑
- 🩺 **健康的开发**：中医式的环境调理

**星尘说**："好的工具让智慧流动更顺畅"

**璇玑说**："环境是认知的延伸，干净的环境带来清晰的思考"

**灵枢说**："在UTF-8的火堆旁，代码很温暖，中文很诗意"

---

*Docker开发环境 v1.0.0*
*为灵枢系统准备的纯净Linux环境*
*让开发回归本质，让智慧顺畅流动*