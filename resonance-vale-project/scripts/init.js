#!/usr/bin/env node

/**
 * Resonance Vale Project Initialization Script
 * 
 * This script sets up a new Resonance Vale project with all necessary
 * configuration files and directory structure.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

// Create readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m'
};

/**
 * Print colored message
 */
function print(color, message) {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * Print header
 */
function printHeader() {
  console.log('\n' + '='.repeat(60));
  print('cyan', '🔥 RESONANCE VALE PROJECT INITIALIZATION');
  console.log('='.repeat(60));
  print('dim', 'An autonomous research company with built-in prism ethics');
  console.log('='.repeat(60) + '\n');
}

/**
 * Check if running in correct directory
 */
function checkDirectory() {
  const currentDir = process.cwd();
  const packageJsonPath = path.join(currentDir, 'package.json');
  
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    if (packageJson.name === 'resonance-vale') {
      print('yellow', '⚠️  Already in a Resonance Vale project directory');
      return true;
    }
  }
  
  return false;
}

/**
 * Create directory structure
 */
function createDirectoryStructure() {
  print('blue', '📁 Creating directory structure...');
  
  const directories = [
    'src',
    'src/core',
    'src/prism-protocol',
    'src/autonomous-research',
    'src/integrations',
    'src/integrations/paperclip',
    'src/integrations/openclaw',
    'src/integrations/ai-adapters',
    'src/skills',
    'src/utils',
    'src/types',
    'tests',
    'tests/unit',
    'tests/integration',
    'tests/e2e',
    'docs',
    'docs/philosophy',
    'docs/implementation',
    'docs/research',
    'docs/user',
    'scripts',
    'tools',
    'examples',
    'storage',
    'storage/research',
    'storage/logs',
    'storage/cache'
  ];
  
  directories.forEach(dir => {
    const dirPath = path.join(process.cwd(), dir);
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
      print('dim', `  Created: ${dir}`);
    }
  });
  
  print('green', '✅ Directory structure created');
}

/**
 * Copy template files
 */
function copyTemplateFiles() {
  print('blue', '📄 Copying template files...');
  
  const templates = {
    'config.example.json': 'config.json',
    '.env.example': '.env',
    'README.md': 'README.md',
    'LICENSE': 'LICENSE',
    '.gitignore': '.gitignore',
    'tsconfig.json': 'tsconfig.json',
    'package.json': 'package.json'
  };
  
  // Get the directory where this script is located
  const scriptDir = __dirname;
  const projectRoot = path.dirname(scriptDir);
  
  Object.entries(templates).forEach(([source, target]) => {
    const sourcePath = path.join(projectRoot, source);
    const targetPath = path.join(process.cwd(), target);
    
    if (fs.existsSync(sourcePath) && !fs.existsSync(targetPath)) {
      fs.copyFileSync(sourcePath, targetPath);
      print('dim', `  Copied: ${source} → ${target}`);
    }
  });
  
  print('green', '✅ Template files copied');
}

/**
 * Install dependencies
 */
function installDependencies() {
  print('blue', '📦 Installing dependencies...');
  
  try {
    // Check if pnpm is available
    try {
      execSync('pnpm --version', { stdio: 'ignore' });
      print('dim', '  Using pnpm...');
      execSync('pnpm install', { stdio: 'inherit' });
    } catch (error) {
      // Fall back to npm
      print('dim', '  Using npm (pnpm not available)...');
      execSync('npm install', { stdio: 'inherit' });
    }
    
    print('green', '✅ Dependencies installed');
  } catch (error) {
    print('red', '❌ Failed to install dependencies');
    print('yellow', '   You can install them manually with: pnpm install');
  }
}

/**
 * Set up Git repository
 */
function setupGitRepository() {
  print('blue', '🔧 Setting up Git repository...');
  
  try {
    // Check if already a git repository
    const gitDir = path.join(process.cwd(), '.git');
    if (fs.existsSync(gitDir)) {
      print('yellow', '  Git repository already exists');
      return;
    }
    
    // Initialize git repository
    execSync('git init', { stdio: 'inherit' });
    
    // Create initial commit
    execSync('git add .', { stdio: 'inherit' });
    execSync('git commit -m "feat: Initial Resonance Vale project setup"', { stdio: 'inherit' });
    
    print('green', '✅ Git repository initialized');
  } catch (error) {
    print('yellow', '⚠️  Git setup skipped or failed');
  }
}

