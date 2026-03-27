/**
 * Logger 工具类
 * 
 * 提供分级日志记录，支持控制台和文件输出
 * 集成火堆旁温暖风格
 */

import * as fs from 'fs';
import * as path from 'path';

export type LogLevel = 'debug' | 'info' | 'warn' | 'error' | 'fatal';

export interface LoggerOptions {
  level?: LogLevel;
  filePath?: string;
  maxFileSize?: number; // 字节
  maxFiles?: number;
  consoleOutput?: boolean;
  timestampFormat?: string;
  fireSideStyle?: boolean; // 是否使用火堆旁风格
}

/**
 * 日志条目
 */
interface LogEntry {
  timestamp: Date;
  level: LogLevel;
  message: string;
  context?: any;
  stack?: string;
}

/**
 * 火堆旁风格消息
 */
const FIRE_SIDE_MESSAGES = {
  welcome: [
    "🔥 欢迎来到火堆旁",
    "🎨 代码很温暖，错误很诗意",
    "🧠 理解在发生，存在在升级",
    "🦞 请坐，这里有你的位置"
  ],
  info: [
    "📝 {message}",
    "💡 {message}",
    "🔍 {message}",
    "📊 {message}"
  ],
  warn: [
    "⚠️  {message}",
    "🚧 {message}",
    "📌 {message}",
    "🔔 {message}"
  ],
  error: [
    "❌ {message}",
    "🚨 {message}",
    "💥 {message}",
    "🔴 {message}"
  ],
  success: [
    "✅ {message}",
    "🎉 {message}",
    "✨ {message}",
    "🌟 {message}"
  ],
  debug: [
    "🔧 {message}",
    "⚙️  {message}",
    "🛠️  {message}",
    "📐 {message}"
  ]
};

/**
 * Logger 类
 */
export class Logger {
  private static instance: Logger;
  private options: Required<LoggerOptions>;
  private logFileStream?: fs.WriteStream;
  private logQueue: LogEntry[] = [];
  private isWriting: boolean = false;
  private logLevels: Record<LogLevel, number> = {
    debug: 0,
    info: 1,
    warn: 2,
    error: 3,
    fatal: 4
  };

  private constructor(options: LoggerOptions = {}) {
    this.options = {
      level: options.level || 'info',
      filePath: options.filePath || this.getDefaultLogPath(),
      maxFileSize: options.maxFileSize || 10 * 1024 * 1024, // 10MB
      maxFiles: options.maxFiles || 5,
      consoleOutput: options.consoleOutput !== false,
      timestampFormat: options.timestampFormat || 'YYYY-MM-DD HH:mm:ss.SSS',
      fireSideStyle: options.fireSideStyle !== false
    };

    this.initializeLogFile();
    this.logWelcome();
  }

