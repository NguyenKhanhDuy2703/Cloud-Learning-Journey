import { WebSocket } from 'ws';
import {
  TranscribeStreamingClient,
  StartStreamTranscriptionCommand,
  TranscriptResultStream,
  LanguageCode,
} from '@aws-sdk/client-transcribe-streaming';

const transcribeClient = new TranscribeStreamingClient({
  region: 'us-east-1',
});

interface TranscribeClientMessage {
  type: 'start' | 'audio' | 'stop';
  config?: {
    sampleRate: number;
    languageCode: string;
  };
  data?: string;
}

interface TranscribeServerMessage {
  type: 'transcription' | 'error';
  text?: string;
  isFinal?: boolean;
  message?: string;
}

export async function handleTranscriptionSession(ws: WebSocket): Promise<void> {
  let transcribeStream: AsyncIterable<TranscriptResultStream> | null = null;
  let audioStream: any = null;

  ws.on('message', async (message: string) => {
    try {
      const data: TranscribeClientMessage = JSON.parse(message);

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
    } catch (error) {
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

  async function handleStart(
    ws: WebSocket,
    data: TranscribeClientMessage
  ): Promise<void> {
    const sampleRate = data.config?.sampleRate || 16000;
    const languageCode: LanguageCode = 'en-US';

    // Create an async generator for audio stream
    audioStream = createAudioStream();

    try {
      const command = new StartStreamTranscriptionCommand({
        LanguageCode: languageCode,
        MediaSampleRateHertz: sampleRate,
        MediaEncoding: 'pcm',
        AudioStream: audioStream,
      });

      const response = await transcribeClient.send(command);
      transcribeStream = response.TranscriptResultStream!;

      // Process transcription results
      processTranscriptionStream(ws, transcribeStream);
    } catch (error) {
      console.error('Error starting transcription:', error);
      sendError(ws, 'Failed to start transcription service');
    }
  }

  async function handleAudio(data: TranscribeClientMessage): Promise<void> {
    if (!audioStream || !data.data) {
      return;
    }

    try {
      // Decode base64 audio data
      const audioBuffer = Buffer.from(data.data, 'base64');
      
      // Push audio to the stream
      audioStream.push(audioBuffer);
    } catch (error) {
      console.error('Error processing audio:', error);
    }
  }

  async function handleStop(): Promise<void> {
    cleanup();
  }

  function cleanup(): void {
    if (audioStream) {
      audioStream.push(null); // Signal end of stream
      audioStream = null;
    }
    transcribeStream = null;
  }
}

function createAudioStream() {
  const chunks: Buffer[] = [];
  let resolveNext: ((value: IteratorResult<{ AudioEvent: { AudioChunk: Uint8Array } }>) => void) | null = null;
  let ended = false;

  return {
    push(chunk: Buffer | null) {
      if (chunk === null) {
        ended = true;
        if (resolveNext) {
          resolveNext({ done: true, value: undefined });
          resolveNext = null;
        }
        return;
      }

      if (resolveNext) {
        resolveNext({ 
          done: false, 
          value: { AudioEvent: { AudioChunk: new Uint8Array(chunk) } }
        });
        resolveNext = null;
      } else {
        chunks.push(chunk);
      }
    },

    [Symbol.asyncIterator]() {
      return {
        async next(): Promise<IteratorResult<{ AudioEvent: { AudioChunk: Uint8Array } }>> {
          if (chunks.length > 0) {
            const chunk = chunks.shift()!;
            return { 
              done: false, 
              value: { AudioEvent: { AudioChunk: new Uint8Array(chunk) } }
            };
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

async function processTranscriptionStream(
  ws: WebSocket,
  stream: AsyncIterable<TranscriptResultStream>
): Promise<void> {
  try {
    for await (const event of stream) {
      if (event.TranscriptEvent) {
        const results = event.TranscriptEvent.Transcript?.Results || [];
        
        for (const result of results) {
          if (result.Alternatives && result.Alternatives.length > 0) {
            const transcript = result.Alternatives[0].Transcript || '';
            const isFinal = !result.IsPartial;

            if (transcript) {
              const message: TranscribeServerMessage = {
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
  } catch (error) {
    console.error('Error processing transcription stream:', error);
    sendError(ws, 'Transcription service error');
  }
}

function sendError(ws: WebSocket, message: string): void {
  const errorMessage: TranscribeServerMessage = {
    type: 'error',
    message,
  };
  ws.send(JSON.stringify(errorMessage));
}
