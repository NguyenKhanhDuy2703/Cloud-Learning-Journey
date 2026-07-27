# Implementation Plan: Interview Coach

## Overview

This plan focuses on building the core MVP functionality of the Interview Coach application within ~1 hour. The implementation prioritizes essential features: project setup, basic UI components, AWS service integrations, and core workflows. Advanced features like comprehensive error handling, testing, and optimizations are excluded to meet the time constraint.

## Tasks

- [x] 1. Set up project structure and install dependencies
  - Create frontend directory with Vite + React + TypeScript
  - Create backend directory with Node.js + Express + TypeScript
  - Install core dependencies: `ws`, `@aws-sdk/client-bedrock-runtime`, `@aws-sdk/client-transcribe-streaming`
  - Configure TypeScript for both frontend and backend
  - Set up environment variables for AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION=us-east-1)
  - _Requirements: 7.1, 7.2, 7.3_

- [x] 2. Implement backend REST API endpoints
  - [x] 2.1 Create Express server with basic routing
    - Set up Express app listening on port 3001
    - Add JSON body parser middleware
    - _Requirements: 7.1, 7.2_
  
  - [x] 2.2 Implement POST /api/questions/generate endpoint
    - Initialize AWS Bedrock client with amazon.nova-premier-v1:0 model
    - Construct question generation prompt using template from design
    - Call Bedrock API and extract question from response
    - Return JSON response with generated question
    - _Requirements: 1.1, 1.2, 1.3, 7.4_
  
  - [x] 2.3 Implement POST /api/feedback/analyze endpoint
    - Accept question and transcription in request body
    - Construct feedback analysis prompt using template from design
    - Call Bedrock API with STAR format analysis instructions
    - Parse JSON response and return feedback structure
    - _Requirements: 4.1, 4.2, 5.1, 5.2, 5.3, 5.4, 7.5_

- [x] 3. Implement WebSocket transcription service
  - [x] 3.1 Set up WebSocket server on backend
    - Create WebSocket server using `ws` library on port 3002
    - Handle client connection and disconnection events
    - _Requirements: 7.3_
  
  - [x] 3.2 Implement AWS Transcribe streaming integration
    - Initialize AWS Transcribe Streaming client
    - On 'start' message: establish Transcribe WebSocket connection with PCM 16kHz config
    - On 'audio' message: decode base64 audio and forward to Transcribe
    - On Transcribe transcription events: forward text to frontend client
    - On 'stop' message: close Transcribe connection
    - _Requirements: 3.1, 3.2, 3.3, 3.5, 8.4_

- [x] 4. Build frontend UI components and layout
  - [x] 4.1 Create main App component with state management
    - Define AppState interface with currentQuestion, sessionState, transcription, feedback
    - Implement state hooks for question, session status, transcription, and feedback
    - Create black and white CSS styling with adequate spacing
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [x] 4.2 Create QuestionDisplay component
    - Display current question or placeholder text
    - Add "Generate Question" button that calls /api/questions/generate
    - Show loading state during generation
    - _Requirements: 1.4, 6.3_
  
  - [x] 4.3 Create PracticeSession component
    - Implement conditional rendering: show "Start Practice Session" when idle, show "Stop Session" when recording
    - Add session timer display that updates every second during active session
    - Create live transcription display area
    - _Requirements: 2.1, 2.3, 2.4, 2.5, 3.4, 6.4, 6.5_
  
  - [x] 4.4 Create FeedbackPanel component
    - Display STAR analysis results with component presence indicators
    - Show strengths, improvements, and tips sections
    - Use encouraging visual design with clear section headers
    - _Requirements: 5.1, 5.2, 5.3, 5.6_

- [x] 5. Implement frontend audio capture and WebSocket client
  - [x] 5.1 Add microphone access and audio capture
    - Request microphone permission when "Start Practice Session" is clicked
    - Use MediaRecorder API to capture audio in compatible format
    - Convert audio to PCM 16kHz format for AWS Transcribe
    - Release microphone when session stops
    - _Requirements: 8.1, 8.3, 8.4, 8.5_
  
  - [x] 5.2 Implement WebSocket client for transcription streaming
    - Establish WebSocket connection to ws://localhost:3002 on session start
    - Send 'start' message with audio config (sampleRate: 16000, languageCode: 'en-US')
    - Stream audio chunks as base64-encoded 'audio' messages
    - Receive 'transcription' messages and update live display
    - Send 'stop' message and close connection on session end
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 6. Integrate session workflow and feedback analysis
  - [x] 6.1 Wire session start/stop logic
    - On start: transition to recording state, start timer, initialize audio capture, connect WebSocket
    - On stop: transition to analyzing state, stop timer, stop audio capture, close WebSocket, preserve transcription
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.6_
  
  - [x] 6.2 Implement feedback analysis trigger
    - After session stops, automatically call /api/feedback/analyze with question and transcription
    - Update feedback state with analysis results
    - Transition to idle state after feedback is received
    - _Requirements: 4.1, 5.1_

- [ ] 7. Final integration and manual testing
  - Start backend server and verify both REST and WebSocket endpoints are running
  - Start frontend dev server and test complete workflow: generate question → start session → speak → stop session → view feedback
  - Verify transcription appears in real-time during recording
  - Verify STAR analysis and feedback display correctly after session ends
  - Ensure all tests pass, ask the user if questions arise

## Notes

- This plan excludes unit tests, property tests, comprehensive error handling, and deployment configurations to meet the ~1 hour time constraint
- Focus is on core functionality: question generation, audio capture, real-time transcription, and feedback analysis
- AWS credentials must be configured in environment variables before starting
- Both frontend and backend will run locally (frontend on default Vite port, backend REST on 3001, WebSocket on 3002)
- Manual testing in task 7 replaces automated test suites for rapid MVP validation
