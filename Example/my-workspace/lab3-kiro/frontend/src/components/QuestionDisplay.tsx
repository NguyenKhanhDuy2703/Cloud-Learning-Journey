import { useState } from 'react';
import './QuestionDisplay.css';

interface QuestionDisplayProps {
  question: string | null;
  onQuestionGenerated: (question: string) => void;
}

function QuestionDisplay({ question, onQuestionGenerated }: QuestionDisplayProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);

    try {
      const response = await fetch('/api/questions/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });

      if (!response.ok) {
        throw new Error('Failed to generate question');
      }

      const data = await response.json();
      onQuestionGenerated(data.question);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate question');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <section className="section question-display">
      <h2 className="section-title">Interview Question</h2>
      
      <div className="question-content">
        {question ? (
          <p className="question-text">{question}</p>
        ) : (
          <p className="question-placeholder">
            Click "Generate Question" to get started with a behavioral interview question.
          </p>
        )}
      </div>

      <div className="button-group">
        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="generate-button"
        >
          {isGenerating ? 'Generating...' : 'Generate Question'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </section>
  );
}

export default QuestionDisplay;
