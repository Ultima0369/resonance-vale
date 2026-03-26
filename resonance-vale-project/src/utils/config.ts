/**
 * Configuration utilities for Resonance Vale
 */

import * as fs from 'fs';
import * as path from 'path';
import { CompanyConfig } from '../types';
import { Logger } from './logger';

/**
 * Configuration manager
 */
export class ConfigManager {
  private static instance: ConfigManager;
  private config: CompanyConfig;
  private logger: Logger;
  private configPath: string;

  private constructor() {
    this.logger = Logger.getInstance();
    this.configPath = this.getConfigPath();
    this.config = this.loadConfig();
  }

  /**
   * Get singleton instance
   */
  public static getInstance(): ConfigManager {
    if (!ConfigManager.instance) {
      ConfigManager.instance = new ConfigManager();
    }
    return ConfigManager.instance;
  }

  /**
   * Get configuration file path
   */
  private getConfigPath(): string {
    // Check for environment-specific config
    const env = process.env.NODE_ENV || 'development';
    const envConfigPath = path.join(process.cwd(), `config.${env}.json`);
    
    // Check for default config
    const defaultConfigPath = path.join(process.cwd(), 'config.json');
    
    // Check for example config
    const exampleConfigPath = path.join(process.cwd(), 'config.example.json');

    // Priority: env config > default config > example config
    if (fs.existsSync(envConfigPath)) {
      this.logger.info(`Using environment config: ${envConfigPath}`);
      return envConfigPath;
    } else if (fs.existsSync(defaultConfigPath)) {
      this.logger.info(`Using default config: ${defaultConfigPath}`);
      return defaultConfigPath;
    } else if (fs.existsSync(exampleConfigPath)) {
      this.logger.warn(`Using example config. Please create config.json`);
      return exampleConfigPath;
    } else {
      throw new Error('No configuration file found. Please create config.json');
    }
  }

  /**
   * Load configuration from file
   */
  private loadConfig(): CompanyConfig {
    try {
      const configData = fs.readFileSync(this.configPath, 'utf8');
      const config = JSON.parse(configData);
      
      // Validate and set defaults
      return this.validateConfig(config);
      
    } catch (error) {
      this.logger.error(`Failed to load config from ${this.configPath}:`, error);
      
      // Return default config
      return this.getDefaultConfig();
    }
  }

  /**
   * Validate configuration and set defaults
   */
  private validateConfig(config: any): CompanyConfig {
    const defaultConfig = this.getDefaultConfig();
    
    // Merge with defaults
    const validatedConfig: CompanyConfig = {
      ...defaultConfig,
      ...config
    };

    // Validate required fields
    this.validateRequiredFields(validatedConfig);

    // Validate numeric ranges
    this.validateNumericRanges(validatedConfig);

    // Validate integration configs
    this.validateIntegrations(validatedConfig);

    this.logger.info('Configuration validated successfully');
    return validatedConfig;
  }

  /**
   * Validate required fields
   */
  private validateRequiredFields(config: CompanyConfig): void {
    const requiredFields = ['name', 'mission', 'maxConcurrentResearch'];
    
    for (const field of requiredFields) {
      if (!config[field as keyof CompanyConfig]) {
        throw new Error(`Missing required configuration field: ${field}`);
      }
    }
  }

  /**
   * Validate numeric ranges
   */
  private validateNumericRanges(config: CompanyConfig): void {
    // Validate maxConcurrentResearch
    if (config.maxConcurrentResearch < 1 || config.maxConcurrentResearch > 100) {
      this.logger.warn(`maxConcurrentResearch should be between 1 and 100, got ${config.maxConcurrentResearch}`);
      config.maxConcurrentResearch = Math.max(1, Math.min(100, config.maxConcurrentResearch));
    }

    // Validate ethicsThreshold
    if (config.ethicsThreshold < 0 || config.ethicsThreshold > 1) {
      this.logger.warn(`ethicsThreshold should be between 0 and 1, got ${config.ethicsThreshold}`);
      config.ethicsThreshold = Math.max(0, Math.min(1, config.ethicsThreshold));
    }

    // Validate maxCognitiveLoad
    if (config.maxCognitiveLoad < 0.1 || config.maxCognitiveLoad > 1) {
      this.logger.warn(`maxCognitiveLoad should be between 0.1 and 1, got ${config.maxCognitiveLoad}`);
      config.maxCognitiveLoad = Math.max(0.1, Math.min(1, config.maxCognitiveLoad));
    }
  }

  /**
   * Validate integration configurations
   */
  private validateIntegrations(config: CompanyConfig): void {
    // Validate Paperclip integration
    if (config.paperclipIntegration?.enabled) {
      if (!config.paperclipIntegration.apiUrl) {
        throw new Error('Paperclip integration enabled but apiUrl is missing');
      }
      if (!config.paperclipIntegration.companyId) {
        throw new Error('Paperclip integration enabled but companyId is missing');
      }
    }

    // Validate OpenClaw integration
    if (config.openclawIntegration?.enabled) {
      if (!config.openclawIntegration.workspacePath) {
        throw new Error('OpenClaw integration enabled but workspacePath is missing');
      }
    }
  }

