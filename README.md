README FOR SPRINT 1.2

Python verision: 3.11

imported libaries: google.generativeai as genai , os , json , spilte3 , from typing import tuple

API key is located in git ignore and has been DM'd to you via slack per Sprint 1 instructions

Running: only requires the libaries stated above and the project files and the API key within your slack inbox 

reason why I choose my LLM/AI model : after expiriting with a the models in this class and another one COMP 399 ( Foundations of Mordern AI ). I ultimately settled with the google AI due to its easy of use in setting up in PyCharm and generally 
and over all liking the way the model operates. Compared to the other model options provided to us for this Sprint. 

For my prompt to generate the resume I first started simple with "resume in markdown format" to ensure it would be created and inputed into the text file correctly, afterwards I then prompted it for a sample resume based on someone trying to get hired 
for the role of junior software engineer to which it modified the resume according then finally I loaded in the json job data and asked it to base the resume off of the job data provided to it. 

Sprint 2 notes: created sqlfunctions which holds functions to open and close the database and the functions to create the tables with columns, test.py contains the pytest functions needed per Sprint 2 instructions and all test cases pass, and load_json.py contains the functions that loads the json data in from both job data files 
