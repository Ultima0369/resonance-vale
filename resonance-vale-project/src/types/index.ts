/**
 * Type definitions for Resonance Vale
 */

// Company Configuration
export interface CompanyConfig {
  name: string;
  mission: string;
  maxConcurrentResearch: number;
  maxQueueSize: number;
  researchPollInterval: number;
  ethicsReviewInterval: number;
  healthCheckInterval: number;
  ethicsThreshold: number;
  maxCognitiveLoad: number;
  paperclipIntegration?: PaperclipConfig;
  openclawIntegration?: OpenClawConfig;
  aiAdapters?: AIAdapterConfig[];
}

// Paperclip Integration
export interface PaperclipConfig {
  enabled: boolean;
  apiUrl: string;
  apiKey?: string;
  companyId: string;
  agentId: string;
}

// OpenClaw Integration
export interface OpenClawConfig {
  enabled: boolean;
  workspacePath: string;
  skillsPath: string;
}

// AI Adapter Configuration
export interface AIAdapterConfig {
  type: 'claude' | 'codex' | 'cursor' | 'openai' | 'anthropic' | 'other';
  name: string;
  apiKey?: string;
  model: string;
  enabled: boolean;
  priority: number;
}

// Research Task
export interface ResearchTask {
  id: string;
  title: string;
  description: string;
  researchQuestion: string;
  scope: {
    depth: 'quick' | 'deep' | 'exploratory';
    breadth: 'narrow' | 'moderate' | 'broad';
    timeframe: 'hours' | 'days' | 'weeks';
  };
  constraints: {
    maxDuration?: number; // in minutes
    maxCost?: number;
    ethicalConstraints?: string[];
    legalConstraints?: string[];
  };
  outputRequirements: {
    format: 'executive-summary' | 'detailed-report' | 'presentation';
    sections: string[];
    length?: {
      min: number;
      max: number;
    };
  };
  metadata: {
    submittedBy: string;
    submittedAt: Date;
    priority: 'low' | 'medium' | 'high' | 'critical';
    tags: string[];
  };
  status: 'pending' | 'queued' | 'active' | 'paused' | 'completed' | 'failed' | 'cancelled';
}

// Research Progress
export interface ResearchProgress {
  taskId: string;
  percentage: number;
  currentPhase: ResearchPhase;
  phaseProgress: number;
  cognitiveLoad: number;
  checkpoints: Checkpoint[];
  lastUpdated: Date;
}

// Research Phase
export type ResearchPhase = 
  | 'problem-definition'
  | 'literature-review'
  | 'data-collection'
  | 'analysis'
  | 'synthesis'
  | 'report-writing'
  | 'quality-review'
  | 'completion';

// Checkpoint
export interface Checkpoint {
  phase: ResearchPhase;
  timestamp: Date;
  metrics: {
    sourcesCollected: number;
    analysisDepth: number;
    synthesisQuality: number;
    ethicalConsiderations: number;
  };
  notes: string;
}

// Ethics Review
export interface EthicsReview {
  taskId: string;
  analysis: PrismAnalysis;
  timestamp: Date;
  status: 'analyzed' | 'periodic-review' | 'checkpoint-review' | 'final';
  recommendations?: string[];
  actionsTaken?: string[];
}

// Prism Protocol Analysis
export interface PrismAnalysis {
  redScore: number;        // Emotional/values perspective (0-1)
  blueScore: number;       // Logical/analytical perspective (0-1)
  purpleScore: number;     // Metacognitive/reflective perspective (0-1)
  overallScore: number;    // Weighted average (0-1)
  breakdown: {
    red: {
      emotionalImpact: number;
      valueAlignment: number;
      humanCentricity: number;
    };
    blue: {
      logicalConsistency: number;
      analyticalRigor: number;
      evidenceStrength: number;
    };
    purple: {
      selfAwareness: number;
      processReflection: number;
      learningDepth: number;
    };
  };
  recommendations: 'continue' | 'pause' | 'adjust' | 'stop';
  reasoning: string;
  insights: string[];
}

