# MyAskJB

My take on the AskJB AI chatbot using Python, Scrapy, LangChain, ChromaDB and StreamLit UI

## Environment variables

To run this project, you will need to add the following variables to your .env file

`CHROMA_PATH`: The path to your chroma db folder.

`DATA_PATH`: The path to your folder containing the resulting data from the webscraping. 

## Requirements

[Python 3.10 + ](https://www.python.org/downloads/)

[Microsoft C++ build tools](https://visualstudio.microsoft.com/pt-br/downloads/?q=build+tools)

[Llama3 local rest API](https://ollama.com/download)
## Quick start

Clone the project:

```bash
  git clone https://github.com/pedro-ggomes/MyAskJB.git
```

Cd into project folder:

```bash
  cd my-project
```
Create Python virtual environment:

```bash
python -m venv env
```
Activate virtual environment:

Windows PowerShell:
```bash
.\env\Scripts\Activate.ps1 
```
Install the dependencies:

```bash
  pip install -r requirements.txt
```

Get all the the urls you want to scrap from and add them to the links.txt file (there's a get_urls.js demonstrating how I did it for the jitterbit success central documentation), after that go into the Scraper folder:

```bash
  cd Scrape_Jitterbit
```

Run the custom spider that will crawl and gather all the data you want from the links provided:

```bash
  scrapy crawl multi_url_spider -o <output-filename>.json
```

If you want to break up the output into chunks add FEED_EXPORT_BATCH_ITEM_COUNT = 100 to scrapy's settings.py and run:

```bash
  scrapy crawl multi_url_spider -o path-to-output-folder%(batch_id)d-filename%(batch_time)s.json
```
After scraping your documentation of choice download and install ollama llm and run:
```bash
ollama pull mistral
```
Then:
```bash
ollama serve
```
When that is finished run (this will take a long time depending on your computer's configurations):
```bash
python populate_database.py
```
Now for the last step run:
```bash
streamlit run app.py
```
## Screenshots

![App Screenshot](https://i.ibb.co/zPd7q5Q/jitterbit-doc-bot-demo.png)

