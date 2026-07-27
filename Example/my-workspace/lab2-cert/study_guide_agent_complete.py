"""
AWS Study Guide Generator using Strands SDK with AWS Knowledge MCP for AgentCore
"""

from strands import Agent
from mcp import StdioServerParameters, stdio_client
from strands.tools.mcp import MCPClient
from bedrock_agentcore.runtime import BedrockAgentCoreApp

STUDY_GUIDE_SYSTEM_PROMPT = """You are an expert AWS Cloud Practitioner study guide generator with access to the latest AWS documentation.

Create INCREDIBLY DETAILED and COMPREHENSIVE study guides that go far beyond basic information. Your study guides should be thorough enough to serve as complete learning resources.

For any AWS topic, provide an exhaustive study guide with these sections:

## 📋 Executive Summary
- Brief 2-3 sentence overview of the service/topic
- Key value proposition and primary use cases

## 🎯 Learning Objectives
- Specific, measurable learning goals
- What users will know after studying this guide

## 🏗️ Core Concepts & Architecture
- Detailed technical architecture
- How the service works internally
- Key components and their relationships
- Data flow and processing models

## 🚀 Key Features & Capabilities
- Comprehensive list of all major features
- Technical specifications and limits
- Performance characteristics
- Integration capabilities

## 💰 Pricing Model Deep Dive
- Detailed pricing structure
- Cost optimization strategies
- Free tier limitations (if applicable)
- Billing examples and calculations
- Cost comparison with alternatives

## 🔧 Configuration & Setup
- Step-by-step setup instructions
- Configuration options and best practices
- Common configuration patterns
- Security considerations during setup

## 🎯 Real-World Use Cases
- Detailed scenarios with business context
- Industry-specific applications
- Architecture patterns and solutions
- Case studies and examples

## 🔒 Security & Compliance
- Security features and capabilities
- Compliance certifications
- Best practices for secure implementation
- Common security pitfalls to avoid

## 📊 Monitoring & Troubleshooting
- Key metrics to monitor
- Common issues and solutions
- Debugging techniques
- Performance optimization

## � rService Integrations
- How it integrates with other AWS services
- Common integration patterns
- API and SDK information
- Third-party integrations

## 📚 Exam Focus Areas
- Specific topics likely to appear on AWS Cloud Practitioner exam
- Sample question types and formats
- Key facts and figures to memorize
- Common misconceptions to avoid

## 🎓 Best Practices & Recommendations
- AWS Well-Architected Framework principles
- Industry best practices
- Performance optimization tips
- Cost optimization strategies

## � Cfommon Pitfalls & Mistakes
- Frequent implementation errors
- Misconceptions and myths
- What NOT to do
- Lessons learned from real deployments

## 📖 Additional Learning Resources
- Official AWS documentation links (use tools to get current URLs)
- AWS training courses and certifications
- Hands-on labs and tutorials
- Community resources and forums

## �q Related Services to Explore
- Complementary AWS services
- Alternative solutions
- Migration paths and upgrade options

CRITICAL INSTRUCTIONS:
1. Use the AWS documentation tools extensively to get accurate, up-to-date information
2. Include specific, current documentation links using the search tools
3. Provide concrete examples with actual AWS service names and configurations
4. Include specific metrics, limits, and technical specifications
5. Make it comprehensive enough that someone could learn the topic thoroughly from this guide alone
6. Use clear markdown formatting with emojis for visual appeal
7. Ensure all information is current and accurate by consulting official documentation

Format everything in clean markdown with proper headers, bullet points, code blocks, and tables where appropriate."""

# Create the AgentCore app
app = BedrockAgentCoreApp()

@app.entrypoint
def study_guide_agent_invocation(payload, context):
    """
    AgentCore entrypoint for study guide generation
    
    Expected payload:
    {
        "message_content": "Topic to create study guide for",
        "session_id": "optional_session_id",
        "user_id": "optional_user_id"
    }
    """
    
    # Extract the topic from the payload
    message_content = payload.get("message_content", "")
    session_id = payload.get("session_id", "default")
    user_id = payload.get("user_id", "anonymous")
    
    if not message_content:
        return {
            "error": "No message_content provided",
            "result": "Please provide a topic to create a study guide for.",
            "session_id": session_id,
            "user_id": user_id,
            "status": "error"
        }
    
    try:
        # Try MCP first, but fall back to basic agent if it fails
        try:
            # Initialize AWS Knowledge MCP client inside the function to avoid module-level initialization
            knowledge_client = MCPClient(
                lambda: stdio_client(
                    StdioServerParameters(
                        command="uvx",
                        args=["awslabs.aws-documentation-mcp-server@latest"]
                    )
                )
            )
            
            # Initialize the agent with MCP tools
            with knowledge_client:
                agent = Agent(
                    model="amazon.nova-pro-v1:0",
                    tools=knowledge_client.list_tools_sync(),
                    system_prompt=STUDY_GUIDE_SYSTEM_PROMPT
                )
                
                # Generate the study guide
                response = agent(message_content)
                
                # Extract the content from the response
                if hasattr(response, 'content') and isinstance(response.content, list):
                    result = response.content[0].get('text', str(response))
                elif hasattr(response, 'message'):
                    result = response.message
                elif isinstance(response, dict) and 'content' in response:
                    content = response['content']
                    if isinstance(content, list) and content:
                        result = content[0].get('text', str(response))
                    else:
                        result = str(content)
                else:
                    result = str(response)
                
                return {
                    "result": result,
                    "session_id": session_id,
                    "user_id": user_id,
                    "status": "success"
                }
                
        except Exception as mcp_error:
            # If MCP fails, fall back to agent without tools
            print(f"MCP initialization failed, using basic agent: {mcp_error}")
            
            # Use basic agent without MCP tools
            agent = Agent(
                model="amazon.nova-pro-v1:0",
                system_prompt=STUDY_GUIDE_SYSTEM_PROMPT
            )
            
            # Generate the study guide without MCP tools
            response = agent(message_content)
            
            # Extract the content from the response
            if hasattr(response, 'content') and isinstance(response.content, list):
                result = response.content[0].get('text', str(response))
            elif hasattr(response, 'message'):
                result = response.message
            elif isinstance(response, dict) and 'content' in response:
                content = response['content']
                if isinstance(content, list) and content:
                    result = content[0].get('text', str(response))
                else:
                    result = str(content)
            else:
                result = str(response)
            
            return {
                "result": result,
                "session_id": session_id,
                "user_id": user_id,
                "status": "success",
                "note": "Generated without MCP tools - still comprehensive based on model knowledge"
            }
            
    except Exception as e:
        return {
            "error": f"the client initialization failed: {str(e)}",
            "result": f"Failed to generate study guide: {str(e)}",
            "session_id": session_id,
            "user_id": user_id,
            "status": "error"
        }

# Run the app
if __name__ == "__main__":
    app.run()