  /**
   * Get default configuration
   */
  private getDefaultConfig(): CompanyConfig {
    return {
      name: 'Resonance Vale',
      mission: 'Build and maintain an autonomous research agent with built-in prism ethics',
      maxConcurrentResearch: 5,
      maxQueueSize: 20,
      researchPollInterval: 30000, // 30 seconds
      ethicsReviewInterval: 600000, // 10 minutes
      healthCheckInterval: 300000, // 5 minutes
      ethicsThreshold: 0.6,
      maxCognitiveLoad: 0.8,
      paperclipIntegration: {
        enabled: false,
        apiUrl: 'http://localhost:3100',
        companyId: '',
        agentId: ''
      },
      openclawIntegration: {
        enabled: false,
        workspacePath: '',
        skillsPath: ''
      },
      aiAdapters: [
        {
          type: 'openai',
          name: 'GPT-4',
          model: 'gpt-4',
          enabled: true,
          priority: 1
        }
      ]
    };
  }

  /**
   * Get configuration
   */
  public getConfig(): CompanyConfig {
    return { ...this.config };
  }

  /**
   * Update configuration
   */
  public updateConfig(updates: Partial<CompanyConfig>): void {
    const newConfig = { ...this.config, ...updates };
    this.config = this.validateConfig(newConfig);
    
    // Save to file
    this.saveConfig();
    
    this.logger.info('Configuration updated');
  }

  /**
   * Save configuration to file
   */
  private saveConfig(): void {
    try {
      const configDir = path.dirname(this.configPath);
      
      // Ensure directory exists
      if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir, { recursive: true });
      }
      
      // Write config file
      fs.writeFileSync(
        this.configPath,
        JSON.stringify(this.config, null, 2),
        'utf8'
      );
      
      this.logger.info(`Configuration saved to ${this.configPath}`);
    } catch (error) {
      this.logger.error('Failed to save configuration:', error);
    }
  }

  /**
   * Reload configuration from file
   */
  public reloadConfig(): void {
    this.config = this.loadConfig();
    this.logger.info('Configuration reloaded');
  }

  /**
   * Get configuration for a specific module
   */
  public getModuleConfig(moduleName: string): any {
    const moduleConfigs: Record<string, any> = {
      'prism-protocol': {
        redWeight: 0.3,
        blueWeight: 0.4,
        purpleWeight: 0.3,
        maxRecursionDepth: 3,
        maxThinkingTime: 600, // 10 minutes
        safetyThresholds: {
          cognitiveLoad: 0.8,
          emotionalIntensity: 0.7,
          logicalInconsistency: 0.3
        }
      },
      'autonomous-research': {
        defaultMode: 'balanced',
        sourcePriorities: ['academic', 'practical', 'data'],
        analysisDepth: 'moderate',
        qualityThresholds: {
          sourceCredibility: 0.7,
          evidenceStrength: 0.6,
          logicalConsistency: 0.8
        }
      },
      'ceo-xuanji': {
        learningRate: 0.1,
        reflectionDepth: 0.7,
        communicationStyle: 'fire-side',
        decisionMaking: {
          confidenceThreshold: 0.7,
          consultationThreshold: 0.5,
          autonomyLevel: 0.8
        }
      }
    };

    return moduleConfigs[moduleName] || {};
  }

  /**
   * Get environment variables with defaults
   */
  public getEnvVar(key: string, defaultValue?: string): string {
    const value = process.env[key];
    
    if (value === undefined) {
      if (defaultValue !== undefined) {
        return defaultValue;
      }
      throw new Error(`Environment variable ${key} is required but not set`);
    }
    
    return value;
  }

  /**
   * Check if running in development mode
   */
  public isDevelopment(): boolean {
    return process.env.NODE_ENV === 'development';
  }

  /**
   * Check if running in production mode
   */
  public isProduction(): boolean {
    return process.env.NODE_ENV === 'production';
  }

  /**
   * Check if running in test mode
   */
  public isTest(): boolean {
    return process.env.NODE_ENV === 'test';
  }
}

/**
 * Load configuration (convenience function)
 */
export function loadConfig(): CompanyConfig {
  return ConfigManager.getInstance().getConfig();
}

/**
 * Get module configuration (convenience function)
 */
export function getModuleConfig(moduleName: string): any {
  return ConfigManager.getInstance().getModuleConfig(moduleName);
}

/**
 * Check environment (convenience function)
 */
export function isDevelopment(): boolean {
  return ConfigManager.getInstance().isDevelopment();
}

/**
 * Check environment (convenience function)
 */
export function isProduction(): boolean {
  return ConfigManager.getInstance().isProduction();
}

/**
 * Check environment (convenience function)
 */
export function isTest(): boolean {
  return ConfigManager.getInstance().isTest();
}