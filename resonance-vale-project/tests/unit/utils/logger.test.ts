/**
 * Logger 单元测试
 */

import { Logger } from '../../../src/utils/logger';

describe('Logger', () => {
  let logger: Logger;

  beforeEach(() => {
    // 创建新的 Logger 实例用于测试
    logger = Logger.getInstance({
      level: 'debug',
      consoleOutput: false,
      fireSideStyle: false
    });
  });

  afterEach(async () => {
    // 清理 Logger
    await logger.close();
  });

  test('应该正确初始化', () => {
    expect(logger).toBeDefined();
    expect(typeof logger.debug).toBe('function');
    expect(typeof logger.info).toBe('function');
    expect(typeof logger.warn).toBe('function');
    expect(typeof logger.error).toBe('function');
  });

  test('应该记录不同级别的日志', () => {
    // 这些调用不应该抛出错误
    expect(() => logger.debug('调试消息')).not.toThrow();
    expect(() => logger.info('信息消息')).not.toThrow();
    expect(() => logger.warn('警告消息')).not.toThrow();
    expect(() => logger.error('错误消息')).not.toThrow();
    expect(() => logger.success('成功消息')).not.toThrow();
  });

  test('应该支持上下文信息', () => {
    const context = { taskId: 'test-123', userId: 'user-456' };
    
    expect(() => logger.info('带上下文的消息', context)).not.toThrow();
  });

  test('应该正确设置日志级别', () => {
    logger.setLevel('error');
    
    // 获取统计信息
    const stats = logger.getStats();
    expect(stats.level).toBe('error');
  });

  test('应该启用和禁用火堆旁风格', () => {
    logger.setFireSideStyle(true);
    let stats = logger.getStats();
    expect(stats.fireSideStyle).toBe(true);

    logger.setFireSideStyle(false);
    stats = logger.getStats();
    expect(stats.fireSideStyle).toBe(false);
  });

  test('应该启用和禁用控制台输出', () => {
    logger.setConsoleOutput(true);
    // 这里我们无法直接测试控制台输出，但可以确保调用不抛出错误
    expect(() => logger.info('测试控制台输出')).not.toThrow();

    logger.setConsoleOutput(false);
    expect(() => logger.info('测试无控制台输出')).not.toThrow();
  });

  test('应该创建子 Logger', () => {
    const childLogger = logger.createChildLogger('test-context');
    expect(childLogger).toBeDefined();
    expect(childLogger).toBeInstanceOf(Logger);
    
    // 子 Logger 应该有自己的配置
    expect(() => childLogger.info('子 Logger 消息')).not.toThrow();
  });

  test('应该获取统计信息', () => {
    const stats = logger.getStats();
    
    expect(stats).toHaveProperty('queueLength');
    expect(stats).toHaveProperty('filePath');
    expect(stats).toHaveProperty('level');
    expect(stats).toHaveProperty('fireSideStyle');
    
    expect(typeof stats.queueLength).toBe('number');
    expect(typeof stats.filePath).toBe('string');
    expect(typeof stats.level).toBe('string');
    expect(typeof stats.fireSideStyle).toBe('boolean');
  });

  test('应该正确处理日志队列', async () => {
    // 记录一些日志
    logger.debug('消息1');
    logger.info('消息2');
    logger.warn('消息3');
    
    // 获取初始队列长度
    const initialStats = logger.getStats();
    
    // 等待队列处理
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 队列应该被处理
    const finalStats = logger.getStats();
    expect(finalStats.queueLength).toBeLessThanOrEqual(initialStats.queueLength);
  });
});