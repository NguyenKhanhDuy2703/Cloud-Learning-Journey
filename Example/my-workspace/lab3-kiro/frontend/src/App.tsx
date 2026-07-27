import { useState } from 'react';
import './App.css';
import type { FeedbackResult, SessionState } from './types';
import QuestionDisplay from './components/QuestionDisplay';
import PracticeSession from './components/PracticeSession';
import FeedbackPanel from './components/FeedbackPanel';

function App() {
  const [currentQuestion, setCurrentQuestion] = useState<string | null>(null);
  const [sessionState, setSessionState] = useState<SessionState>('idle');
  const [transcription, setTranscription] = useState<string>('');
  const [feedback, setFeedback] = useState<FeedbackResult | null>(null);

  const handleSessionComplete = (finalTranscription: string) => {
    setTranscription(finalTranscription);
    setSessionState('analyzing');
    
    // Call feedback API
    if (currentQuestion) {
      fetch('/api/feedback/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: currentQuestion,
          transcription: finalTranscription
        })
      })
        .then(res => res.json())
        .then(data => {
          setFeedback(data);
          setSessionState('idle');
        })
        .catch(err => {
          console.error('Feedback analysis failed:', err);
          setSessionState('idle');
        });
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Interview Coach</h1>
        <p>Practice behavioral interview questions with AI-powered feedback</p>
      </header>

      <div className="app-content">
        <QuestionDisplay
          question={currentQuestion}
          onQuestionGenerated={setCurrentQuestion}
        />

        {currentQuestion && (
          <PracticeSession
            question={currentQuestion}
            sessionState={sessionState}
            onSessionStateChange={setSessionState}
            onSessionComplete={handleSessionComplete}
            transcription={transcription}
          />
        )}

        <FeedbackPanel
          feedback={feedback}
          isAnalyzing={sessionState === 'analyzing'}
        />
      </div>
    </div>
  );
}

export default App;
