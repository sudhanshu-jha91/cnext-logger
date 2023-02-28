# Flask-ClickHouse-Logging

Flask-ClickHouse-Logging is a sample Flask application that logs messages to ClickHouse, and allows you to retrieve and filter those logs using a REST API.

## Getting started
To get started with Flask-ClickHouse-Logging, follow these steps:

Clone the repository to your local machine
Install the required packages listed in requirements.txt
Set up your ClickHouse database and create a table for storing logs (see below for an example schema)
Update the configuration file (config.py) with your ClickHouse database details
Start the Flask application using python app.py
Send log messages to the /logs endpoint using a POST request
Retrieve logs using a GET request to the /logs endpoint

## Logging
To send log messages to the Flask-ClickHouse-Logging application, send a POST request to the /logs-ingest endpoint with a JSON payload containing the following fields:

level: the log level (e.g. INFO, WARNING, ERROR)
message: the log message
created_at: the timestamp when the log message was created (in ISO format)
source : source from where it was hit
For example:

json`
{
    "level": "INFO", 
    "message": "Hello, world!",
    "created_at": "2023-02-28T15:30:00Z"
    "extra_info": " Hello world from function"
    "source":" Backend call"
}
`
## Retrieving logs
To retrieve logs from the Flask-ClickHouse-Logging application, send a GET request to the /logs endpoint with the following query parameters:

page: the page number to retrieve (default: 1)
page_size: the number of logs to retrieve per page (default: 20)
level: filter logs by log level (e.g. INFO, WARNING, ERROR)
message: filter logs by message text (substring match)
search: search for logs that match the given text (substring match)
The response will be a JSON object containing the following fields:

logs: an array of log messages, sorted by descending timestamp (most recent first)
page: the current page number
page_size: the number of logs per page
total_pages: the total number of pages
Each log message is represented as a JSON object with the following fields:

level: the log level
extra_info: extra_info you want
message: the log message
created_at: the timestamp when the log message was created (in ISO format)

http://log-service:5000/logs?page=<page_number>&page_size=<page_size>&level=<level>&message=<message>&search=<search>&extra_info=<extra_info>

## ClickHouse schema
Here is an example ClickHouse schema for storing log messages:

CREATE DATABASE cnext_logs;

CREATE TABLE log_data (
    id UUID,
    level String,
    extra_info String,
    message String,
    created_at DateTime,
    source String 
) ENGINE = MergeTree()
ORDER BY (created_at, id)
SETTINGS index_granularity = 8192;

