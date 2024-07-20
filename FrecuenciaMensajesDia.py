import pandas as pd  # pandas library for data manipulation / librería pandas para manipulación de datos
import matplotlib.pyplot as plt  # matplotlib library for plotting / librería matplotlib para creación de gráficos
import re  # regular expressions library for pattern matching / librería expresiones regulares para búsqueda de patrones
from collections import Counter  # Counter class for counting elements / Clase Counter para conteo de elementos
import nltk  # Natural Language Toolkit library for text processing / Biblioteca Natural Language Toolkit para procesamiento de texto
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # VADER sentiment analyzer / Analizador de sentimiento VADER
nltk.download('vader_lexicon')  # Download VADER lexicon for sentiment analysis / Descarga léxico VADER para análisis de sentimiento

# Load the chat data / Cargar el archivo de chat
file_path = r'ChatWhatsApp.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    chat_data = file.readlines()

# Function to clean and structure the chat data / Función para limpiar y estructurar los datos del chat
def preprocess_chat(chat_data):
    messages = []
    date_time_pattern = r'^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s?[ap]\.?\s?[mM]\.?\s?-'  # Date and time pattern regex / Patrón regex para fecha y hora
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
                print(f"Error processing line: {line}")  # Error processing line
                print(f"Exception: {e}")  # Exception
                pass
        else:
            if current_date and current_sender:
                messages[-1][2] += ' ' + line.strip()  # Concatenate messages for a sender in the same line / Concatenar mensajes de un remitente en la misma línea
            else:
                print(f"Line does not match the pattern: {line}")  # Line does not match the pattern

    return pd.DataFrame(messages, columns=['Date', 'Sender', 'Message'])

# Clean and structure the data / Limpiar y estructurar los datos
chat_df = preprocess_chat(chat_data)

if chat_df.empty:
    print("No messages found in the file.")  # No messages found in the file
else:
    # Step 4: Analysis of message frequency by day/month / Paso 4: Análisis de la frecuencia de mensajes por día/mes

    # Convert 'Date' column to datetime format / Convertir la columna 'Fecha' a formato datetime
    chat_df['Date'] = pd.to_datetime(chat_df['Date'], format='%d/%m/%Y')

    # Count messages by date / Contar mensajes por fecha
    date_counts = chat_df['Date'].dt.date.value_counts().sort_index()  # Group by date and sort chronologically

    # Create a DataFrame with dates and message counts / Crear un DataFrame con fechas y conteos de mensajes
    date_counts_df = pd.DataFrame({'Date': date_counts.index, 'Count': date_counts.values})

    # Save the DataFrame to an Excel file / Guardar el DataFrame en un archivo Excel
    output_file_path = 'frecuencia_mensajes_por_dia.xlsx'
    date_counts_df.to_excel(output_file_path, index=False)

    # Display the message frequency table by day for verification / Mostrar la tabla de frecuencia de mensajes por día para verificar los datos
    print(date_counts_df)

    # Plot of message frequency by day / Plot de la frecuencia de mensajes por día
    if not date_counts.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(date_counts.index, date_counts.values, marker='o')
        plt.title('Message Frequency by Day / Frecuencia de mensajes por día')
        plt.xlabel('Date / Fecha')
        plt.ylabel('Number of Messages / Cantidad de mensajes')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("No message frequency data to show.")  # No hay datos de frecuencia de mensajes para mostrar.
