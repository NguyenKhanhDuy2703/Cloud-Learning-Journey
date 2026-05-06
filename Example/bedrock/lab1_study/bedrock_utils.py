import boto3
import json
import os

def get_bedrock_client():
    """Khởi tạo client để kết nối với Amazon Bedrock."""
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    )

def invoke_nova_model(prompt, temperature, top_p, response_style):
    client = get_bedrock_client()
    
    # Định dạng prompt
    formatted_prompt = f"Please provide a {response_style} response.\n\nUser: {prompt}"
    
    # Cấu hình Body đúng chuẩn Amazon Nova
    input_data = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": formatted_prompt}]
            }
        ],
        "inferenceConfig": {
            "temperature": temperature,
            "topP": top_p,
            "maxTokens": 2048
        }
    }

    try:
        response = client.invoke_model(
            modelId="amazon.nova-pro-v1:0",
            body=json.dumps(input_data) # Sử dụng json.dumps thay vì replace()
        )
        
        response_body = json.loads(response.get('body').read())
        # Trích xuất dữ liệu theo cấu trúc của Nova
        return response_body['output']['message']['content'][0]['text']
        
    except Exception as e:
        return f"Lỗi kết nối Bedrock: {str(e)}"
# --- EXERCISE 2: LOCAL RAG CONFIGURATION ---

# TODO: Exercise 2 - Thay thế "___" bằng model ID chính xác
embedding_model = "amazon.titan-embed-text-v1" #

def get_embedding(text):
    """Sử dụng Amazon Titan Text Embedding để tạo vector."""
    client = get_bedrock_client()
    
    body = json.dumps({
        "inputText": text
    })
    
    try:
        response = client.invoke_model(
            modelId=embedding_model, # Sử dụng biến đã định nghĩa ở trên
            body=body
        )
        
        response_body = json.loads(response.get('body').read())
        return response_body.get('embedding')
    except Exception as e:
        print(f"Lỗi tạo Embedding: {str(e)}")
        return None