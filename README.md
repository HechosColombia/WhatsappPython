### This read me is in english in the first part and in spanish in the lower part
### este readme esta en ingles en la parte puperior y en ingles en la parte de abajo
# ENGLISH
# WhatsApp Chat Analyzer

This repository contains Python scripts for analyzing data from a WhatsApp chat export file.

## Description:

This project provides several functionalities for analyzing your WhatsApp chat data. You can:

- Identify the most frequent senders and visualize the distribution of messages.
- Analyze the most common words used by each sender.
- Perform sentiment analysis to understand the overall sentiment of the conversation.
- Visualize the frequency of messages by day/month, with the option to include a trend line.
- Analyze message trends for the top 12 senders (for data after a specified date).

## Requirements:

- Python 3.x
- `pandas` library
- `matplotlib` library
- `nltk` library
- `re` library
- `collections` library (included in Python)

## Installation:

1. Clone this repository to your local machine.
2. Open a terminal or command prompt and navigate to the repository directory.
3. Install the required libraries using pip:
    ```sh
    pip install pandas matplotlib nltk
    ```

## Usage:

1. Make sure you have a text file containing your WhatsApp chat data exported without media.
2. Rename the file to `ChatWhatsApp.txt` and place it in the same directory as the Python scripts.
3. Run the desired script from the command line. For example, to analyze message counts and common words:

    - `CantidadMensajesIndividual.py`: Analyzes message counts by sender and common words for all senders.
    - `CantidadMensajesMienbrosPalabras.py`: Similar to `CantidadMensajesIndividual.py` but analyzes common words for all messages.
    - `FrecuenciaMensajesDia.py`: Analyzes message frequency by day/month and saves the results to an Excel file.
    - `FrecuenciaMensajesDiaTendencia.py`: Similar to `FrecuenciaMensajesDia.py` but includes a trend line in the visualization and saves it as a JPG image.
    - `MensajesRemitenteTodos.py`: Analyzes message frequency trend for the top 12 senders (data after a specified date) and saves the visualization as a JPG image.

## Note:

The scripts assume a specific format for the WhatsApp chat export file. Make sure your file follows this format for accurate results. You can modify the scripts to customize the analysis based on your needs.

## Additional Information:

The `nltk.download('vader_lexicon')` line in the scripts downloads a sentiment lexicon used for sentiment analysis. This might require an internet connection the first time you run the scripts.

I hope this README provides a clear understanding of the project and its functionalities. Feel free to explore the code and adapt it to your specific requirements!


# ESPAÑOL
## Analizador de Chats de WhatsApp

Este repositorio contiene scripts Python para analizar datos exportados de tus chats de WhatsApp.

## Descripción

Este proyecto ofrece diversas funcionalidades para analizar los datos de tus chats de WhatsApp. Puedes:

* **Identificar a los remitentes más frecuentes** y visualizar la distribución de mensajes.
* **Analizar las palabras más comunes utilizadas por cada remitente**.
* **Realizar un análisis de sentimiento** para comprender el sentimiento general de la conversación.
* **Visualizar la frecuencia de mensajes por día/mes**, con la opción de incluir una línea de tendencia.
* **Analizar las tendencias de mensajes para los 12 remitentes principales** (para datos posteriores a una fecha específica).

## Requisitos

* Python 3.x
* **Biblioteca pandas** (`pip install pandas`)
* **Biblioteca matplotlib** (`pip install matplotlib`)
* **Biblioteca nltk** (`pip install nltk`)
* **Biblioteca re** (incluida en Python)
* **Biblioteca collections** (incluida en Python)

## Instalación

1. Clona este repositorio en tu máquina local.
2. Abre una terminal o línea de comandos y navega hasta el directorio del repositorio.
3. Instala las bibliotecas requeridas usando pip:
   ```bash
   pip install pandas matplotlib nltk
## Uso

1. Asegúrate de tener un archivo de texto con los datos de tu chat de WhatsApp exportados sin medios.
2. Renombra el archivo a "ChatWhatsApp.txt" y colócalo en el mismo directorio que los scripts de Python.
3. Ejecuta el script deseado desde la línea de comandos. Por ejemplo:

   * **`CantidadMensajesIndividual.py`**: Analiza el conteo de mensajes por remitente y las palabras más comunes para todos los remitentes.
   * **`CantidadMensajesMienbrosPalabras.py`**: Similar a `CantidadMensajesIndividual.py` pero analiza las palabras comunes para todos los mensajes.
   * **`FrecuenciaMensajesDia.py`**: Analiza la frecuencia de mensajes por día/mes y guarda los resultados en un archivo Excel.
   * **`FrecuenciaMensajesDiaTendencia.py`**: Similar a `FrecuenciaMensajesDia.py` pero incluye una línea de tendencia en la visualización y la guarda como una imagen JPG.
   * **`MensajesRemitenteTodos.py`**: Analiza la tendencia de frecuencia de mensajes para los 12 remitentes principales (datos posteriores a una fecha específica) y guarda la visualización como una imagen JPG.
## Nota:

Los scripts asumen un formato específico para el archivo de exportación de chats de WhatsApp. Asegúrate de que tu archivo cumpla con este formato para obtener resultados precisos. Puedes modificar los scripts para adaptar el análisis a tus necesidades específicas.

## Información adicional:

La línea `nltk.download('vader_lexicon')` en los scripts descarga un léxico de sentimientos esencial para el análisis de sentimientos. Esto podría requerir una conexión a internet la primera vez que ejecutes los scripts.

Espero que este README te brinde una comprensión clara del proyecto y sus funcionalidades. ¡No dudes en explorar el código y adaptarlo a tus necesidades específicas!

