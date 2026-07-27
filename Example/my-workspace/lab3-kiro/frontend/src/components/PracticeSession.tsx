import { useState, useEffect, useRef } from 'react';
import type { SessionState } from '../types';
import './PracticeSession.css';

interface PracticeSessionProps {
  question: string;
  sessionState: SessionState;
  onSessionStateChange: (state: SessionState) => void;
  onSessionComplete: (transcription: string) => void;
  transcription: string;
}

function PracticeSession({
  sessionState,
  onSessionStateChange,
  onSessionComplete,
  transcription
}: PracticeSessionProps) {
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [finalTranscription, setFinalTranscription] = useState('');
  const [partialTranscription, setPartialTranscription] = useState('');
  const [error, setError] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const audioStreamRef = useRef<MediaStream | null>(null);
  const processorRef = useRef<ScriptProcessorNode | null>(null);
  const startTimeRef = useRef<number | null>(null);
  const timerIntervalRef = useRef<number | null>(null);

  // Timer effect
  useEffect(() => {
    if (sessionState === 'recording') {
      startTimeRef.current = Date.now();
      setElapsedSeconds(0);
      
      timerIntervalRef.current = window.setInterval(() => {
        if (startTimeRef.current) {
          const elapsed = Math.floor((Date.now() - startTimeRef.current) / 1000);
          setElapsedSeconds(elapsed);
        }
      }, 1000);
    } else {
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
        timerIntervalRef.current = null;
      }
    }

    return () => {
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
      }
    };
  }, [sessionState]);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStartSession = async () => {
    setError(null);
    setFinalTranscription('');
    setPartialTranscription('');

    try {
      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioStreamRef.current = stream;
      
      // Create WebSocket connection
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.hostname}:3002`;
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        // Send start message
        ws.send(JSON.stringify({
          type: 'start',
          config: {
            sampleRate: 16000,
            languageCode: 'en-US'
          }
        }));

        // Set up audio processing for PCM conversion
        setupAudioProcessing(stream, ws);
        onSessionStateChange('recording');
      };

      ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        
        if (message.type === 'transcription') {
          if (message.isFinal) {
            // Append final transcription and clear partial
            setFinalTranscription(prev => prev + ' ' + message.text);
            setPartialTranscription('');
          } else {
            // Update partial transcription (replaces previous partial)
            setPartialTranscription(message.text);
          }
        } else if (message.type === 'error') {
          setError(message.message);
        }
      };

      ws.onerror = () => {
        setError('WebSocket connection error');
        handleStopSession();
      };

      ws.onclose = () => {
        // Cleanup handled in handleStopSession
      };

    } catch (err) {
      if (err instanceof Error && err.name === 'NotAllowedError') {
        setError('Microphone access denied. Please allow microphone access to start a practice session.');
      } else {
        setError('Failed to start session. Please check your microphone.');
      }
    }
  };

  const setupAudioProcessing = (stream: MediaStream, ws: WebSocket) => {
    // Create audio context with 16kHz sample rate
    const audioContext = new AudioContext({ sampleRate: 16000 });
    audioContextRef.current = audioContext;

    const source = audioContext.createMediaStreamSource(stream);
    
    // Create script processor for audio data
    const processor = audioContext.createScriptProcessor(4096, 1, 1);
    processorRef.current = processor;

    processor.onaudioprocess = (e) => {
      if (ws.readyState === WebSocket.OPEN) {
        const inputData = e.inputBuffer.getChannelData(0);
        
        // Convert Float32Array to Int16Array (PCM 16-bit)
        const pcmData = new Int16Array(inputData.length);
        for (let i = 0; i < inputData.length; i++) {
          // Clamp to [-1, 1] and convert to 16-bit integer
          const s = Math.max(-1, Math.min(1, inputData[i]));
          pcmData[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
        }

        // Convert to base64 using browser APIs
        const uint8Array = new Uint8Array(pcmData.buffer);
        let binary = '';
        for (let i = 0; i < uint8Array.length; i++) {
          binary += String.fromCharCode(uint8Array[i]);
        }
        const base64 = btoa(binary);

        ws.send(JSON.stringify({
          type: 'audio',
          data: base64
        }));
      }
    };

    source.connect(processor);
    processor.connect(audioContext.destination);
  };

  const handleStopSession = () => {
    // Stop audio processing
    if (processorRef.current) {
      processorRef.current.disconnect();
      processorRef.current = null;
    }

    // Close audio context
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }

    // Release microphone
    if (audioStreamRef.current) {
      audioStreamRef.current.getTracks().forEach(track => track.stop());
      audioStreamRef.current = null;
    }

    // Stop media recorder (if still using it)
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current = null;
    }

    // Close WebSocket
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'stop' }));
      wsRef.current.close();
      wsRef.current = null;
    }

    // Complete session with transcription
    const fullTranscription = (finalTranscription + ' ' + partialTranscription).trim();
    onSessionComplete(fullTranscription);
  };

  return (
    <section className="section practice-session">
      <h2 className="section-title">Practice Session</h2>

      <div className="session-controls">
        {sessionState === 'idle' && (
          <button
            onClick={handleStartSession}
            className="start-button"
          >
            Start Practice Session
          </button>
        )}

        {sessionState === 'recording' && (
          <>
            <button
              onClick={handleStopSession}
              className="stop-button"
            >
              Stop Session
            </button>
            <div className="session-timer">
              Time: {formatTime(elapsedSeconds)}
            </div>
          </>
        )}
      </div>

      {sessionState === 'recording' && (
        <div className="transcription-display">
          <h3>Live Transcription</h3>
          <div className="transcription-text">
            {finalTranscription && <span>{finalTranscription}</span>}
            {partialTranscription && <span className="partial"> {partialTranscription}</span>}
            {!finalTranscription && !partialTranscription && 'Listening...'}
          </div>
        </div>
      )}

      {sessionState === 'idle' && transcription && (
        <div className="transcription-display">
          <h3>Your Response</h3>
          <div className="transcription-text">
            {transcription}
          </div>
        </div>
      )}

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </section>
  );
}

export default PracticeSession;
