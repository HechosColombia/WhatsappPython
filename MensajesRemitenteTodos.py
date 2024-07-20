import pandas as pd  # Import the pandas library for data manipulation / Importar la librería pandas para manipulación de datos
import numpy as np  # Import the NumPy library for numerical operations / Importar la librería NumPy para operaciones numéricas
import matplotlib.pyplot as plt  # Import the matplotlib library for plotting / Importar la librería matplotlib para creación de gráficos
import re  # Import the regular expressions library for pattern matching / Importar la librería expresiones regulares para búsqueda de patrones
from collections import Counter  # Import the Counter class for counting elements / Importar la clase Counter para conteo de elementos
import nltk  # Import the Natural Language Toolkit library for text processing / Importar la biblioteca Natural Language Toolkit para procesamiento de texto
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # Import the VADER sentiment analyzer / Importar el analizador de sentimiento VADER
nltk.download('vader_lexicon')  # Download the VADER lexicon for sentiment analysis / Descargar el léxico VADER para análisis de sentimiento

# Load the chat data / Cargar los datos del chat
file_path = r'ChatWhatsApp.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    chat_data = file.readlines()

# Function to clean and structure the chat data / Función para limpiar y estructurar los datos del chat
def preprocess_chat(chat_data):
    messages = []
    date_time_pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), \d{1,2}:\d{2}\s?[ap]\.?\s?[mM]\.?\s?-'  # Date and time pattern regex / Patrón regex para fecha y hora
    current_date = None
    current_sender = None

    for line in chat_data:
        line = re.sub(r'\u2009|\u202F', ' ', line)  # Replace special thin space characters / Reemplazar caracteres especiales de espacio fino
        match = re.match(date_time_pattern, line)

        if match:
            try:
                date_time, message = line.split(' - ', 1)
                date_time = date_time.strip()
                if ':' in message:
                    sender, message = message.split(': ', 1)
                else:
                    sender = 'Sistema'
                current_date = date_time.split(',')[0]  # Extract only date / Obtener solo la fecha
                current_sender = sender
                messages.append([current_date, current_sender, message.strip()])
            except Exception as e:
                print(f"Error processing line: {line}")  # Error processing line / Error al procesar la línea
                print(f"Exception: {e}")  # Exception / Excepción
                pass
        else:
            if current_date and current_sender:
                messages[-1][2] += ' ' + line.strip()  # Concatenate messages for a sender in the same line / Concatenar mensajes de un remitente en la misma línea
            else:
                print(f"Line does not match the pattern: {line}")  # Line does not match the pattern / Línea no coincide con el patrón
    return pd.DataFrame(messages, columns=['Date', 'Sender', 'Message'])

# Clean and structure the data / Limpiar y estructurar los datos
chat_df = preprocess_chat(chat_data)

if chat_df.empty:
    print("No messages found in the file.")  # No se encontraron mensajes en el archivo.
else:
    # Convert 'Date' column to datetime format / Convertir la columna 'Date' a formato datetime
    chat_df['Date'] = pd.to_datetime(chat_df['Date'], format='%d/%m/%Y')

    # Filter data starting from 01/01/2022 / Filtrar datos a partir del 01/01/2022
    filtered_chat_df = chat_df[chat_df['Date'] >= '2022-01-01']

    if filtered_chat_df.empty:
        print("No messages found starting from 01/01/2022.")  # No se encontraron mensajes a partir del 01/01/2022.
    else:
        # Calculate message frequency for each sender / Calcular la frecuencia de mensajes para cada remitente
        sender_counts = filtered_chat_df['Sender'].value_counts()

        # Select the top 12 senders / Seleccionar los 12 principales remitentes
        top_senders = sender_counts.head(12).index

        # Create a figure for subplots / Crear una figura para los subplots
        fig, axs = plt.subplots(4, 3, figsize=(15, 15))

        for i, sender in enumerate(top_senders):
            sender_data = filtered_chat_df[filtered_chat_df['Sender'] == sender]
            date_counts = sender_data['Date'].dt.date.value_counts().sort_index()

            # Calculate the trendline / Calcular la línea de tendencia
            trend_line_degree = 1  # Degree of the polynomial for the trendline (linear in this case) / Grado del polinomio para la línea de tendencia (lineal en este caso)
            trend_coefficients = np.polyfit(range(len(date_counts)), date_counts.values, trend_line_degree)
            trend_poly = np.poly1d(trend_coefficients)

            # Plot the message frequency by day for each sender / Gráfico de la frecuencia de mensajes por día para cada remitente
            ax = axs[i // 3, i % 3]
            ax.plot(date_counts.index, date_counts.values, marker='o', label='Original data / Datos originales')
            ax.plot(date_counts.index, trend_poly(range(len(date_counts))), color='red', linestyle='--', label='Trendline / Línea de tendencia')
            ax.set_title(f'{sender} - Message frequency trend by day / {sender} - Tendencia de mensajes por día')
            ax.set_xlabel('Date / Fecha')
            ax.set_ylabel('Number of messages / Cantidad de mensajes')
            ax.grid(True)
            ax.legend()

            # Rotate the dates on the x-axis / Rotar las fechas en el eje x
            ax.tick_params(axis='x', rotation=45)

        # Adjust figure layout / Ajustar el diseño de la figura
        fig.tight_layout()

        # Save the figure as an image / Guardar la figura como una imagen
        plt.savefig('tendencias_top_remitentes.jpg')

        # Show the figure / Mostrar la figura
        plt.show()
