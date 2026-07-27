"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.handleTranscriptionSession = handleTranscriptionSession;
const client_transcribe_streaming_1 = require("@aws-sdk/client-transcribe-streaming");
const transcribeClient = new client_transcribe_streaming_1.TranscribeStreamingClient({
    region: 'us-east-1',
});
async function handleTranscriptionSession(ws) {
    let transcribeStream = null;
    let audioStream = null;
    ws.on('message', async (message) => {
        try {
            const data = JSON.parse(message);
            switch (data.type) {
                case 'start':
                    await handleStart(ws, data);
                    break;
                case 'audio':
                    await handleAudio(data);
                    break;
                case 'stop':
                    await handleStop();
                    break;
                default:
                    console.warn('Unknown message type:', data);
            }
        }
        catch (error) {
            console.error('Error processing message:', error);
            sendError(ws, 'Failed to process message');
        }
    });
    ws.on('close', () => {
        console.log('WebSocket client disconnected');
        cleanup();
    });
    ws.on('error', (error) => {
        console.error('WebSocket error:', error);
        cleanup();
    });
    async function handleStart(ws, data) {
        const sampleRate = data.config?.sampleRate || 16000;
        const languageCode = 'en-US';
        // Create an async generator for audio stream
        audioStream = createAudioStream();
        try {
            const command = new client_transcribe_streaming_1.StartStreamTranscriptionCommand({
                LanguageCode: languageCode,
                MediaSampleRateHertz: sampleRate,
                MediaEncoding: 'pcm',
                AudioStream: audioStream,
            });
            const response = await transcribeClient.send(command);
            transcribeStream = response.TranscriptResultStream;
            // Process transcription results
            processTranscriptionStream(ws, transcribeStream);
        }
        catch (error) {
            console.error('Error starting transcription:', error);
            sendError(ws, 'Failed to start transcription service');
        }
    }
    async function handleAudio(data) {
        if (!audioStream || !data.data) {
            return;
        }
        try {
            // Decode base64 audio data
            const audioBuffer = Buffer.from(data.data, 'base64');
            // Push audio to the stream
            audioStream.push(audioBuffer);
        }
        catch (error) {
            console.error('Error processing audio:', error);
        }
    }
    async function handleStop() {
        cleanup();
    }
    function cleanup() {
        if (audioStream) {
            audioStream.push(null); // Signal end of stream
            audioStream = null;
        }
        transcribeStream = null;
    }
}
function createAudioStream() {
    const chunks = [];
    let resolveNext = null;
    let ended = false;
    return {
        push(chunk) {
            if (chunk === null) {
                ended = true;
                if (resolveNext) {
                    resolveNext({ done: true, value: undefined });
                    resolveNext = null;
                }
                return;
            }
            if (resolveNext) {
                resolveNext({ done: false, value: chunk });
                resolveNext = null;
            }
            else {
                chunks.push(chunk);
            }
        },
        [Symbol.asyncIterator]() {
            return {
                async next() {
                    if (chunks.length > 0) {
                        return { done: false, value: chunks.shift() };
                    }
                    if (ended) {
                        return { done: true, value: undefined };
                    }
                    return new Promise((resolve) => {
                        resolveNext = resolve;
                    });
                },
            };
        },
    };
}
async function processTranscriptionStream(ws, stream) {
    try {
        for await (const event of stream) {
            if (event.TranscriptEvent) {
                const results = event.TranscriptEvent.Transcript?.Results || [];
                for (const result of results) {
                    if (result.Alternatives && result.Alternatives.length > 0) {
                        const transcript = result.Alternatives[0].Transcript || '';
                        const isFinal = !result.IsPartial;
                        if (transcript) {
                            const message = {
                                type: 'transcription',
                                text: transcript,
                                isFinal,
                            };
                            ws.send(JSON.stringify(message));
                        }
                    }
                }
            }
        }
    }
    catch (error) {
        console.error('Error processing transcription stream:', error);
        sendError(ws, 'Transcription service error');
    }
}
function sendError(ws, message) {
    const errorMessage = {
        type: 'error',
        message,
    };
    ws.send(JSON.stringify(errorMessage));
}
