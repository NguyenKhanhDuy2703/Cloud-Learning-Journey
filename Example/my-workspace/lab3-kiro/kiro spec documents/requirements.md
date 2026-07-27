# Requirements Document

## Introduction

The Interview Coach is an AI-powered application that helps college students practice behavioral interview questions and receive structured feedback using the STAR format (Situation, Task, Action, Result). The system generates realistic behavioral questions, captures spoken responses through real-time transcription, and provides actionable coaching feedback to improve interview performance.

## Glossary

- **Interview_Coach**: The complete application system that generates questions, captures responses, and provides feedback
- **Question_Generator**: The component that creates behavioral interview questions using AWS Bedrock
- **Practice_Session**: A timed recording session where the user speaks their answer to a behavioral question
- **Transcription_Service**: The component that converts spoken audio to text in real-time using AWS Transcribe
- **Feedback_Analyzer**: The component that evaluates transcribed responses against STAR format criteria using AWS Bedrock
- **STAR_Format**: A structured response framework consisting of Situation, Task, Action, and Result components
- **User**: A college student or entry-level candidate practicing interview skills
- **Behavioral_Question**: An interview question asking about past experiences and behaviors
- **Session_Timer**: A display showing elapsed time during a practice session
- **WebSocket_Connection**: A bidirectional communication channel for streaming audio and transcription data

## Requirements

### Requirement 1: Generate Behavioral Interview Questions

**User Story:** As a user, I want to generate realistic behavioral interview questions, so that I can practice answering different types of questions.

#### Acceptance Criteria

1. WHEN the user clicks "Generate Question", THE Question_Generator SHALL create a behavioral interview question using AWS Bedrock with Amazon Nova Premier model (amazon.nova-premier-v1:0)
2. THE Question_Generator SHALL produce questions from six categories: leadership, teamwork, conflict resolution, problem-solving, failure/learning, and time management
3. THE Question_Generator SHALL create questions appropriate for college students and entry-level candidates
4. THE Interview_Coach SHALL display the generated question in the question display area
5. THE Question_Generator SHALL produce diverse questions across multiple generation requests

### Requirement 2: Start and Stop Practice Sessions

**User Story:** As a user, I want to control when my practice session starts and stops, so that I can speak my answer at my own pace.

#### Acceptance Criteria

1. WHEN the user clicks "Start Practice Session", THE Interview_Coach SHALL begin a new Practice_Session
2. WHILE a Practice_Session is active, THE Interview_Coach SHALL capture audio from the user's microphone
3. WHILE a Practice_Session is active, THE Session_Timer SHALL display elapsed time
4. WHILE a Practice_Session is active, THE Interview_Coach SHALL disable the "Start Practice Session" button
5. WHEN the user clicks "Stop Session", THE Interview_Coach SHALL end the Practice_Session
6. WHEN a Practice_Session ends, THE Interview_Coach SHALL stop capturing audio

### Requirement 3: Real-Time Audio Transcription

**User Story:** As a user, I want to see my words transcribed in real-time as I speak, so that I can verify what is being captured.

#### Acceptance Criteria

1. WHEN a Practice_Session starts, THE Transcription_Service SHALL establish a WebSocket_Connection to AWS Transcribe
2. WHILE a Practice_Session is active, THE Transcription_Service SHALL stream audio data to AWS Transcribe via the WebSocket_Connection
3. WHILE a Practice_Session is active, THE Transcription_Service SHALL receive transcription data from AWS Transcribe via the WebSocket_Connection
4. WHILE transcription data is received, THE Interview_Coach SHALL display the transcribed text in the live transcription display area
5. WHEN a Practice_Session ends, THE Transcription_Service SHALL close the WebSocket_Connection
6. THE Interview_Coach SHALL preserve the complete transcription after the Practice_Session ends

### Requirement 4: Analyze Response Using STAR Format

