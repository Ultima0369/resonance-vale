/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  
  // 测试文件匹配模式
  testMatch: [
    '**/__tests__/**/*.ts',
    '**/?(*.)+(spec|test).ts'
  ],
  
  // 忽略的测试路径
  testPathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/coverage/'
  ],
  
  // 收集测试覆盖率
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  
  // 覆盖率阈值
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  },
  
  // 覆盖率收集排除
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/**/types/**',
    '!src/**/__tests__/**',
    '!src/**/__mocks__/**'
  ],
  
  // 模块名称映射
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@core/(.*)$': '<rootDir>/src/core/$1',
    '^@prism/(.*)$': '<rootDir>/src/prism-protocol/$1',
    '^@research/(.*)$': '<rootDir>/src/autonomous-research/$1',
    '^@integrations/(.*)$': '<rootDir>/src/integrations/$1',
    '^@skills/(.*)$': '<rootDir>/src/skills/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',
    '^@types/(.*)$': '<rootDir>/src/types/$1'
  },
  
  // 测试前设置
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  
  // 测试运行器
  runner: 'jest-runner',
  
  // 测试超时
  testTimeout: 10000,
  
  // 显示测试位置
  displayName: {
    name: 'Resonance Vale',
    color: 'cyan'
  },
  
  // 测试结果输出
  verbose: true,
  
  // 监听模式配置
  watchPlugins: [
    'jest-watch-typeahead/filename',
    'jest-watch-typeahead/testname'
  ],
  
  // 测试运行器配置
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: 'test-results',
      outputName: 'junit.xml'
    }]
  ]
};