# Testcase generator
## Objective:
The user can provide the link of the website that needs to be tested. The selenium framework is used for parsing the web page and then return its source code. This is then used as a part of a prompt given to gemini model. This then generates the required testcases in the form of an array of json objects that can be used for testing the application. 

At present the application simply generates the testcases it can be then copied from streamlit frontend. Additional functionality intended would be to make selenium use the dummy data in testing the app. This functionality is still in progress.


Frontend: Streamlit

LLM model used: Gemini Pro 1.5
 