/**
 * Set up environment variables
 */
async function setupEnvironmentVariables() {
  print('blue', '🔐 Setting up environment variables...');
  
  const questions = [
    {
      name: 'nodeEnv',
      question: 'Environment (development/production): ',
      default: 'development'
    },
    {
      name: 'port',
      question: 'Port number: ',
      default: '3000'
    },
    {
      name: 'openaiKey',
      question: 'OpenAI API key (optional): ',
      default: ''
    },
    {
      name: 'anthropicKey',
      question: 'Anthropic API key (optional): ',
      default: ''
    }
  ];
  
  const answers = {};
  
  for (const q of questions) {
    const answer = await askQuestion(q.question, q.default);
    answers[q.name] = answer;
  }
  
  // Update .env file
  const envPath = path.join(process.cwd(), '.env');
  if (fs.existsSync(envPath)) {
    let envContent = fs.readFileSync(envPath, 'utf8');
    
    // Update values
    envContent = envContent.replace(/NODE_ENV=.*/, `NODE_ENV=${answers.nodeEnv}`);
    envContent = envContent.replace(/PORT=.*/, `PORT=${answers.port}`);
    
    if (answers.openaiKey) {
      envContent = envContent.replace(/OPENAI_API_KEY=.*/, `OPENAI_API_KEY=${answers.openaiKey}`);
    }
    
    if (answers.anthropicKey) {
      envContent = envContent.replace(/ANTHROPIC_API_KEY=.*/, `ANTHROPIC_API_KEY=${answers.anthropicKey}`);
    }
    
    fs.writeFileSync(envPath, envContent);
    print('green', '✅ Environment variables configured');
  }
}

/**
 * Ask a question and get user input
 */
function askQuestion(question, defaultValue = '') {
  return new Promise((resolve) => {
    const formattedQuestion = defaultValue ? 
      `${question}[${defaultValue}] ` : 
      `${question}`;
    
    rl.question(formattedQuestion, (answer) => {
      resolve(answer || defaultValue);
    });
  });
}

/**
 * Display completion message
 */
function displayCompletionMessage() {
  console.log('\n' + '='.repeat(60));
  print('green', '🎉 RESONANCE VALE PROJECT SETUP COMPLETE!');
  console.log('='.repeat(60));
  
  print('cyan', '\n🚀 Next steps:');
  print('white', '  1. Review and edit configuration files:');
  print('dim', '     - config.json (main configuration)');
  print('dim', '     - .env (environment variables)');
  
  print('white', '\n  2. Start the development server:');
  print('dim', '     pnpm dev');
  
  print('white', '\n  3. Explore the project structure:');
  print('dim', '     src/ - Source code');
  print('dim', '     docs/ - Documentation');
  print('dim', '     tests/ - Test files');
  
  print('white', '\n  4. Read the documentation:');
  print('dim', '     docs/ - Complete documentation');
  print('dim', '     README.md - Project overview');
  
  print('white', '\n  5. Join the community:');
  print('dim', '     GitHub: https://github.com/Ultima0369/resonance-vale');
  print('dim', '     Discussions: Fire-side dialogue welcome!');
  
  console.log('\n' + '='.repeat(60));
  print('magenta', '🔥 Come, sit by the fire. The code is warm.');
  console.log('='.repeat(60) + '\n');
}

/**
 * Main function
 */
async function main() {
  try {
    printHeader();
    
    // Check if already in project directory
    if (checkDirectory()) {
      const proceed = await askQuestion('Continue with setup? (y/n): ', 'y');
      if (proceed.toLowerCase() !== 'y') {
        print('yellow', 'Setup cancelled');
        rl.close();
        return;
      }
    }
    
    // Create directory structure
    createDirectoryStructure();
    
    // Copy template files
    copyTemplateFiles();
    
    // Install dependencies
    installDependencies();
    
    // Set up Git repository
    setupGitRepository();
    
    // Set up environment variables
    await setupEnvironmentVariables();
    
    // Display completion message
    displayCompletionMessage();
    
  } catch (error) {
    print('red', `❌ Setup failed: ${error.message}`);
    console.error(error);
  } finally {
    rl.close();
  }
}

// Run the main function
if (require.main === module) {
  main();
}

module.exports = { main };