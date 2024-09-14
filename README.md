# IBM Watson AI Wrapper

This project provides a command-line interface for interacting with IBM's Watson AI using the watsonX.ai API. It allows users to engage in conversations with the AI model, supporting both English and Arabic languages.

Created by Sultan Wehaibi

## Prerequisites

- Python 3.6 or higher
- An IBM Cloud account with access to watsonX.ai
- API key and Project ID from IBM Cloud

## Installation

1. Clone this repository or download the `ibm_watsonx_ai_wrapper.py` file.

2. Install the required Python packages using the provided `requirements.txt` file:

   ```
   pip install -r requirements.txt
   ```

   This will install the following packages:
   - requests
   - python-dotenv

3. Create a `.env` file in the same directory as the script with the following content:

   ```
   IBM_WATSONX_API_KEY=your_api_key_here
   IBM_WATSONX_PROJECT_ID=your_project_id_here
   IBM_WATSONX_URL=https://eu-de.ml.cloud.ibm.com
   ```

   Replace `your_api_key_here` and `your_project_id_here` with your actual IBM Watson API key and Project ID.

   **Note**: The `.env` file is a hidden file. If you can't see it in your file explorer, you may need to enable "Show hidden files" in your operating system settings.

4. Editing the `.env` file:
   - On Windows:
     1. Open File Explorer and navigate to the script's directory.
     2. Click on 'View' in the top menu and check 'Hidden items'.
     3. Right-click on the .env file and select 'Edit'.
   - On macOS or Linux:
     1. Open a terminal and navigate to the script's directory.
     2. Run the following command to edit the file:
        ```
        nano .env
        ```

   Update the values with your actual API key and Project ID.

## Usage

Run the script from the command line:

```
python ibm_watsonx_ai_wrapper.py
```

The script will check if you've updated the `.env` file with your actual API key and Project ID. If you haven't, it will provide instructions on how to do so.

You can also specify additional parameters:

```
python ibm_watsonx_ai_wrapper.py --max_new_tokens 900 --temperature 0.7 --top_p 1 --repetition_penalty 1.0 --timeout 60
```

### Parameters

- `--max_new_tokens`: Maximum number of new tokens to generate (default: 900)
- `--decoding_method`: Decoding method, either "greedy" or "sample" (default: "greedy")
- `--temperature`: Temperature for sampling (default: 0.7)
- `--top_p`: Top-p sampling value (default: 1)
- `--repetition_penalty`: Repetition penalty (default: 1.0)
- `--timeout`: Timeout for API calls in seconds (default: 60)

## Interacting with the AI

Once the script is running, you can start chatting with the AI. Type your messages and press Enter to send them. The AI will respond to each of your inputs.

To exit the program, type '/q' and press Enter.

## Support for Arabic

This wrapper fully supports Arabic input and output. You can type questions or prompts in Arabic, and the AI will respond in Arabic as well.

## Troubleshooting

If you encounter any issues:

1. Ensure your API key and Project ID are correct in the `.env` file.
2. Check your internet connection.
3. Verify that you have the necessary permissions in your IBM Cloud account.
4. If you're having trouble with Arabic text display, make sure your terminal supports UTF-8 encoding.
5. If you encounter package-related issues, ensure you've installed all required packages using the `requirements.txt` file.

## Disclaimer

This wrapper is an unofficial tool and is not affiliated with, officially maintained, or endorsed by IBM. Use it responsibly and in accordance with IBM's terms of service.

## Credits

This IBM Watson AI Wrapper was created by Sultan Wehaibi for the ALLaM Challange 2024.

For any questions or issues, please open an issue in this repository.