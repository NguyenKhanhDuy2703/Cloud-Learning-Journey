"""
AgentCore Study Guide Client
Intermediate script to call the study guide agent hosted on AgentCore using runtime ARN
"""

import json
import boto3
from typing import Dict, Any
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

class AgentCoreStudyGuideClient:
    """Client to interact with study guide agent hosted on AgentCore using runtime ARN"""
    
    def __init__(self):
        # Use hardcoded ARN for your deployed agent
        self.runtime_arn = self.runtime_arn = os.getenv('AGENTCORE_RUNTIME_ARN')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        print(f"Initializing AgentCore client with ARN: {self.runtime_arn}")
        
        # Initialize boto3 client for AgentCore
        try:
            self.bedrock_agentcore = boto3.client(
                'bedrock-agentcore',
                region_name=self.aws_region
            )
            print(f"Successfully initialized bedrock-agentcore client in region: {self.aws_region}")
        except Exception as e:
            print(f"Failed to initialize bedrock-agentcore client: {e}")
            raise
    
    def generate_study_guide(self, topic: str) -> str:
        """
        Generate a comprehensive study guide for the given AWS topic
        
        Args:
            topic: The AWS topic to create a study guide for
            
        Returns:
            Generated study guide content as markdown string
        """
        try:
            print(f"Generating study guide for topic: {topic}")
            
            # Prepare the payload - use message_content instead of prompt
            payload = json.dumps({
                "message_content": f"Create a comprehensive study guide for: {topic}"
            })
            
            # Generate a session ID (must be 33+ characters)
            session_id = f"study_guide_session_{uuid.uuid4().hex}"
            print(f"Using session ID: {session_id}")
            
            # Prepare invoke parameters
            invoke_params = {
                'agentRuntimeArn': self.runtime_arn,
                'runtimeSessionId': session_id,
                'payload': payload
            }
            
            print(f"Invoking AgentCore with payload: {payload}")
            
            # Invoke the AgentCore runtime
            response = self.bedrock_agentcore.invoke_agent_runtime(**invoke_params)
            
            print(f"Received response from AgentCore")
            
            # Process the response
            response_body = response['response'].read()
            print(f"Response body length: {len(response_body)} bytes")
            
            # Try to parse as JSON
            try:
                response_data = json.loads(response_body)
                print(f"Successfully parsed JSON response")
                print(f"Response keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Not a dict'}")
            except json.JSONDecodeError:
                print(f"Response is not JSON, treating as plain text")
                return response_body.decode('utf-8') if isinstance(response_body, bytes) else str(response_body)
            
            # Extract the study guide content
            if 'error' in response_data and response_data['error']:
                error_msg = response_data['error']
                print(f"Agent returned an error: {error_msg}")
                
                # Check if there's still a result despite the error
                if 'result' in response_data and response_data['result']:
                    print(f"Found result despite error, proceeding...")
                    return self._extract_content_text(response_data['result'])
                else:
                    # If it's a client initialization error, suggest using the simplified deployment
                    if "client initialization failed" in error_msg.lower():
                        raise Exception(f"AgentCore agent initialization failed. This is likely due to MCP server issues. Please redeploy using agentcore_deployment_simple.py which doesn't require MCP. Original error: {error_msg}")
                    else:
                        raise Exception(f"Agent error: {error_msg}")
            elif 'result' in response_data:
                print(f"Found 'result' field in response")
                return self._extract_content_text(response_data['result'])
            elif 'response' in response_data:
                print(f"Found 'response' field in response")
                return self._extract_content_text(response_data['response'])
            elif 'message' in response_data:
                print(f"Found 'message' field in response")
                return self._extract_content_text(response_data['message'])
            elif 'content' in response_data:
                print(f"Found 'content' field in response")
                return self._extract_content_text(response_data['content'])
            else:
                print(f"No expected fields found, trying to extract from full response")
                return self._extract_content_text(response_data)
                
        except Exception as e:
            print(f"Error in generate_study_guide: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            raise Exception(f"Failed to call AgentCore runtime: {str(e)}")
    
    def _extract_content_text(self, data) -> str:
        """
        Extract text content from various response formats
        
        Args:
            data: Response data that could be string, dict, or nested structure
            
        Returns:
            Extracted text content
        """
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            # Handle AgentCore response format: {'role': 'assistant', 'content': [{'text': '...'}]}
            if 'content' in data and isinstance(data['content'], list):
                # Extract text from content array
                text_parts = []
                for item in data['content']:
                    if isinstance(item, dict) and 'text' in item:
                        text_parts.append(item['text'])
                    elif isinstance(item, str):
                        text_parts.append(item)
                return ''.join(text_parts)
            elif 'content' in data:
                return self._extract_content_text(data['content'])
            elif 'text' in data:
                return data['text']
            elif 'message' in data:
                return self._extract_content_text(data['message'])
            else:
                return str(data)
        elif isinstance(data, list):
            # Handle list of content items
            text_parts = []
            for item in data:
                text_parts.append(self._extract_content_text(item))
            return ''.join(text_parts)
        else:
            return str(data)

def create_agentcore_study_guide_client() -> AgentCoreStudyGuideClient:
    """Factory function to create AgentCore study guide client"""
    return AgentCoreStudyGuideClient()

def generate_study_guide_via_agentcore(topic: str) -> str:
    """
    Convenience function to generate study guide via AgentCore
    
    Args:
        topic: AWS topic to create study guide for
        
    Returns:
        Generated study guide content
    """
    client = create_agentcore_study_guide_client()
    return client.generate_study_guide(topic)

# Test function for development
if __name__ == "__main__":
    # Test the AgentCore integration
    test_topic = "Amazon S3"
    
    try:
        print(f"🧪 Testing AgentCore study guide generation for: {test_topic}")
        print("=" * 60)
        
        guide = generate_study_guide_via_agentcore(test_topic)
        
        print("=" * 60)
        print("✅ Successfully generated study guide")
        print(f"📏 Guide length: {len(guide)} characters")
        print("\n📖 First 500 characters:")
        print("-" * 40)
        print(guide[:500] + "..." if len(guide) > 500 else guide)
        print("-" * 40)
        
    except Exception as e:
        print("=" * 60)
        print(f"❌ Error: {e}")
        print(f"🔍 Error details: {type(e).__name__}")
        
        # Additional debugging info
        import traceback
        print("\n🐛 Full traceback:")
        traceback.print_exc()