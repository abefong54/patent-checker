# patent-checker

This app creates a basic ui to input a patent publication id and a company name, and does a basic text similiarity search to confirm the most

CREATE LOCAL ENV USING CONDA
`conda create -n myenv python=3.11`
`conda activate myenv`
in conda env:
`pip install -r requirements.txt`

and to view changes in localhost:8501 run:
`streamlit run app.py`
The easiest wayt o run

# Docker Setup

To run the app in a docker container run this command to build the docker image:
`docker build -t patent_checker_app .`

If successful, run this command to view the app in localhost:8501
`docker run -p 8501:8501 patent_checker_app`
