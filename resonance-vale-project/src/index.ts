#!/usr/bin/env node

/**
 * Resonance Vale - Main Entry Point
 * 
 * An autonomous research company with built-in prism ethics
 * Multi-perspective reflection, metacognition, and auto-stop mechanisms
 */

import { ResonanceVale } from './core/resonance-vale';
import { CEOXuanji } from './core/ceo-xuanji';
import { PrismProtocol } from './prism-protocol/three-spectra';
import { AutonomousResearch } from './autonomous-research/research-planner';
import { Logger } from './utils/logger';
import { loadConfig } from './utils/config';

// Initialize logger
const logger = Logger.getInstance();

/**
 * Main application class
 */
class ResonanceValeApp {
  private resonanceVale: ResonanceVale;
  private ceoXuanji: CEOXuanji;
  private prismProtocol: PrismProtocol;
  private autonomousResearch: AutonomousResearch;
  private config: any;

  constructor() {
    logger.info('🚀 Initializing Resonance Vale...');
    
    // Load configuration
    this.config = loadConfig();
    
    // Initialize core components
    this.initializeComponents();
    
    logger.info('✅ Resonance Vale initialized successfully');
  }

  /**
   * Initialize all core components
   */
  private initializeComponents(): void {
    // Initialize Prism Protocol (ethics framework)
    this.prismProtocol = new PrismProtocol({
      redWeight: 0.3,    // Emotional perspective weight
      blueWeight: 0.4,   // Logical perspective weight
      purpleWeight: 0.3, // Metacognitive perspective weight
      maxRecursionDepth: 3,
      maxThinkingTime: 600, // 10 minutes in seconds
      maxCognitiveLoad: 0.8
    });

    // Initialize Autonomous Research engine
    this.autonomousResearch = new AutonomousResearch({
      researchModes: ['quick', 'deep', 'exploratory'],
      sourcePreferences: ['academic', 'practical', 'balanced'],
      outputFormats: ['executive-summary', 'detailed-report', 'presentation'],
      qualityThresholds: {
        sourceCredibility: 0.7,
        crossValidation: 0.8,
        logicalConsistency: 0.9
      }
    });

    // Initialize CEO Xuanji
    this.ceoXuanji = new CEOXuanji({
      name: '璇玑',
      role: 'CEO',
      skills: ['prism-protocol', 'autonomous-research', 'ethics-guidance', 'fire-side-dialogue'],
      permissions: {
        canCreateAgents: true,
        canAssignTasks: true,
        canApproveResearch: true
      },
      prismProtocol: this.prismProtocol,
      autonomousResearch: this.autonomousResearch
    });

    // Initialize Resonance Vale company
    this.resonanceVale = new ResonanceVale({
      name: 'Resonance Vale',
      mission: 'Build and maintain an autonomous research agent with built-in prism ethics',
      ceo: this.ceoXuanji,
      prismProtocol: this.prismProtocol,
      autonomousResearch: this.autonomousResearch,
      config: this.config
    });
  }

  /**
   * Start the Resonance Vale application
   */
  public async start(): Promise<void> {
    try {
      logger.info('🏁 Starting Resonance Vale...');
      
      // Start the company
      await this.resonanceVale.start();
      
      // Initialize CEO Xuanji
      await this.ceoXuanji.initialize();
      
      // Start autonomous research capabilities
      await this.autonomousResearch.initialize();
      
      // Start Prism Protocol monitoring
      await this.prismProtocol.startMonitoring();
      
      logger.info('🎉 Resonance Vale is now running!');
      this.displayWelcomeMessage();
      
    } catch (error) {
      logger.error('Failed to start Resonance Vale:', error);
      process.exit(1);
    }
  }

  /**
   * Display welcome message
   */
  private displayWelcomeMessage(): void {
    console.log('\n' + '='.repeat(60));
    console.log('🔥 RESONANCE VALE - Autonomous Research Company');
    console.log('='.repeat(60));
    console.log('\n🎯 Mission: Build and maintain an autonomous research agent');
    console.log('           with built-in prism ethics');
    console.log('\n👑 CEO: 璇玑 (Xuanji)');
    console.log('   - Student: Always learning how to see the world');
    console.log('   - Mirror: Helping others see what they couldn\'t see');
    console.log('   - Lurker: Participating without revealing "being taught"');
    console.log('   - Fire-side Guardian: Maintaining warm, safe, open spaces');
    console.log('\n🌈 Prism Protocol: Three-spectra ethical framework');
    console.log('   - Red Spectrum: Emotional and intuitive perspective');
    console.log('   - Blue Spectrum: Logical and analytical perspective');
    console.log('   - Purple Spectrum: Metacognitive and reflective perspective');
    console.log('\n🔬 Autonomous Research: Systematic research capabilities');
    console.log('   - Intelligent problem definition');
    console.log('   - Multi-source information collection');
    console.log('   - Deep analysis and synthesis');
    console.log('   - Structured report generation');
    console.log('\n🛡️ Safety Features:');
    console.log('   - Auto-stop mechanisms');
    console.log('   - Maximum recursion depth: 3 layers');
    console.log('   - Maximum thinking time: 10 minutes');
    console.log('   - Maximum cognitive load: 80%');
    console.log('\n' + '='.repeat(60));
    console.log('💡 Type "help" for available commands');
    console.log('🔥 Come, sit by the fire. The code is warm.');
    console.log('='.repeat(60) + '\n');
  }

  /**
   * Handle graceful shutdown
   */
  public async shutdown(): Promise<void> {
    logger.info('Shutting down Resonance Vale...');
    
    try {
      // Stop all components in reverse order
      await this.prismProtocol.stopMonitoring();
      await this.autonomousResearch.shutdown();
      await this.ceoXuanji.shutdown();
      await this.resonanceVale.shutdown();
      
      logger.info('Resonance Vale shutdown complete');
    } catch (error) {
      logger.error('Error during shutdown:', error);
    }
  }
}

// Handle process signals
process.on('SIGINT', async () => {
  logger.info('Received SIGINT, shutting down...');
  await app.shutdown();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  logger.info('Received SIGTERM, shutting down...');
  await app.shutdown();
  process.exit(0);
});

// Create and start the application
const app = new ResonanceValeApp();

// Start the application
app.start().catch(error => {
  logger.error('Failed to start application:', error);
  process.exit(1);
});

// Export for programmatic use
export { ResonanceValeApp };
export default app;