// Research Result
export interface ResearchResult {
  taskId: string;
  completionTime: Date;
  executiveSummary: string;
  detailedFindings: ResearchFinding[];
  conclusions: string[];
  recommendations: Recommendation[];
  limitations: string[];
  futureResearch: string[];
  metadata: {
    totalDuration: number; // in minutes
    sourcesUsed: number;
    analysisMethods: string[];
    qualityScore: number;
  };
}

// Research Finding
export interface ResearchFinding {
  id: string;
  claim: string;
  evidence: Evidence[];
  confidence: number;
  implications: string[];
  limitations: string[];
}

// Evidence
export interface Evidence {
  source: string;
  type: 'academic' | 'data' | 'expert' | 'practical' | 'theoretical';
  credibility: number;
  relevance: number;
  citation?: string;
  excerpt?: string;
}

// Recommendation
export interface Recommendation {
  type: 'action' | 'policy' | 'research' | 'ethical';
  priority: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  rationale: string;
  implementation: string;
  expectedImpact: string;
  risks: string[];
}

// CEO Xuanji Configuration
export interface CEOXuanjiConfig {
  name: string;
  role: string;
  skills: string[];
  permissions: {
    canCreateAgents: boolean;
    canAssignTasks: boolean;
    canApproveResearch: boolean;
    canModifyEthics: boolean;
    canAccessAllData: boolean;
  };
  learningRate: number;
  reflectionDepth: number;
  communicationStyle: 'direct' | 'reflective' | 'socratic' | 'fire-side';
}

// Skill Definition
export interface Skill {
  id: string;
  name: string;
  description: string;
  category: 'research' | 'ethics' | 'communication' | 'management' | 'technical';
  level: 'basic' | 'intermediate' | 'advanced' | 'expert';
  dependencies: string[];
  configuration: Record<string, any>;
}

// Fire-side Dialogue
export interface FireSideDialogue {
  id: string;
  topic: string;
  participants: Participant[];
  messages: DialogueMessage[];
  atmosphere: {
    warmth: number;
    safety: number;
    openness: number;
    depth: number;
  };
  outcomes: string[];
  reflections: string[];
}

// Participant
export interface Participant {
  id: string;
  type: 'human' | 'ai' | 'system';
  name: string;
  role: string;
  contribution: number;
  perspective: 'red' | 'blue' | 'purple' | 'balanced';
}

// Dialogue Message
export interface DialogueMessage {
  id: string;
  participantId: string;
  timestamp: Date;
  content: string;
  perspective: 'red' | 'blue' | 'purple';
  depth: number;
  responseTo?: string;
  reactions: Reaction[];
}

// Reaction
export interface Reaction {
  participantId: string;
  type: 'agreement' | 'question' | 'insight' | 'challenge' | 'appreciation';
  content?: string;
  intensity: number;
}

// Monitoring Metrics
export interface MonitoringMetrics {
  timestamp: Date;
  system: {
    cpuUsage: number;
    memoryUsage: number;
    diskUsage: number;
    networkActivity: number;
  };
  research: {
    activeTasks: number;
    queueLength: number;
    completionRate: number;
    averageDuration: number;
    successRate: number;
  };
  ethics: {
    reviewsCompleted: number;
    averageScore: number;
    interventions: number;
    complianceRate: number;
  };
  learning: {
    skillsAcquired: number;
    knowledgeGrowth: number;
    patternRecognition: number;
    adaptationRate: number;
  };
}

// Export all types
export type {
  CompanyConfig,
  PaperclipConfig,
  OpenClawConfig,
  AIAdapterConfig,
  ResearchTask,
  ResearchProgress,
  ResearchPhase,
  Checkpoint,
  EthicsReview,
  PrismAnalysis,
  ResearchResult,
  ResearchFinding,
  Evidence,
  Recommendation,
  CEOXuanjiConfig,
  Skill,
  FireSideDialogue,
  Participant,
  DialogueMessage,
  Reaction,
  MonitoringMetrics
};