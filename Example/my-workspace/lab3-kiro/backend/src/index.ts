import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { WebSocketServer } from 'ws';
import { createServer } from 'http';
import { generateQuestion, analyzeFeedback } from './services/bedrock';
import { handleTranscriptionSession } from './services/transcription';

// Load environment variables
dotenv.config();

const app = express();
const PORT = 3001;
const WS_PORT = 3002;

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Question generation endpoint
app.post('/api/questions/generate', async (req, res) => {
  try {
    const question = await generateQuestion();
    res.json({ question });
  } catch (error) {
    console.error('Error generating question:', error);
    res.status(500).json({ error: 'Failed to generate question' });
  }
});

// Feedback analysis endpoint
app.post('/api/feedback/analyze', async (req, res) => {
  try {
    const { question, transcription } = req.body;
    
    if (!question || !transcription) {
      return res.status(400).json({ error: 'Question and transcription are required' });
    }
    
    const feedback = await analyzeFeedback(question, transcription);
    res.json(feedback);
  } catch (error) {
    console.error('Error analyzing feedback:', error);
    res.status(500).json({ error: 'Failed to analyze response' });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});

// Create WebSocket server for transcription
const wsServer = new WebSocketServer({ port: WS_PORT });

wsServer.on('connection', (ws) => {
  console.log('WebSocket client connected');
  handleTranscriptionSession(ws);
});

wsServer.on('error', (error) => {
  console.error('WebSocket server error:', error);
});

console.log(`WebSocket server running on port ${WS_PORT}`);
