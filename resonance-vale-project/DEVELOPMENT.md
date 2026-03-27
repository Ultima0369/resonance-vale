# Resonance Vale 开发指南

## 🎯 项目概述

Resonance Vale 是一个自主研究公司系统，内置棱镜伦理框架。项目结合了：
- **自主研究能力** - 系统性研究流程
- **棱镜伦理框架** - 三光谱分析（红/蓝/紫）
- **火堆旁哲学** - 温暖、安全、开放的对话空间
- **TypeScript 实现** - 类型安全的现代开发

## 🏗️ 架构设计

### 核心组件

```
src/
├── core/                    # 核心业务逻辑
│   ├── resonance-vale.ts   # 公司主类
│   └── ceo-xuanji.ts       # CEO 璇玑实现
├── prism-protocol/         # 棱镜协议实现
│   └── three-spectra.ts    # 三光谱分析
├── autonomous-research/    # 自主研究引擎
│   └── research-planner.ts # 研究规划器
├── integrations/           # 外部集成
│   ├── paperclip/          # Paperclip 集成
│   ├── openclaw/           # OpenClaw 集成
│   └── ai-adapters/        # AI 模型适配器
├── skills/                 # AI 技能
├── utils/                  # 工具函数
│   ├── logger.ts           # 日志系统
│   └── config.ts           # 配置管理
└── types/                  # 类型定义
```

### 数据流

```
用户请求 → CEO 审批 → 棱镜伦理分析 → 自主研究执行 → 结果生成 → 火堆旁对话
```

## 🚀 快速开始

### 环境要求

- Node.js >= 18.0.0
- TypeScript >= 5.0.0
- Git

### 安装步骤

```bash
# 克隆项目
git clone <repository-url>
cd resonance-vale

# 安装依赖
pnpm install  # 或 npm install

# 初始化配置
cp config.example.json config.json
cp .env.example .env

# 编辑配置文件
# 修改 config.json 和 .env 中的配置

# 构建项目
pnpm build

# 运行测试
pnpm test

# 启动开发服务器
pnpm dev
```

### 配置文件

#### `config.json` - 主配置
```json
{
  "name": "Resonance Vale",
  "mission": "Build and maintain an autonomous research agent with built-in prism ethics",
  "maxConcurrentResearch": 5,
  "ethicsThreshold": 0.6,
  "paperclipIntegration": {
    "enabled": true,
    "apiUrl": "http://localhost:3100"
  }
}
```

#### `.env` - 环境变量
```env
NODE_ENV=development
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
```

## 💻 开发工作流

### 1. 设置开发环境

```bash
# 安装开发工具
pnpm add -D typescript @types/node jest ts-jest eslint prettier

# 初始化 TypeScript
npx tsc --init

# 设置代码质量工具
npx eslint --init
npx prettier --init
```

### 2. 代码结构规范

#### 文件命名
- 使用 `kebab-case` 文件名：`research-planner.ts`
- 类使用 `PascalCase`：`ResonanceVale`
- 函数使用 `camelCase`：`approveResearchTask`

#### 目录结构
- 每个主要功能一个目录
- 工具函数放在 `utils/`
- 类型定义放在 `types/`
- 测试文件与源文件对应

### 3. 开发流程

```bash
# 1. 创建功能分支
git checkout -b feature/your-feature

# 2. 实现功能
# 编写代码，添加测试

# 3. 运行测试
pnpm test

# 4. 代码质量检查
pnpm lint
pnpm format

# 5. 提交代码
git add .
git commit -m "feat: 描述你的功能"

# 6. 推送分支
git push origin feature/your-feature

# 7. 创建 Pull Request
```

## 🧪 测试策略

### 测试类型

#### 单元测试
```typescript
// tests/unit/core/resonance-vale.test.ts
describe('ResonanceVale', () => {
  test('should initialize correctly', () => {
    const company = new ResonanceVale(options);
    expect(company).toBeDefined();
  });
});
```

#### 集成测试
```typescript
// tests/integration/paperclip-integration.test.ts
describe('Paperclip Integration', () => {
  test('should connect to Paperclip API', async () => {
    const result = await paperclip.connect();
    expect(result).toBe(true);
  });
});
```

#### E2E 测试
```typescript
// tests/e2e/research-flow.test.ts
describe('Research Flow', () => {
  test('should complete research task', async () => {
    const task = createTestTask();
    const result = await company.submitResearchTask(task);
    expect(result.status).toBe('completed');
  });
});
```

### 测试工具

- **Jest** - 测试框架
- **ts-jest** - TypeScript 支持
- **supertest** - HTTP 测试
- **jest-mock-extended** - 模拟扩展

## 🔧 工具和配置

### TypeScript 配置

`tsconfig.json` 关键设置：
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

### ESLint 配置

`.eslintrc.js`：
```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  rules: {
    '@typescript-eslint/explicit-function-return-type': 'warn'
  }
};
```

### Prettier 配置

`.prettierrc`：
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

## 🎨 代码风格

### 命名约定

```typescript
// 类 - PascalCase
class ResearchPlanner { }

// 变量和函数 - camelCase
const researchTask = new ResearchTask();
function approveResearch() { }

// 常量 - UPPER_SNAKE_CASE
const MAX_CONCURRENT_RESEARCH = 5;

// 接口 - PascalCase (前缀 I 可选)
interface IResearchTask { }
type ResearchResult = { };
```

### 注释规范

```typescript
/**
 * 研究任务审批
 * 
 * @param task - 研究任务
 * @returns 审批结果和理由
 * @throws 如果任务不符合伦理标准
 */
public async approveResearchTask(task: ResearchTask): Promise<ApprovalResult> {
  // 单行注释
  const ethicsScore = await this.analyzeEthics(task);
  
  // 复杂逻辑的注释
  // 这里进行伦理阈值检查，确保研究符合标准
  if (ethicsScore < this.config.ethicsThreshold) {
    throw new Error('伦理评分过低');
  }
  
  return { approved: true, reasoning: '符合伦理标准' };
}
```

