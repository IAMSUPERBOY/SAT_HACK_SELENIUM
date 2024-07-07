# Testcase generator
## Objective:
The user can provide the link of the website that needs to be tested. The selenium framework is used for parsing the web page and then returns its source code. This is then used as part of a prompt given to the Gemini model. This generates the required testcases in the form of an array of JSON objects that can be used to test application. 

Presently the application simply generates the testcases which can be then be copied from Streamlit frontend. Additional functionality intended would be making selenium use the dummy data in testing the app. This functionality is still in progress.

Required packages need to be installed. And don't forget to add your Gemini API key.

It can be run by executing 
```python3 -m streamlit run selenium_added.py```

Frontend: Streamlit

LLM model used: Gemini Pro 1.5
 
[screen-capture (1).webm](https://github.com/IAMSUPERBOY/SAT_HACK_SELENIUM/assets/117973059/b992ff6a-2b1e-4c90-8e50-61fe6834b00c)
