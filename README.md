# Mytool Instructions
This tool is built using google's gemini api and it has basically two tools
1) Weather tool
   It answers all the weather related queries for a perticular city.
2) run comand tool
   It runs comand automatically and performs lots of task automatically based on user query.
   Examples:
   1) If I ask it to install git in my system. It will run the required comands in the system and it will complete the task for me.
   2) If I ask it to move some files to a perticular folder, it will do the task for me.

## Installation

1.  Install the required packages using pip:

   ```bash
   cd Tooling
   pip install -r requirements.txt
   ```

## Usage
1.  update your gemini api key in .env
   
2.  Run my-tool:

   ```bash
   python my-tool.py
   ```
