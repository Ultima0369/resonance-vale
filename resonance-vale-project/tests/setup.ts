/**
 * Jest 测试设置文件
 * 
 * 在所有测试运行之前执行
 */

import { Logger } from '../src/utils/logger';

// 设置测试环境变量
process.env.NODE_ENV = 'test';

// 配置测试日志
const testLogger = Logger.getInstance({
  level: 'error', // 测试中只显示错误
  consoleOutput: false, // 不输出到控制台
  fireSideStyle: false // 测试中不使用火堆旁风格
});

// 全局测试超时
jest.setTimeout(10000);

// 测试前的全局设置
beforeAll(() => {
  console.log('🚀 开始运行 Resonance Vale 测试');
  console.log('='.repeat(60));
});

// 测试后的全局清理
afterAll(() => {
  console.log('='.repeat(60));
  console.log('✅ Resonance Vale 测试完成');
});

// 每个测试前的设置
beforeEach(() => {
  // 可以在这里重置测试状态
});

// 每个测试后的清理
afterEach(() => {
  // 可以在这里清理测试资源
});

// 全局测试辅助函数
global.createTestTask = () => ({
  id: `test-task-${Date.now()}`,
  title: '测试研究任务',
  description: '这是一个测试研究任务',
  researchQuestion: '如何测试 Resonance Vale 系统？',
  scope: {
    depth: 'quick' as const,
    breadth: 'narrow' as const,
    timeframe: 'hours' as const
  },
  constraints: {
    maxDuration: 60,
    ethicalConstraints: ['尊重隐私', '透明公开']
  },
  outputRequirements: {
    format: 'executive-summary' as const,
    sections: ['摘要', '方法', '结果', '结论']
  },
  metadata: {
    submittedBy: '测试用户',
    submittedAt: new Date(),
    priority: 'medium' as const,
    tags: ['测试', '验证']
  },
  status: 'pending' as const
});

// 扩展全局类型
declare global {
  namespace NodeJS {
    interface Global {
      createTestTask: () => any;
    }
  }
  
  var createTestTask: () => any;
}

export { testLogger };