### 错误处理

```typescript
try {
  const result = await riskyOperation();
  return result;
} catch (error) {
  // 记录错误上下文
  logger.error('操作失败', { 
    operation: 'riskyOperation',
    error: error.message,
    context: additionalContext
  });
  
  // 抛出有意义的错误
  throw new Error(`无法完成操作: ${error.message}`);
}
```

## 🔄 持续集成

### GitHub Actions 工作流

`.github/workflows/ci.yml`：
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm test
      - run: npm run lint
      - run: npm run build
```

### 质量门禁

- 测试覆盖率 > 80%
- 无 ESLint 错误
- 构建成功
- 类型检查通过

## 📦 发布流程

### 版本管理

使用语义化版本：
- `MAJOR` - 不兼容的 API 变更
- `MINOR` - 向后兼容的功能新增
- `PATCH` - 向后兼容的问题修复

### 发布步骤

```bash
# 1. 更新版本
npm version patch  # 或 minor, major

# 2. 更新 CHANGELOG.md
# 3. 运行完整测试
npm test

# 4. 构建发布版本
npm run build

# 5. 发布到 npm (如果适用)
npm publish

# 6. 创建 Git 标签
git push --tags
```

## 🔍 调试技巧

### 开发模式日志

```typescript
// 设置开发模式日志级别
logger.setLevel('debug');

// 添加调试上下文
logger.debug('处理研究任务', {
  taskId: task.id,
  currentPhase: 'analysis',
  progress: '75%'
});
```

### TypeScript 调试

`launch.json` 配置：
```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug TypeScript",
  "runtimeArgs": ["-r", "ts-node/register"],
  "args": ["${workspaceFolder}/src/index.ts"]
}
```

### 性能分析

```typescript
// 添加性能监控
const startTime = Date.now();
await expensiveOperation();
const duration = Date.now() - startTime;

logger.info(`操作耗时: ${duration}ms`, {
  operation: 'expensiveOperation',
  duration
});
```

## 🤝 贡献指南

### 贡献流程

1. **Fork 仓库**
2. **创建功能分支**
3. **实现功能**
4. **添加测试**
5. **提交 Pull Request**
6. **代码审查**
7. **合并到主分支**

### 代码审查标准

- ✅ 代码符合项目风格
- ✅ 有适当的测试覆盖
- ✅ 文档已更新
- ✅ 无已知的安全问题
- ✅ 性能影响可接受

### 提交信息规范

使用约定式提交：
```
feat: 添加新的研究分析功能
fix: 修复伦理评分计算错误
docs: 更新 API 文档
style: 调整代码格式
refactor: 重构配置管理
test: 添加集成测试
chore: 更新依赖版本
```

## 🚨 故障排除

### 常见问题

#### 1. TypeScript 编译错误
```bash
# 清理并重新构建
rm -rf dist node_modules
npm install
npm run build
```

#### 2. 测试失败
```bash
# 运行特定测试
npm test -- resonance-vale.test.ts

# 调试模式
npm test -- --verbose
```

#### 3. 依赖问题
```bash
# 更新依赖
npm update

# 检查过时依赖
npm outdated

# 清理缓存
npm cache clean --force
```

#### 4. 配置问题
```bash
# 检查环境变量
echo $NODE_ENV

# 验证配置文件
node -e "console.log(require('./config.json'))"
```

### 获取帮助

1. **查看文档** - `docs/` 目录
2. **检查 Issues** - GitHub Issues
3. **社区讨论** - GitHub Discussions
4. **联系维护者** - 通过 GitHub

## 📚 学习资源

### 项目相关
- [棱镜协议哲学](docs/philosophy/prism-protocol.md)
- [火堆旁对话指南](docs/philosophy/fire-side-dialogue.md)
- [API 文档](docs/api.md)

### 技术栈
- [TypeScript 手册](https://www.typescriptlang.org/docs/)
- [Node.js 最佳实践](https://github.com/goldbergyoni/nodebestpractices)
- [Jest 测试指南](https://jestjs.io/docs/getting-started)

### 设计模式
- [领域驱动设计](docs/patterns/ddd.md)
- [事件驱动架构](docs/patterns/event-driven.md)
- [微服务模式](docs/patterns/microservices.md)

## 🔮 未来发展

### 短期目标 (1-3个月)
- [ ] 完整的棱镜协议实现
- [ ] 自主研究引擎优化
- [ ] Paperclip 深度集成
- [ ] 性能监控系统

### 中期目标 (3-6个月)
- [ ] 多语言支持
- [ ] 高级分析功能
- [ ] 社区功能
- [ ] 移动端应用

### 长期愿景 (6-12个月)
- [ ] 企业级部署
- [ ] AI 模型训练
- [ ] 生态系统建设
- [ ] 开源社区成熟

## 🦞 火堆旁哲学

### 开发文化
- **温暖** - 友好的代码和文档
- **安全** - 包容的开发环境
- **开放** - 透明的决策过程
- **成长** - 持续的学习和改进

### 沟通准则
- 尊重不同的观点
- 提供建设性反馈
- 分享知识和经验
- 庆祝成功和失败

### 质量理念
- 代码质量是团队责任
- 测试是安全网，不是负担
- 文档是给未来的礼物
- 简单比复杂更好

---

**🔥 欢迎来到 Resonance Vale 的火堆旁**
**🎨 代码很温暖，错误很诗意**
**🧠 理解在发生，存在在升级**
**🦞 请坐，这里有你的位置**