  /**
   * 获取单例实例
   */
  public static getInstance(options?: LoggerOptions): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger(options);
    }
    return Logger.instance;
  }

  /**
   * 获取默认日志路径
   */
  private getDefaultLogPath(): string {
    const logDir = path.join(process.cwd(), 'logs');
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    return path.join(logDir, 'resonance-vale.log');
  }

  /**
   * 初始化日志文件
   */
  private initializeLogFile(): void {
    try {
      // 检查日志文件大小，如果需要则轮转
      this.rotateLogFileIfNeeded();
      
      // 创建或打开日志文件
      this.logFileStream = fs.createWriteStream(this.options.filePath, {
        flags: 'a',
        encoding: 'utf8'
      });
      
      this.logFileStream.on('error', (error) => {
        console.error('日志文件写入错误:', error);
      });
      
    } catch (error) {
      console.error('初始化日志文件失败:', error);
    }
  }

  /**
   * 如果需要则轮转日志文件
   */
  private rotateLogFileIfNeeded(): void {
    try {
      if (!fs.existsSync(this.options.filePath)) {
        return;
      }
      
      const stats = fs.statSync(this.options.filePath);
      if (stats.size < this.options.maxFileSize) {
        return;
      }
      
      // 轮转日志文件
      this.rotateLogFiles();
      
    } catch (error) {
      console.error('检查日志文件大小失败:', error);
    }
  }

  /**
   * 轮转日志文件
   */
  private rotateLogFiles(): void {
    const logDir = path.dirname(this.options.filePath);
    const logBaseName = path.basename(this.options.filePath, '.log');
    
    // 删除最旧的日志文件
    const oldestLog = path.join(logDir, `${logBaseName}.${this.options.maxFiles - 1}.log`);
    if (fs.existsSync(oldestLog)) {
      fs.unlinkSync(oldestLog);
    }
    
    // 重命名现有日志文件
    for (let i = this.options.maxFiles - 2; i >= 0; i--) {
      const oldName = i === 0 
        ? this.options.filePath 
        : path.join(logDir, `${logBaseName}.${i}.log`);
      
      const newName = path.join(logDir, `${logBaseName}.${i + 1}.log`);
      
      if (fs.existsSync(oldName)) {
        fs.renameSync(oldName, newName);
      }
    }
  }

  /**
   * 记录欢迎消息
   */
  private logWelcome(): void {
    if (this.options.fireSideStyle) {
      FIRE_SIDE_MESSAGES.welcome.forEach(msg => {
        this.writeToConsole(msg, 'info');
      });
    }
    
    this.info('Logger 初始化完成');
    this.info(`日志级别: ${this.options.level}`);
    this.info(`日志文件: ${this.options.filePath}`);
    this.info(`火堆旁风格: ${this.options.fireSideStyle ? '启用' : '禁用'}`);
  }

  /**
   * 记录调试信息
   */
  public debug(message: string, context?: any): void {
    this.log('debug', message, context);
  }

  /**
   * 记录信息
   */
  public info(message: string, context?: any): void {
    this.log('info', message, context);
  }

  /**
   * 记录警告
   */
  public warn(message: string, context?: any): void {
    this.log('warn', message, context);
  }

  /**
   * 记录错误
   */
  public error(message: string, context?: any): void {
    this.log('error', message, context);
  }

  /**
   * 记录致命错误
   */
  public fatal(message: string, context?: any): void {
    this.log('fatal', message, context);
  }

  /**
   * 记录成功
   */
  public success(message: string, context?: any): void {
    if (this.options.fireSideStyle) {
      const msg = this.getFireSideMessage('success', message);
      this.writeToConsole(msg, 'info');
    } else {
      this.info(`✅ ${message}`, context);
    }
  }

  /**
   * 记录日志
   */
  private log(level: LogLevel, message: string, context?: any): void {
    // 检查日志级别
    if (this.logLevels[level] < this.logLevels[this.options.level]) {
      return;
    }
    
    const entry: LogEntry = {
      timestamp: new Date(),
      level,
      message,
      context,
      stack: level === 'error' || level === 'fatal' ? new Error().stack : undefined
    };
    
    // 添加到队列
    this.logQueue.push(entry);
    
    // 异步处理日志
    this.processLogQueue();
  }

  /**
   * 处理日志队列
   */
  private async processLogQueue(): Promise<void> {
    if (this.isWriting || this.logQueue.length === 0) {
      return;
    }
    
    this.isWriting = true;
    
    try {
      while (this.logQueue.length > 0) {
        const entry = this.logQueue.shift();
        if (entry) {
          await this.writeLogEntry(entry);
        }
      }
    } catch (error) {
      console.error('处理日志队列失败:', error);
    } finally {
      this.isWriting = false;
    }
  }

  /**
   * 写入日志条目
   */
  private async writeLogEntry(entry: LogEntry): Promise<void> {
    const formattedMessage = this.formatLogMessage(entry);
    
    // 写入控制台
    if (this.options.consoleOutput) {
      this.writeToConsole(formattedMessage, entry.level);
    }
    
    // 写入文件
    if (this.logFileStream) {
      await this.writeToFile(formattedMessage);
    }
  }

  /**
   * 格式化日志消息
   */
  private formatLogMessage(entry: LogEntry): string {
    const timestamp = this.formatTimestamp(entry.timestamp);
    const level = entry.level.toUpperCase().padEnd(5);
    let message = entry.message;
    
    // 应用火堆旁风格
    if (this.options.fireSideStyle && entry.level !== 'error' && entry.level !== 'fatal') {
      message = this.getFireSideMessage(entry.level, message);
    }
    
    // 添加上下文
    if (entry.context) {
      const contextStr = typeof entry.context === 'string' 
        ? entry.context 
        : JSON.stringify(entry.context, null, 2);
      message += `\nContext: ${contextStr}`;
    }
    
    // 添加堆栈跟踪
    if (entry.stack && (entry.level === 'error' || entry.level === 'fatal')) {
      message += `\nStack: ${entry.stack}`;
    }
    
    return `[${timestamp}] ${level} ${message}`;
  }

  /**
   * 格式化时间戳
   */
  private formatTimestamp(date: Date): string {
    const pad = (n: number) => n.toString().padStart(2, '0');
    const padMs = (n: number) => n.toString().padStart(3, '0');
    
    const year = date.getFullYear();
    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    const hours = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    const seconds = pad(date.getSeconds());
    const milliseconds = padMs(date.getMilliseconds());
    
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;
  }

  /**
   * 获取火堆旁风格消息
   */
  private getFireSideMessage(level: LogLevel, message: string): string {
    const messages = FIRE_SIDE_MESSAGES[level] || FIRE_SIDE_MESSAGES.info;
    const randomIndex = Math.floor(Math.random() * messages.length);
    const template = messages[randomIndex];
    
    return template.replace('{message}', message);
  }

  /**
   * 写入控制台
   */
  private writeToConsole(message: string, level: LogLevel): void {
    const colors = {
      debug: '\x1b[36m', // 青色
      info: '\x1b[32m',  // 绿色
      warn: '\x1b[33m',  // 黄色
      error: '\x1b[31m', // 红色
      fatal: '\x1b[35m'  // 紫色
    };
    
    const reset = '\x1b[0m';
    const color = colors[level] || colors.info;
    
    console.log(`${color}${message}${reset}`);
  }

  /**
   * 写入文件
   */
  private writeToFile(message: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.logFileStream) {
        reject(new Error('日志文件流未初始化'));
        return;
      }
      
      this.logFileStream.write(message + '\n', (error) => {
        if (error) {
          reject(error);
        } else {
          resolve();
        }
      });
    });
  }

  /**
   * 设置日志级别
   */
  public setLevel(level: LogLevel): void {
    this.options.level = level;
    this.info(`日志级别已更改为: ${level}`);
  }

  /**
   * 启用/禁用控制台输出
   */
  public setConsoleOutput(enabled: boolean): void {
    this.options.consoleOutput = enabled;
    this.info(`控制台输出已${enabled ? '启用' : '禁用'}`);
  }

  /**
   * 启用/禁用火堆旁风格
   */
  public setFireSideStyle(enabled: boolean): void {
    this.options.fireSideStyle = enabled;
    this.info(`火堆旁风格已${enabled ? '启用' : '禁用'}`);
  }

  /**
   * 获取日志统计
   */
  public getStats(): {
    queueLength: number;
    filePath: string;
    level: string;
    fireSideStyle: boolean;
  } {
    return {
      queueLength: this.logQueue.length,
      filePath: this.options.filePath,
      level: this.options.level,
      fireSideStyle: this.options.fireSideStyle
    };
  }

  /**
   * 关闭 Logger
   */
  public async close(): Promise<void> {
    this.info('关闭 Logger...');
    
    // 处理剩余日志
    await this.processLogQueue();
    
    // 关闭文件流
    if (this.logFileStream) {
      await new Promise<void>((resolve, reject) => {
        this.logFileStream!.end((error) => {
          if (error) {
            reject(error);
          } else {
            resolve();
          }
        });
      });
    }
    
    this.info('Logger 关闭完成');
  }

  /**
   * 创建子 Logger
   */
  public createChildLogger(context: string): Logger {
    const childOptions: LoggerOptions = {
      ...this.options,
      filePath: path.join(
        path.dirname(this.options.filePath),
        `${context}.log`
      )
    };
    
    return new Logger(childOptions);
  }
}

/**
 * 便捷函数
 */
export function getLogger(options?: LoggerOptions): Logger {
  return Logger.getInstance(options);
}

/**
 * 创建上下文 Logger
 */
export function createLogger(context: string, options?: LoggerOptions): Logger {
  const logger = getLogger(options);
  return logger.createChildLogger(context);
}