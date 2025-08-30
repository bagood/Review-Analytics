# Review-Analytics

This project provides a complete, end-to-end pipeline for gathering, analyzing, and visualizing restaurant reviews. It automates the process of scraping review data, leverages a Large Language Model (LLM) to extract and summarize key insights, and presents the findings in a beautiful, interactive dashboard built with Streamlit.


✨ Features
Automated Data Scraping: A script to efficiently collect review data from various sources.
Intelligent LLM Analysis: Utilizes a Large Language Model to process raw text reviews, summarizing them and grouping feedback into relevant categories (e.g., Food, Ambience, Service, Price).
Interactive Dashboard: A user-friendly web-based dashboard to visualize sentiment analysis, popular menu items, and overall restaurant performance.


🛠️ Tech Stack
Python 3.13
Conda for environment management
Streamlit for the interactive dashboard
Python-dotenv for managing environment variables
Large Language Model (LLM) for text analytics


🚀 Getting Started
Follow these instructions to set up the project environment and get it running on your local machine.
Prerequisites
You must have Anaconda or Miniconda installed to manage the environment.
Installation & Configuration
Clone the Repository
```
git clone https://github.com/bagood/Review-Analytics.git
cd Review-Analytics
```

Create a Conda Environment
Create a new Conda environment with Python 3.13. We'll name it review-analyzer.
```
conda create --name Review-Analytics-Env python=3.13
```

Activate the Environment
You must activate the environment before installing dependencies and running the scripts.
```
conda activate Review-Analytics-Env
```

Install Required Packages
Install all the necessary libraries from the requirements.txt file.
```
pip install -r requirements.txt
```


Configure Environment Variables
This project requires API credentials to connect to the LLM.
Create a new file named .env in the root directory of the project.
Open the .env file and add your credentials in the following format:
```
OPENAI_API_KEY="your_api_key_here"
CUSTOM_ENDPOINT="your_custom_endpoint_url_here"
```
Replace the placeholder values with your actual API key and endpoint. The application will load these variables automatically.

🏃‍♂️ Running the Program
The program is designed to be run in three distinct steps. Please execute them in the following order.
Step 1: Perform Data Scraping
This script will collect the raw review data and save it locally.
```
python3 executeDataCollection.py
```


Step 2: Perform Data Processing with LLM
This script will use the credentials from your .env file to connect to the LLM, process the scraped data, and prepare it for the dashboard.
```
python3 executeReviewAnalytics.py
```


Step 3: Initialize the Dashboard
This command starts the Streamlit server and opens the interactive dashboard in your default web browser.
```
streamlit run dashboardFunctions/main.py
```

After running the final command, you can navigate to the local URL provided in your terminal (usually http://localhost:8501) to view and interact with your dashboard.
