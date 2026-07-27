"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const dotenv_1 = __importDefault(require("dotenv"));
const ws_1 = require("ws");
const bedrock_1 = require("./services/bedrock");
const transcription_1 = require("./services/transcription");
// Load environment variables
dotenv_1.default.config();
const app = (0, express_1.default)();
const PORT = 3001;
const WS_PORT = 3002;
// Middleware
app.use((0, cors_1.default)());
app.use(express_1.default.json());
// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
});
// Question generation endpoint
app.post('/api/questions/generate', async (req, res) => {
    try {
        const question = await (0, bedrock_1.generateQuestion)();
        res.json({ question });
    }
    catch (error) {
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
        const feedback = await (0, bedrock_1.analyzeFeedback)(question, transcription);
        res.json(feedback);
    }
    catch (error) {
        console.error('Error analyzing feedback:', error);
        res.status(500).json({ error: 'Failed to analyze response' });
    }
});
// Start server
app.listen(PORT, () => {
    console.log(`Backend server running on port ${PORT}`);
});
// Create WebSocket server for transcription
const wsServer = new ws_1.WebSocketServer({ port: WS_PORT });
wsServer.on('connection', (ws) => {
    console.log('WebSocket client connected');
    (0, transcription_1.handleTranscriptionSession)(ws);
});
wsServer.on('error', (error) => {
    console.error('WebSocket server error:', error);
});
console.log(`WebSocket server running on port ${WS_PORT}`);
