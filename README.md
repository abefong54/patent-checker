# patent-checker

This app creates a basic ui to input a patent publication id and a company name, and does a basic text similiarity search to confirm the most
The app is live here:<br /> `https://fong-patent-checker.streamlit.app/`

# LOCAL SET UP

Install Conda

Mac: https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html <br />
Windows: https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html<br />
Linux: https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html<br />

Create a conda environment using terminal:<br />

`conda create -n myenv python=3.11`
`conda activate myenv`

In the conda env install requirements:<br />

`pip install -r requirements.txt`

To view and test the app run:<br />
`streamlit run app.py`
<br />
(if streamlit command not found, try adding it manually: `pip install streamlit`)
<br />
You should see the app in your browser at : http://localhost:8501

# Docker Setup

To run the app in a docker container run this command to build the docker image:<br />
`docker build -t patent_checker_app .`

If successful, run this command to view the app in localhost:8501<br />
`docker run -p 8501:8501 patent_checker_app`

# NOTE

In order for your app to run locally you need to set an api key for OpenAI in the key variable on line 16 in app.py.<br />
You can generate a free key if you login to open ai, create a new project, and navigate to keys.
`https://community.openai.com/t/how-to-generate-openai-api-key/401363`
