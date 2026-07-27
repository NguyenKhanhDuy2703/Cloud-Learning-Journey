// Type definitions for Interview Coach application

export interface ComponentAnalysis {
  present: boolean;
  content: string | null;
}

export interface FeedbackResult {
  starAnalysis: {
    situation: ComponentAnalysis;
    task: ComponentAnalysis;
    action: ComponentAnalysis;
    result: ComponentAnalysis;
  };
  strengths: string[];
  improvements: string[];
  tips: string[];
  fillerWords: {
    count: number;
    examples: string[];
  };
}

export type SessionState = 'idle' | 'recording' | 'analyzing';

export interface AppState {
  currentQuestion: string | null;
  sessionState: SessionState;
  transcription: string;
  feedback: FeedbackResult | null;
}
