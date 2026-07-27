# AWS Knowledge Chat Assistant

A Streamlit application that provides an interactive chat interface powered by a Strands agent with access to AWS documentation through the AWS Knowledge MCP server.

## Features

- 💬 Interactive chat interface for AWS questions
- ☁️ Real-time access to AWS documentation via MCP server
- 🔍 Search AWS services and best practices
- 📚 Detailed service information lookup
- 🎯 Example questions to get started
- 🧠 Conversation memory and context
- 🔄 Automatic fallback if MCP server unavailable

## Prerequisites

- Python 3.8+
- AWS Bedrock API key or AWS credentials
- `uv` package manager (for MCP server - optional but recommended)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install uv package manager (optional but recommended):**
   ```bash
   # For better AWS documentation access
   pip install uv
   
   # Verify installation
   uvx --version
   ```

3. **Set up AWS credentials:**
   
   **Option 1: Bedrock API Key (Recommended for development)**
   - Get an API key from [AWS Bedrock Console](https://console.aws.amazon.com/bedrock)
   - Enable model access for Claude models
   - Create a `.env` file:
     ```
     AWS_BEDROCK_API_KEY=your_bedrock_api_key_here
     ```
   
   **Option 2: AWS Credentials**
   - Set up AWS credentials via `aws configure` or environment variables
   - Create a `.env` file:
     ```
     AWS_ACCESS_KEY_ID=your_access_key
     AWS_SECRET_ACCESS_KEY=your_secret_key
     AWS_REGION=us-west-2
     ```

## Usage

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to the URL shown (typically `http://localhost:8501`)

3. **Start chatting** about AWS services! Try questions like:
   - "What is Amazon S3 and what are its main features?"
   - "How do I set up a Lambda function?"
   - "What are the different EC2 instance types?"
   - "Explain AWS IAM roles and policies"

## How It Works

The application uses:

1. **Strands Agents SDK** - Provides the conversational AI agent framework
2. **AWS Documentation MCP Server** - Accesses real-time AWS documentation via Model Context Protocol
3. **Streamlit** - Creates the interactive web interface

The agent dynamically loads MCP tools from the AWS Documentation server:
- Real-time AWS service documentation search
- Up-to-date best practices and guides
- Automatic fallback to basic tools if MCP server unavailable

## Project Structure

```
├── app.py                 # Main Streamlit application
├── simple_agent.py        # AWS Knowledge Agent class
├── aws_knowledge_tool.py  # AWS MCP tools for the agent
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── setup.py              # Setup script for easy installation
└── README.md             # This file
```

## Troubleshooting

**"MCP server not available"**
- Install uv: `pip install uv`
- The app will work with fallback tools if MCP server fails
- For full functionality, ensure uvx is available

**"AWS Credentials Required"**
- Set up your `.env` file with either Bedrock API key or AWS credentials
- For Bedrock, ensure model access is enabled in the console

**Agent initialization fails**
- Check your AWS credentials are valid
- Ensure you have internet connectivity for MCP server access
- Verify the Strands agents package is installed correctly

## License

MIT License - feel free to modify and use for your projects!