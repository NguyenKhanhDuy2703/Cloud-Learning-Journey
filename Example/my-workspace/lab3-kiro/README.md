# Interview Coach

An AI-powered application that helps college students practice behavioral interview questions and receive structured feedback using the STAR format.

## Project Structure

```
interview-coach/
├── frontend/          # React + Vite + TypeScript frontend
│   ├── src/          # Source files
│   ├── public/       # Static assets
│   └── package.json  # Frontend dependencies
├── backend/          # Node.js + Express + TypeScript backend
│   ├── src/          # Source files
│   └── package.json  # Backend dependencies
└── README.md         # This file
```

## Prerequisites

- Node.js 18+
- npm or yarn
- AWS Account with access to:
  - AWS Bedrock (amazon.nova-premier-v1:0 model)
  - AWS Transcribe Streaming

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Copy the environment variables template:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   AWS_REGION=us-east-1
   PORT=3000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Copy the environment variables template:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` if needed (defaults should work for local development):
   ```
   VITE_API_URL=http://localhost:3000
   VITE_WS_URL=ws://localhost:3000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open your browser to `http://localhost:5173`

## Technology Stack

### Frontend
- React 19+ with functional components and hooks
- Vite for build tooling and dev server
- TypeScript for type safety
- Native WebSocket API for streaming
- MediaRecorder API for microphone access

### Backend
- Node.js 18+ with Express framework
- TypeScript for type safety
- `ws` library for WebSocket server
- AWS SDK v3 for Bedrock and Transcribe clients

### AWS Services
- AWS Bedrock with `amazon.nova-premier-v1:0` model for text generation
- AWS Transcribe Streaming for real-time speech-to-text
- Region: `us-east-1`

## Core Dependencies

### Backend
- `express` - Web framework
- `ws` - WebSocket server
- `@aws-sdk/client-bedrock-runtime` - AWS Bedrock client
- `@aws-sdk/client-transcribe-streaming` - AWS Transcribe client
- `cors` - CORS middleware

### Frontend
- `react` - UI library
- `react-dom` - React DOM renderer
- `vite` - Build tool and dev server

## Development

### Backend Scripts
- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm start` - Start production server

### Frontend Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Features

- Generate realistic behavioral interview questions
- Real-time audio transcription during practice sessions
- STAR format analysis and feedback
- Session timer and live transcription display
- Clean black and white UI design
