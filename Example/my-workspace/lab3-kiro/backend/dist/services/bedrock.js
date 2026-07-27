"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateQuestion = generateQuestion;
exports.analyzeFeedback = analyzeFeedback;
const client_bedrock_runtime_1 = require("@aws-sdk/client-bedrock-runtime");
const client = new client_bedrock_runtime_1.BedrockRuntimeClient({
    region: 'us-east-1',
});
const MODEL_ID = 'amazon.nova-premier-v1:0';
const QUESTION_GENERATION_PROMPT = `You are an interview coach helping college students practice behavioral interviews.
Generate a single behavioral interview question appropriate for entry-level candidates.

The question should:
- Focus on one of these categories: leadership, teamwork, conflict resolution, problem-solving, failure/learning, or time management
- Be open-ended and encourage STAR format responses
- Be realistic for college students with limited work experience

Generate only the question text, no additional commentary.`;
async function generateQuestion() {
    const requestBody = {
        messages: [
            {
                role: 'user',
                content: QUESTION_GENERATION_PROMPT,
            },
        ],
        max_tokens: 1000,
        temperature: 0.7,
    };
    const command = new client_bedrock_runtime_1.InvokeModelCommand({
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
function createFeedbackPrompt(question, transcription) {
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
  "tips": [string]
}`;
}
async function analyzeFeedback(question, transcription) {
    const prompt = createFeedbackPrompt(question, transcription);
    const requestBody = {
        messages: [
            {
                role: 'user',
                content: prompt,
            },
        ],
        max_tokens: 2000,
        temperature: 0.3,
    };
    const command = new client_bedrock_runtime_1.InvokeModelCommand({
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
