# Call Azure OpenAI from Power BI
# Replace XXX with custom values

# Tweaking boilerplate code from Azure OpenAI Studio Completions screen.
# Remember to install openai, pandas, and matplotlib using pip in the command window.

# Import packages
import os  
import openai
from openai import AzureOpenAI  

# Initialize Azure OpenAI endpoint URL (from Azure Portal)
endpoint = os.getenv("ENDPOINT_URL", "https://XXX.openai.azure.com/")  

# Initialize model deployment name e.g. gpt-35-turbo (from Azure OpenAI Portal)
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")  

# Initialize Azure OpenAI API key (from Azure Portal)
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "XXX")  

# Create connection to Azure OpenAI API
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",  
) 

# Initialize variables
descCol = "Description"
result = ""

# Iterate over records using a pre-populated Pandas dataframe
for index, row in dataset.iterrows():
    # Get description text and store value in a variable
    txt = row[descCol]

    # Create a prompt
    chat_prompt = [
        {
            "role": "system",
            "content": "Summarize the following text using only three bullet points: " + txt
        }
    ]  

    # Include speech result if speech is enabled  
    speech_result = chat_prompt  

    # Call the Azure OpenAI Completions API and get the response
    api_response = client.chat.completions.create(
        model=deployment,  
        messages=speech_result,  
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None,  
        stream=False 
    )

    # Extract API response and store result in a variable
    result = api_response.choices[0].message.content
    # Write result to a new column in the dataset dataframe which automatically updates the semantic model 
    dataset.at[index, "SummaryAOAI"] = result
