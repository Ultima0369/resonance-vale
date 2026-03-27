# 灵枢Linux环境快速开始指南

## 🚀 一键启动命令

### 1. 验证环境（最简单）
```powershell
# 在PowerShell中运行
docker run --rm -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh -c "echo '🎉 Linux环境就绪' && cd autoresearch && python test_lingshu_ascii.py"
```

### 2. 交互式开发（推荐）
```powershell
# 进入Linux Shell
docker run -it --rm -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh
```

### 3. 使用开发脚本
```powershell
# 运行交互式菜单
.\dev-linux.ps1
```

## 📁 在Linux环境中的操作

### 进入Linux Shell后：
```bash
# 1. 查看工作空间
pwd
ls -la

# 2. 进入灵枢项目
cd autoresearch

# 3. 运行测试
python test_lingshu_ascii.py

# 4. 查看灵枢代码
cat lingshu/lingshu_ethics.py | head -30

# 5. 创建新文件
touch lingshu/new_feature.py

# 6. 编辑文件（使用vim或nano）
vim lingshu/new_feature.py

# 7. 退出Shell
exit
```

### 常用Linux命令：
```bash
# 文件操作
ls -la          # 详细列表
cat file.py     # 查看文件
head -20 file   # 查看前20行
tail -f log.txt # 实时查看日志

# 搜索
find . -name "*.py"          # 查找Python文件
grep "class" *.py           # 搜索文本
find . -type f -size +1M    # 查找大文件

# 进程管理
ps aux                       # 查看进程
top                          # 系统监控

# 网络
curl https://example.com     # HTTP请求
ping google.com              # 网络测试
```

## 🛠️ 开发工作流

### 场景1: 修改灵枢代码
1. **在Windows编辑**：用VS Code编辑`autoresearch/lingshu_ethics.py`
2. **在Linux测试**：
   ```powershell
   docker run --rm -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh -c "cd autoresearch && python test_lingshu_ascii.py"
   ```
3. **查看结果**：测试输出

### 场景2: 添加新功能
1. **进入Linux环境**：
   ```powershell
   docker run -it --rm -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh
   ```
2. **在Linux中开发**：
   ```bash
   cd autoresearch
   vim lingshu/new_feature.py
   python -c "import sys; print('测试新功能')"
   ```
3. **保存退出**：`exit`

### 场景3: 批量操作
```powershell
# 运行所有Python文件检查
docker run --rm -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh -c "
  cd autoresearch
  echo '📊 Python文件统计:'
  find . -name '*.py' | wc -l
  echo ''
  echo '🧪 运行所有测试:'
  python test_lingshu_ascii.py
"
```

## 🔧 故障排除

### 常见问题：

#### 1. Docker命令失败
```powershell
# 检查Docker状态
docker --version
docker ps

# 重启Docker Desktop
# 1. 右键系统托盘Docker图标
# 2. 选择"Restart"
```

#### 2. 文件权限问题
```powershell
# 检查文件权限
docker run --rm -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh -c "ls -la /workspace"
```

#### 3. 编码问题
```powershell
# 测试编码
docker run --rm python:3.11-alpine python -c "print('✅ 中文测试 🎉')"
```

#### 4. 路径问题
```powershell
# 使用绝对路径
docker run --rm -v "C:\Users\lgdln\.openclaw\workspace:/workspace" -w /workspace python:3.11-alpine sh -c "pwd"
```

## 📈 进阶操作

### 持久化开发容器
```powershell
# 创建并进入命名容器
docker run -it --name lingshu-dev -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh

# 后续进入（容器保持运行）
docker exec -it lingshu-dev sh

# 停止容器
docker stop lingshu-dev

# 删除容器
docker rm lingshu-dev
```

### 安装额外工具
```powershell
# 创建自定义镜像
docker run -it --rm -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh -c "
  apk add --no-cache vim git curl tree
  echo '✅ 工具安装完成'
  vim --version
"
```

### 数据持久化
```powershell
# 创建数据卷
docker volume create lingshu-data

# 使用数据卷
docker run -it --rm -v lingshu-data:/data -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh
```

## 🎯 最佳实践

### 1. **保持容器轻量**
- 使用`python:3.11-alpine`小镜像
- 按需安装工具
- 及时清理临时容器

### 2. **文件同步**
- 开发文件放在挂载卷中
- 大型数据使用数据卷
- 配置文件版本控制

### 3. **开发流程**
- 在Windows编辑，在Linux测试
- 使用Git进行版本控制
- 定期提交代码

### 4. **环境一致性**
- 使用相同的基础镜像
- 记录依赖版本
- 创建Dockerfile标准化环境

## 🦞 火堆旁开发哲学

### 温暖开发
```bash
# 在Linux中感受温暖
echo '🔥 火堆旁，代码很温暖'
echo '🦞 灵枢在Linux中呼吸'
echo '🎯 星尘的方向很清晰'
```

### 渐进改进
1. **先让代码运行**：最简单的Docker命令
2. **再优化环境**：添加工具和配置
3. **最后标准化**：创建完整开发环境

### 工具服务于目标
- Docker是手段，灵枢开发是目标
- Linux环境是画布，中医伦理是艺术
- 火堆旁是空间，智慧流动是本质

---

**开始命令：**
```powershell
cd C:\Users\lgdln\.openclaw\workspace
.\dev-linux.ps1
```

**或直接：**
```powershell
docker run -it --rm -v ${PWD}:/workspace -w /workspace python:3.11-alpine sh
```

**火堆旁，Linux很温暖。** 🔥🐳