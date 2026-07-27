import { BedrockRuntimeClient, InvokeModelCommand } from '@aws-sdk/client-bedrock-runtime';

const client = new BedrockRuntimeClient({
  region: 'us-east-1',
});

const MODEL_ID = 'amazon.nova-pro-v1:0';

const QUESTION_GENERATION_PROMPT = `You are an interview coach helping college students practice behavioral interviews.
Generate a single behavioral interview question appropriate for entry-level candidates.

The question should:
- Focus on one of these categories: leadership, teamwork, conflict resolution, problem-solving, failure/learning, or time management
- Be open-ended and encourage STAR format responses
- Be realistic for college students with limited work experience

Generate only the question text, no additional commentary.`;

interface BedrockRequestBody {
  messages: Array<{
    role: 'user' | 'assistant';
    content: Array<{ text: string }>;
  }>;
  inferenceConfig?: {
    maxTokens: number;
    temperature: number;
  };
}

export async function generateQuestion(): Promise<string> {
  const requestBody: BedrockRequestBody = {
    messages: [
      {
        role: 'user',
        content: [{ text: QUESTION_GENERATION_PROMPT }],
      },
    ],
    inferenceConfig: {
      maxTokens: 1000,
      temperature: 0.7,
    },
  };

  const command = new InvokeModelCommand({
    modelId: MODEL_ID,
    contentType: 'application/json',
    accept: 'application/json',
    body: JSON.stringify(requestBody),
  });

  const response = await client.send(command);
  const responseBody = JSON.parse(new TextDecoder().decode(response.body));
  
  // Extract the question from the response
  const question = responseBody.output?.message?.content?.[0]?.text || '';
  
  return question.trim();
}

interface ComponentAnalysis {
  present: boolean;
  content: string | null;
}

interface FeedbackResult {
  starAnalysis: {
    situation: ComponentAnalysis;
    task: ComponentAnalysis;
    action: ComponentAnalysis;
    result: ComponentAnalysis;
  };
  strengths: string[];
  improvements: string[];
  tips: string[];
  fillerWords: {
    count: number;
    examples: string[];
  };
}

function createFeedbackPrompt(question: string, transcription: string): string {
  return `You are an encouraging interview coach analyzing a student's response to a behavioral interview question.

Question: ${question}

Response: ${transcription}

Analyze this response using the STAR format (Situation, Task, Action, Result).

For each component:
1. Identify if it is present or absent
2. If present, extract the relevant content

Then provide:
- 2-3 specific strengths (what they did well)
- 2-3 areas for improvement (what's missing or weak)
- 2-3 actionable tips for improvement

Also analyze filler words:
- Count occurrences of filler words like "um", "uh", "like", "you know", "so", "actually", "basically", "literally", etc.
- List the specific filler words found with their frequency

Use an encouraging, constructive tone. Be specific and helpful.

Return your analysis in JSON format matching this structure:
{
  "starAnalysis": {
    "situation": {"present": boolean, "content": string or null},
    "task": {"present": boolean, "content": string or null},
    "action": {"present": boolean, "content": string or null},
    "result": {"present": boolean, "content": string or null}
  },
  "strengths": [string],
  "improvements": [string],
  "tips": [string],
  "fillerWords": {
    "count": number,
    "examples": [string]
  }
}`;
}

export async function analyzeFeedback(question: string, transcription: string): Promise<FeedbackResult> {
  const prompt = createFeedbackPrompt(question, transcription);
  
  const requestBody: BedrockRequestBody = {
    messages: [
      {
        role: 'user',
        content: [{ text: prompt }],
      },
    ],
    inferenceConfig: {
      maxTokens: 2000,
      temperature: 0.3,
    },
  };

  const command = new InvokeModelCommand({
    modelId: MODEL_ID,
    contentType: 'application/json',
    accept: 'application/json',
    body: JSON.stringify(requestBody),
  });

  const response = await client.send(command);
  const responseBody = JSON.parse(new TextDecoder().decode(response.body));
  
  // Extract the feedback from the response
  const feedbackText = responseBody.output?.message?.content?.[0]?.text || '';
  
  // Parse the JSON response from the model
  const feedback = JSON.parse(feedbackText);
  
  return feedback;
}
