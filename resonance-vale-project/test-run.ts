#!/usr/bin/env ts-node

/**
 * Resonance Vale 测试运行脚本
 * 
 * 测试核心组件的功能
 */

import { Logger } from './src/utils/logger';
import { ConfigManager } from './src/utils/config';

// 初始化 Logger
const logger = Logger.getInstance({
  level: 'debug',
  fireSideStyle: true,
  consoleOutput: true
});

async function runTests() {
  logger.info('🚀 开始 Resonance Vale 测试');
  logger.info('='.repeat(60));

  // 测试 1: Logger 功能
  logger.info('测试 1: Logger 功能测试');
  logger.debug('这是一条调试消息');
  logger.info('这是一条信息消息');
  logger.warn('这是一条警告消息');
  logger.error('这是一条错误消息');
  logger.success('这是一条成功消息');
  
  // 测试 2: ConfigManager 功能
  logger.info('测试 2: ConfigManager 功能测试');
  try {
    const configManager = ConfigManager.getInstance();
    const config = configManager.getConfig();
    
    logger.info(`公司名称: ${config.name}`);
    logger.info(`公司使命: ${config.mission}`);
    logger.info(`最大并发研究数: ${config.maxConcurrentResearch}`);
    logger.info(`伦理阈值: ${config.ethicsThreshold}`);
    
    // 测试模块配置
    const prismConfig = configManager.getModuleConfig('prism-protocol');
    logger.info(`棱镜协议配置: ${JSON.stringify(prismConfig, null, 2)}`);
    
  } catch (error) {
    logger.error('配置测试失败:', error);
  }

  // 测试 3: 类型系统
  logger.info('测试 3: 类型系统验证');
  const sampleTask = {
    id: 'test-task-001',
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
  };

  logger.info(`测试任务创建: ${sampleTask.title}`);
  logger.info(`研究问题: ${sampleTask.researchQuestion}`);
  logger.info(`范围: ${sampleTask.scope.depth}深度, ${sampleTask.scope.breadth}广度`);

  // 测试 4: 火堆旁风格
  logger.info('测试 4: 火堆旁风格验证');
  logger.setFireSideStyle(true);
  logger.info('火堆旁风格已启用');
  logger.warn('这是一个温暖的警告');
  logger.success('测试成功完成！');

  // 测试 5: 环境检测
  logger.info('测试 5: 环境检测');
  const configManager = ConfigManager.getInstance();
  logger.info(`开发模式: ${configManager.isDevelopment()}`);
  logger.info(`生产模式: ${configManager.isProduction()}`);
  logger.info(`测试模式: ${configManager.isTest()}`);

  logger.info('='.repeat(60));
  logger.success('所有测试完成！');
  logger.info('🔥 代码很温暖，测试很诗意');
  logger.info('🧠 理解在发生，存在在升级');
  logger.info('🦞 Resonance Vale 测试运行完成');

  // 获取统计信息
  const stats = logger.getStats();
  logger.debug(`日志统计: 队列长度=${stats.queueLength}, 级别=${stats.level}, 火堆旁风格=${stats.fireSideStyle}`);
}

// 运行测试
runTests().catch(error => {
  console.error('测试运行失败:', error);
  process.exit(1);
});