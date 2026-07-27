import type { FeedbackResult } from '../types';
import './FeedbackPanel.css';

interface FeedbackPanelProps {
  feedback: FeedbackResult | null;
  isAnalyzing: boolean;
}

function FeedbackPanel({ feedback, isAnalyzing }: FeedbackPanelProps) {
  if (isAnalyzing) {
    return (
      <section className="section feedback-panel">
        <h2 className="section-title">Feedback</h2>
        <div className="analyzing-message">
          Analyzing your response...
        </div>
      </section>
    );
  }

  if (!feedback) {
    return (
      <section className="section feedback-panel">
        <h2 className="section-title">Feedback</h2>
        <div className="no-feedback-message">
          Complete a practice session to receive feedback on your response.
        </div>
      </section>
    );
  }

  const { starAnalysis, strengths, improvements, tips, fillerWords } = feedback;

  return (
    <section className="section feedback-panel">
      <h2 className="section-title">Feedback</h2>

      <div className="star-analysis">
        <h3>STAR Format Analysis</h3>
        <div className="star-components">
          <div className={`star-component ${starAnalysis.situation.present ? 'present' : 'missing'}`}>
            <span className="component-indicator">
              {starAnalysis.situation.present ? '✓' : '✗'}
            </span>
            <span className="component-name">Situation</span>
            {starAnalysis.situation.present && starAnalysis.situation.content && (
              <p className="component-content">{starAnalysis.situation.content}</p>
            )}
          </div>

          <div className={`star-component ${starAnalysis.task.present ? 'present' : 'missing'}`}>
            <span className="component-indicator">
              {starAnalysis.task.present ? '✓' : '✗'}
            </span>
            <span className="component-name">Task</span>
            {starAnalysis.task.present && starAnalysis.task.content && (
              <p className="component-content">{starAnalysis.task.content}</p>
            )}
          </div>

          <div className={`star-component ${starAnalysis.action.present ? 'present' : 'missing'}`}>
            <span className="component-indicator">
              {starAnalysis.action.present ? '✓' : '✗'}
            </span>
            <span className="component-name">Action</span>
            {starAnalysis.action.present && starAnalysis.action.content && (
              <p className="component-content">{starAnalysis.action.content}</p>
            )}
          </div>

          <div className={`star-component ${starAnalysis.result.present ? 'present' : 'missing'}`}>
            <span className="component-indicator">
              {starAnalysis.result.present ? '✓' : '✗'}
            </span>
            <span className="component-name">Result</span>
            {starAnalysis.result.present && starAnalysis.result.content && (
              <p className="component-content">{starAnalysis.result.content}</p>
            )}
          </div>
        </div>
      </div>

      <div className="feedback-section strengths-section">
        <h3>Strengths</h3>
        <ul>
          {strengths.map((strength, index) => (
            <li key={index}>{strength}</li>
          ))}
        </ul>
      </div>

      <div className="feedback-section improvements-section">
        <h3>Areas for Improvement</h3>
        <ul>
          {improvements.map((improvement, index) => (
            <li key={index}>{improvement}</li>
          ))}
        </ul>
      </div>

      <div className="feedback-section tips-section">
        <h3>Tips for Next Time</h3>
        <ul>
          {tips.map((tip, index) => (
            <li key={index}>{tip}</li>
          ))}
        </ul>
      </div>

      {fillerWords && fillerWords.count > 0 && (
        <div className="feedback-section filler-words-section">
          <h3>Filler Words</h3>
          <p className="filler-count">
            You used {fillerWords.count} filler word{fillerWords.count !== 1 ? 's' : ''} in your response.
          </p>
          {fillerWords.examples.length > 0 && (
            <div className="filler-examples">
              <strong>Examples:</strong> {fillerWords.examples.join(', ')}
            </div>
          )}
          <p className="filler-tip">
            Try to minimize filler words by pausing briefly instead. This makes your response sound more confident and polished.
          </p>
        </div>
      )}
    </section>
  );
}

export default FeedbackPanel;
