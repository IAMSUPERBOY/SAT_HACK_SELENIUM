"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""
from google.generativeai.types import HarmCategory, HarmBlockThreshold

import requests
import os
import streamlit as st

import google.generativeai as genai

genai.configure(api_key="AIzaSyD4ZGanAgjM8OxmyE4tC-kCwITlKxRq5Kg")

st.set_page_config(page_title="Html parser")
st.title("Automated testcase generator")

if "app_key" not in st.session_state:
    app_key="AIzaSyD4ZGanAgjM8OxmyE4tC-kCwITlKxRq5Kg"
    if app_key:
        st.session_state["app_key"]=app_key
# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1.4,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Task: Analyze HTML code, identify text input elements (<input type=\"text\">), and generate corresponding dummy code with characteristics.\n\nInput:\n\nProvide the HTML code as a string.\nSteps:\n\nIdentify text inputs: Ask Gemini to find all HTML elements where the tag is input and the type attribute is set to \"text\".\nExtract characteristics: For each identified text input, ask Gemini to extract the following information (if available):\nid attribute (if present)\nname attribute (if present)\nplaceholder attribute (if present)\nGenerate dummy code: Based on the extracted information, ask Gemini to generate corresponding dummy code snippets for each text input element. The dummy code should include:\nA comment explaining the original HTML element.\nA line of code demonstrating how to access the text input element using its id or name attribute (if available).\nOutput:\n\nA list of text input elements with their characteristics.\nCorresponding dummy code snippets for each identified text input element.\nExample:\n\nInput:\n\nHTML\n<div>\n  <label for=\"username\">Username:</label>\n  <input type=\"text\" id=\"username\" name=\"user_name\" placeholder=\"Enter your username\">\n</div>\nUse code with caution.\ncontent_copy\nDesired Output:\n\nList of text inputs:\n<input type=\"text\" id=\"username\" name=\"user_name\" placeholder=\"Enter your username\">\nDummy code snippets:\nPython\n# This line corresponds to the username text input element with id \"username\"\nusername_element = driver.find_element_by_id(\"username\")\n\n# This line corresponds to the username text input element with name \"user_name\"\nusername_element = driver.find_element_by_name(\"user_name\")",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Please provide the HTML code you would like me to analyze. I will then:\n\n1. **Identify text input elements:** Find all `<input type=\"text\">` elements in the provided code.\n2. **Extract characteristics:** For each identified input, I will extract its `id`, `name`, and `placeholder` attributes (if present).\n3. **Generate dummy code:** Based on the extracted information, I will create code snippets (in Python or JavaScript) demonstrating how to access the input element using its `id` or `name` attribute.\n\nI'm ready to help! 😊 \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "<!DOCTYPE html>\n<html>\n<head>\n<title>Test Form</title>\n</head>\n<body>\n  <form>\n    <label for=\"firstname\">First Name:</label>\n    <input type=\"text\" id=\"firstname\" name=\"first_name\" placeholder=\"Enter your first name\">\n    <br>\n    <label for=\"lastname\">Last Name:</label>\n    <input type=\"text\" name=\"last_name\" placeholder=\"Enter your last name\">\n  </form>\n</body>\n</html>\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "## List of text inputs:\n\n1. `<input type=\"text\" id=\"firstname\" name=\"first_name\" placeholder=\"Enter your first name\">`\n2. `<input type=\"text\" name=\"last_name\" placeholder=\"Enter your last name\">`\n\n## Dummy Code Snippets (Python):\n\n**1. First Name Input:**\n\n```python\n# This line corresponds to the first name input element with id \"firstname\"\nfirstname_element = driver.find_element_by_id(\"firstname\")\n\n# This line corresponds to the first name input element with name \"first_name\"\nfirstname_element = driver.find_element_by_name(\"first_name\")\n```\n\n**2. Last Name Input:**\n\n```python\n# This line corresponds to the last name input element with name \"last_name\"\nlastname_element = driver.find_element_by_name(\"last_name\")\n```\n\n**Notes:**\n\n* These code snippets assume you are using a web automation library like Selenium (with `driver` representing the WebDriver instance).\n* The second input element lacks an `id` attribute, so we can only access it using its `name`.\n* The `placeholder` attribute is not used in the dummy code examples, but it can be helpful for providing user guidance. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "generate only dummy data in json format for the inputs in the html code\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"first_name\": \"John\",\n  \"last_name\": \"Doe\"\n}\n```\n\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "generate sample inputs while keeping in consideration the different factors that may compromise the website ",
        "Here are some sample inputs designed to test the robustness of your website, considering various factors that could lead to breakage:\n\n**1.  Basic & Valid:**\n\n```json\n{\n  \"first_name\": \"John\",\n  \"last_name\": \"Doe\"\n}\n```\n\n**2.  Edge Cases:**\n\n* **Short Names:** \n  ```json\n  {\n    \"first_name\": \"J\",\n    \"last_name\": \"D\"\n  }\n  ```\n* **Long Names:** \n  ```json\n  {\n    \"first_name\": \"Johnathon\", \n    \"last_name\": \"Doe-Smith-Jr\"\n  }\n  ```\n* **Special Characters:**\n  ```json\n  {\n    \"first_name\": \"Jöhn\",\n    \"last_name\": \"Döé\"\n  }\n  ```\n\n**3.  Invalid Inputs (Potential Breakage):**\n\n* **Empty Values:**\n  ```json\n  {\n    \"first_name\": \"\",\n    \"last_name\": \"\"\n  }\n  ```\n* **Numbers Only:**\n  ```json\n  {\n    \"first_name\": \"12345\",\n    \"last_name\": \"67890\"\n  }\n  ```\n* **Special Characters (Unescaped):**\n  ```json\n  {\n    \"first_name\": \"John<script>alert('Gotcha!')</script>\",\n    \"last_name\": \"Doe\"\n  }\n  ```\n* **Extremely Long Strings:** (Exceeding field length limits)\n  ```json\n  {\n    \"first_name\": \" \".repeat(256), // 256 spaces\n    \"last_name\": \" \".repeat(512) // 512 spaces\n  }\n  ```\n* **Non-printable Characters:** (Including control characters, etc.)\n  ```json\n  {\n    \"first_name\": \"\\x08John\\x08\", // Backspace characters\n    \"last_name\": \"\\x03Doe\\x03\" // Control characters\n  }\n  ```\n\n**Important Considerations:**\n\n* **Server-Side Validation:** Ensure your backend has robust validation to catch invalid inputs and prevent potential security vulnerabilities (e.g., cross-site scripting attacks).\n* **User Experience:** Aim to provide clear error messages and guidance to the user if their input is invalid. \n* **Database Integrity:**  Be aware of the constraints of your database and design your input fields accordingly to prevent data corruption. \n\n\nRemember to thoroughly test your website with a variety of input scenarios like these. \n",
        "give all sample inputs as single json object\n,generate a comprehensive set of testdata contained as an array of json objects with each input element name being the key. Display only the array data\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n[\n  {\n    \"first_name\": \"John\",\n    \"last_name\": \"Doe\"\n  },\n  {\n    \"first_name\": \"J\",\n    \"last_name\": \"D\"\n  },\n  {\n    \"first_name\": \"Johnathon\", \n    \"last_name\": \"Doe-Smith-Jr\"\n  },\n  {\n    \"first_name\": \"Jöhn\",\n    \"last_name\": \"Döé\"\n  },\n  {\n    \"first_name\": \"\",\n    \"last_name\": \"\"\n  },\n  {\n    \"first_name\": \"12345\",\n    \"last_name\": \"67890\"\n  },\n  {\n    \"first_name\": \"John<script>alert('Gotcha!')</script>\",\n    \"last_name\": \"Doe\"\n  },\n  {\n    \"first_name\": \" \".repeat(256), \n    \"last_name\": \" \".repeat(512) \n  },\n  {\n    \"first_name\": \"\\x08John\\x08\", \n    \"last_name\": \"\\x03Doe\\x03\" \n  }\n]\n``` \n",
      ],
    },
  ]
)
st.session_state['history']=[]


for message in chat_session.history:
    role="model" if message.role=='model' else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

print(chat_session.history)
if "app_key" in st.session_state:
    if prompt:=st.chat_input(''):
        prompt=prompt.replace('\n',' \n')
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message("model"):
        message_placeholder=st.empty()
        message_placeholder.markdown("Generating dummy data")
        try:
            response=""
            if prompt!=None:
                for chunk in chat_session.send_message(content=prompt,stream=True,safety_settings={ HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,}):
                     for word in chunk.text:
                         response+=word
                         message_placeholder.markdown(response)
                         print(response)
                    
            message_placeholder.markdown(response)
            
        except Exception as e:
            st.exception(e)
        st.session_state.history=chat_session.history