**User Story:** As a user, I want my response analyzed against the STAR format, so that I understand which components I included or missed.

#### Acceptance Criteria

1. WHEN a Practice_Session ends, THE Feedback_Analyzer SHALL analyze the transcribed response using AWS Bedrock with Amazon Nova Premier model (amazon.nova-premier-v1:0)
2. THE Feedback_Analyzer SHALL identify the presence or absence of each STAR_Format component: Situation, Task, Action, and Result
3. WHERE a Situation component is present, THE Feedback_Analyzer SHALL identify context and background details
4. WHERE a Task component is present, THE Feedback_Analyzer SHALL identify the specific challenge or responsibility described
5. WHERE an Action component is present, THE Feedback_Analyzer SHALL identify the steps taken by the user
6. WHERE a Result component is present, THE Feedback_Analyzer SHALL identify outcomes and impact described
7. THE Feedback_Analyzer SHALL return analysis results indicating which components are present and which are missing

### Requirement 5: Provide Coaching Feedback

**User Story:** As a user, I want to receive encouraging and actionable feedback on my response, so that I can improve my interview skills.

#### Acceptance Criteria

1. WHEN the Feedback_Analyzer completes analysis, THE Interview_Coach SHALL display feedback in the feedback panel
2. THE Interview_Coach SHALL present strengths identifying what the user did well
3. THE Interview_Coach SHALL present areas for improvement identifying specific gaps or weaknesses
4. THE Interview_Coach SHALL provide between two and three actionable tips for improvement
5. THE Interview_Coach SHALL use encouraging and constructive language in all feedback
6. THE Interview_Coach SHALL base all feedback on the STAR_Format analysis results

### Requirement 6: User Interface Design

**User Story:** As a user, I want a clean and intuitive interface, so that I can focus on practicing without distraction.

#### Acceptance Criteria

1. THE Interview_Coach SHALL use a black and white color scheme
2. THE Interview_Coach SHALL provide adequate white space between interface components
3. THE Interview_Coach SHALL display the following components: question display area, Generate Question button, Start Practice Session button, Stop Session button, live transcription display, Session_Timer, and feedback panel
4. WHILE no Practice_Session is active, THE Interview_Coach SHALL hide the Stop Session button
5. WHILE a Practice_Session is active, THE Interview_Coach SHALL hide the Start Practice Session button
6. THE Interview_Coach SHALL use simple and intuitive navigation patterns

### Requirement 7: Frontend-Backend Communication

**User Story:** As a developer, I want well-defined communication protocols between frontend and backend, so that the system components integrate reliably.

#### Acceptance Criteria

1. THE Interview_Coach SHALL provide a REST API endpoint for question generation requests
2. THE Interview_Coach SHALL provide a REST API endpoint for response analysis requests
3. THE Interview_Coach SHALL provide a WebSocket endpoint for real-time transcription streaming
4. WHEN the frontend requests question generation, THE Question_Generator SHALL return a generated question via the REST API
5. WHEN the frontend submits a transcribed response for analysis, THE Feedback_Analyzer SHALL return feedback via the REST API
6. WHILE a Practice_Session is active, THE Transcription_Service SHALL maintain bidirectional communication via WebSocket for audio upload and transcription download

### Requirement 8: Microphone Access and Audio Capture

**User Story:** As a user, I want the application to access my microphone, so that I can speak my answers during practice sessions.

#### Acceptance Criteria

1. WHEN a Practice_Session starts, THE Interview_Coach SHALL request microphone access from the user's browser
2. IF microphone access is denied, THEN THE Interview_Coach SHALL display an error message and prevent the Practice_Session from starting
3. WHEN microphone access is granted, THE Interview_Coach SHALL capture audio from the user's microphone
4. THE Interview_Coach SHALL capture audio in a format compatible with AWS Transcribe streaming requirements
5. WHEN a Practice_Session ends, THE Interview_Coach SHALL release microphone access
