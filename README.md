Title: WhatsApp Chat Analyzer

This repository contains Python scripts for analyzing data from a WhatsApp chat export file.

Description:

This project provides several functionalities for analyzing your WhatsApp chat data. You can:

Identify the most frequent senders and visualize the distribution of messages.
Analyze the most common words used by each sender.
Perform sentiment analysis to understand the overall sentiment of the conversation.
Visualize the frequency of messages by day/month, with the option to include a trend line.
Analyze message trends for the top 12 senders (for data after a specified date).
Requirements:

Python 3.x
pandas library
matplotlib library
nltk library
re library
collections library (included in Python)
Installation:

Clone this repository to your local machine.
Open a terminal or command prompt and navigate to the repository directory.
Install the required libraries using pip:
pip install pandas matplotlib nltk
Usage:

Make sure you have a text file containing your WhatsApp chat data exported without media.
Rename the file to ChatWhatsApp.txt and place it in the same directory as the Python scripts.
Run the desired script from the command line. For example, to analyze message counts and common words:

CantidadMensajesIndividual.py: Analyzes message counts by sender and common words for all senders.
CantidadMensajesMienbrosPalabras.py: Similar to CantidadMensajesIndividual.py but analyzes common words for all messages.
FrecuenciaMensajesDia.py: Analyzes message frequency by day/month and saves the results to an Excel file.
FrecuenciaMensajesDiaTendencia.py: Similar to FrecuenciaMensajesDia.py but includes a trend line in the visualization and saves it as a JPG image.
MensajesRemitenteTodos.py: Analyzes message frequency trend for the top 12 senders (data after a specified date) and saves the visualization as a JPG image.
Note:

The scripts assume a specific format for the WhatsApp chat export file. Make sure your file follows this format for accurate results.
You can modify the scripts to customize the analysis based on your needs.
Additional Information:

The nltk.download('vader_lexicon') line in the scripts downloads a sentiment lexicon used for sentiment analysis. This might require an internet connection the first time you run the scripts.
I hope this README provides a clear understanding of the project and its functionalities. Feel free to explore the code and adapt it to your specific requirements!
