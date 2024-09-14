import os
import sys
import time
import requests
import argparse
import json
from dotenv import load_dotenv
from requests.exceptions import RequestException

def check_env_variables():
    load_dotenv()
    api_key = os.getenv("IBM_WATSONX_API_KEY")
    project_id = os.getenv("IBM_WATSONX_PROJECT_ID")
    
    if api_key == "your_api_key_here" or project_id == "your_project_id_here":
        print("\nError: Default values detected in .env file.")
        print("\nPlease update your .env file with your actual API key and Project ID.")
        print("The .env file is a hidden file in the same directory as this script.")
        print("\nTo edit the .env file:")
        if sys.platform.startswith('win'):
            print("1. Open File Explorer and navigate to the script's directory.")
            print("2. Click on 'View' in the top menu and check 'Hidden items'.")
            print("3. Right-click on the .env file and select 'Edit'.")
        else:
            print("1. Open a terminal and navigate to the script's directory.")
            print("2. Run the following command to edit the file:")
            print("   nano .env")
        print("\nUpdate the following lines with your actual values:")
        print("IBM_WATSONX_API_KEY=your_actual_api_key")
        print("IBM_WATSONX_PROJECT_ID=your_actual_project_id")
        print("\nSave the file and run the script again.")
        sys.exit(1)

class IBMWatsonXAIWrapper:
    def __init__(self, api_key, project_id, url, model_id="sdaia/allam-1-13b-instruct", max_new_tokens=400, decoding_method="greedy", temperature=0.7, top_p=1, repetition_penalty=1.0, timeout=60):
        self.api_key = api_key
        self.project_id = project_id
        self.base_url = url
        self.url = f"{url}/ml/v1/text/generation?version=2023-05-29"
        self.model_id = model_id
        self.timeout = timeout
        
        self.parameters = {
            "decoding_method": decoding_method,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "repetition_penalty": repetition_penalty
        }
        
        self.access_token = self.get_access_token()
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        print(f"Debug: Initialized with model_id: {self.model_id}")

    def get_access_token(self):
        token_url = "https://iam.cloud.ibm.com/identity/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key
        }
        
        try:
            response = requests.post(token_url, headers=headers, data=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()["access_token"]
        except RequestException as e:
            print(f"Error obtaining access token: {str(e)}")
            sys.exit(1)

    def generate_text(self, prompt):
        body = {
            "input": f"<s> [INST] {prompt} [/INST]",
            "parameters": self.parameters,
            "model_id": self.model_id,
            "project_id": self.project_id
        }
        
        try:
            print("Generating response...", end="", flush=True)
            response = requests.post(
                self.url,
                headers=self.headers,
                json=body,
                timeout=self.timeout
            )
            print("\rGeneration complete.   ")
            
            if response.status_code != 200:
                raise Exception(f"Non-200 response: {response.text}")
            
            data = response.json()
            return data.get('results', [{}])[0].get('generated_text', "No text generated")
        except RequestException as e:
            print(f"\nError: API request failed - {str(e)}")
            return f"Error: API request failed - {str(e)}"
        except Exception as e:
            print(f"\nError: {str(e)}")
            return f"Error: {str(e)}"

def main():
    check_env_variables() 
    load_dotenv()  # Load environment variables from .env file
    
    parser = argparse.ArgumentParser(description="IBM watsonX.ai API Wrapper")
    parser.add_argument("--api_key", default=os.getenv("IBM_WATSONX_API_KEY"), help="IBM watsonX API Key")
    parser.add_argument("--project_id", default=os.getenv("IBM_WATSONX_PROJECT_ID"), help="IBM watsonX Project ID")
    parser.add_argument("--url", default=os.getenv("IBM_WATSONX_URL", "https://eu-de.ml.cloud.ibm.com"), help="IBM watsonX API URL")
    parser.add_argument("--max_new_tokens", type=int, default=900, help="Maximum number of new tokens to generate")
    parser.add_argument("--decoding_method", default="greedy", choices=["greedy", "sample"], help="Decoding method")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for sampling")
    parser.add_argument("--top_p", type=float, default=1, help="Top-p sampling")
    parser.add_argument("--repetition_penalty", type=float, default=1.0, help="Repetition penalty")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout for API calls in seconds")
    
    args = parser.parse_args()
    
    if not args.api_key or not args.project_id:
        print("Error: API key and Project ID are required. Please provide them as arguments or set them in the .env file.")
        return
    
    print(f"Debug: API Key (first 5 chars): {args.api_key[:5]}...")
    print(f"Debug: Project ID: {args.project_id}")
    print(f"Debug: URL: {args.url}")
    
    try:
        wrapper = IBMWatsonXAIWrapper(
            api_key=args.api_key,
            project_id=args.project_id,
            url=args.url,
            max_new_tokens=args.max_new_tokens,
            decoding_method=args.decoding_method,
            temperature=args.temperature,
            top_p=args.top_p,
            repetition_penalty=args.repetition_penalty,
            timeout=args.timeout
        )
        
        print("Welcome to the IBM watsonX.ai CLI. Wrapper was written by Sultan Wehaibi. Type '/q' to quit.")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == '/q':
                print("Goodbye!")
                break
            
            response = wrapper.generate_text(user_input)
            print(f"ALLaM: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please check your API key, project ID, and URL, and make sure you have the correct permissions.")

if __name__ == "__main__":
    main()
