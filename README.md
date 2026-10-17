## Installation Instructions

This project is a beginner-friendly starter for working with financial data. It has a Streamlit web app (`app.py`, with logic in `src/`) built from the code in the `notebooks/` folder.

## Run the Streamlit app

After installing the packages (steps below), run:

```bash
streamlit run app.py
```

Then enter a ticker (e.g. `MU`), choose an analysis type (filings, news, or stock price ratings) and click **Run**.

- `app.py`: the Streamlit UI in the project root (the file you run).
- `src/analysis.py`: the logic, with functions taken from the notebooks (`get_financials`, `get_news`, `get_price`, `get_analyst_ratings`).
- `src/storage.py`: helpers to build filenames and to save, list and read analyses.

## Save and view previous analyses

After an analysis is displayed, click **Save Analysis**. It is written as a Markdown file (ticker, analysis type, parameters, creation date, results) to the `analyses-data/` folder at the project root, named like `MU_news_20261017-140309.md`. Existing files are never overwritten (a `_2`, `_3`, ... suffix is added if needed).

The **Previous Analyses** section at the bottom of the homepage lists saved analyses newest first. Pick one from the dropdown and click **Show** to open it in a pop-up. If nothing has been saved yet, a message says so.

The folder path is resolved from the location of the code, so it is the same wherever you launch the app from. It is created automatically and ignored by git (`analyses-data/` is in `.gitignore`). It uses the instance's existing disk, so there is no extra setup and no CloudFormation change. The same code runs in GitHub Codespaces and on EC2.

> Files live on the machine running the app. Codespaces and EC2 each have their own `analyses-data/`, and deleting or replacing the instance deletes its saved analyses.

### Verify in Codespaces

1. `streamlit run app.py`, run an analysis (e.g. `MU`, `news`) and click **Save Analysis**. A success message shows the filename.
2. `ls analyses-data/` shows the new `.md` file; `cat` it to check the header and contents.
3. Under **Previous Analyses**, select the entry (nothing appears yet), then click **Show** to see the pop-up.
4. Stop the app, start it again from a different directory (`cd / && streamlit run /workspaces/smu-cce-starter-finn/app.py`); the saved analysis is still listed.

### Verify on EC2

1. Deploy the app as usual (pull the latest code and restart the Streamlit service).
2. Open the app in the browser, run an analysis and click **Save Analysis**.
3. SSH in and run `ls <project folder>/analyses-data/` to see the file.
4. Restart the Streamlit service and reload the page; the analysis is still listed under **Previous Analyses**.

## Installation Instructions

1. Open a terminal in the project folder.

   ```bash
   cd /workspaces/smu-cce-starter-finn
   ```

2. Create a virtual environment so your packages stay organized.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Upgrade pip and install the required packages.

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. If Jupyter is not already available, install it.

   ```bash
   python -m pip install notebook
   ```

5. Start Jupyter and open a notebook.

   ```bash
   jupyter notebook
   ```

6. Open one of the files in the notebooks folder and run the cells from top to bottom.

> You can also explore the raw code by opening the notebooks in Jupyter.

## Code Walkthrough

The main work in this repo lives in the notebooks folder. Each notebook is a small data task that uses Yahoo Finance to pull stock information.

- notebooks/stock_price_ratings.ipynb: gets a stock's current price and shows analyst recommendation data.
- notebooks/news.ipynb: fetches recent news headlines and summaries for a stock ticker.
- notebooks/filings.ipynb: pulls financial statements such as income statements, balance sheets, and cash flow.

Each notebook starts by importing the yfinance library, which connects to Yahoo Finance. The code then defines a function such as get_price(), get_news(), or get_financials(). After that, the notebook calls the function with a stock ticker such as MU or GOOG. The result is printed in the notebook so you can see the raw data in an easy-to-read format.

From start to finish, the workflow is simple:

1. Choose a stock ticker.
2. Run the notebook cell that defines the function.
3. Call the function with the ticker.
4. View the output data in the notebook.
5. Use that data to explore the stock, news, or financial statements.

This is a good starter project for learning how Python notebooks connect to live data, cleanly organize code, and prepare for building a larger financial or cloud-based application later.

 # Cloud Computing for Economics: Starter Repo 

  This repository contains the starter code and lesson materials for building a Python financial-data application and deploying it to AWS.

  Students will use GitHub Codespaces, Python, Jupyter notebooks, Streamlit, Git, and AWS CloudFormation.

  ## Learning outcomes

  By the end of the course, you will be able to:

   1.  Build and deploy an analytics application with a simple Front End / back-end (using AI)
   2.  Host and share the application on a cloud platform (e.g., AWS EC2 or similar) so that others can access it securely over the web
   3.  Integrate data sources and APIs into the app to enable interactive, real-time analytics
   4.  Apply cloud architecture best practices, ensuring the app demonstrates scalability, performance efficiency, and basic security
   5.  Showcase your work on GitHub as part of a personal portfolio, demonstrating practical cloud and analytics skills through a shareable, explorable repository

  
  ## Repository structure

  ```text
  .
  ├── lessons/          # Step-by-step course instructions
  ├── notebooks/        # Starter financial-data notebooks
  ├── app.py            # Streamlit app (run this)
  ├── src/              # Logic (analysis.py)
  ├── requirements.txt  # Python dependencies
  └── README.md         # Course overview