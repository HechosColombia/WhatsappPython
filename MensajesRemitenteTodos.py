import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# Cargar el archivo de chat
file_path = r'ChatWhatsApp.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    chat_data = file.readlines()

# Función para limpiar y estructurar los datos del chat
def preprocess_chat(chat_data):
    messages = []
    date_time_pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), \d{1,2}:\d{2}\s?[ap]\.?\s?[mM]\.?\s?-'
    current_date = None
    current_sender = None

    for line in chat_data:
        line = re.sub(r'\u2009|\u202F', ' ', line)  # Reemplazar caracteres especiales de espacio fino
        match = re.match(date_time_pattern, line)
        if match:
            try:
                date_time, message = line.split(' - ', 1)
                date_time = date_time.strip()
                if ':' in message:
                    sender, message = message.split(': ', 1)
                else:
                    sender = 'Sistema'
                current_date = date_time.split(',')[0]  # Obtener solo la fecha
                current_sender = sender
                messages.append([current_date, current_sender, message.strip()])
            except Exception as e:
                print(f"Error al procesar la línea: {line}")
                print(f"Excepción: {e}")
                pass
        else:
            if current_date and current_sender:
                messages[-1][2] += ' ' + line.strip()
            else:
                print(f"Línea no coincide con el patrón: {line}")
    return pd.DataFrame(messages, columns=['Date', 'Sender', 'Message'])

# Limpiar y estructurar los datos
chat_df = preprocess_chat(chat_data)

if chat_df.empty:
    print("No se encontraron mensajes en el archivo.")
else:
    # Paso 4: Análisis de la frecuencia de mensajes por día/mes
    chat_df['Date'] = pd.to_datetime(chat_df['Date'], format='%d/%m/%Y')

    # Filtrar datos a partir del 01/01/2022
    filtered_chat_df = chat_df[chat_df['Date'] >= '2022-01-01']
    
    if filtered_chat_df.empty:
        print("No se encontraron mensajes a partir del 01/01/2022.")
    else:
        # Calcular la frecuencia de mensajes para cada remitente
        sender_counts = filtered_chat_df['Sender'].value_counts()

        # Seleccionar los 12 principales remitentes
        top_senders = sender_counts.head(12).index

        # Crear una figura para los subplots
        fig, axs = plt.subplots(4, 3, figsize=(15, 15))

        for i, sender in enumerate(top_senders):
            sender_data = filtered_chat_df[filtered_chat_df['Sender'] == sender]
            date_counts = sender_data['Date'].dt.date.value_counts().sort_index()

            # Calcular la línea de tendencia
            trend_line_degree = 1  # Grado del polinomio para la línea de tendencia (lineal en este caso)
            trend_coefficients = np.polyfit(range(len(date_counts)), date_counts.values, trend_line_degree)
            trend_poly = np.poly1d(trend_coefficients)

            # Plot de la frecuencia de mensajes por día
            ax = axs[i // 3, i % 3]
            ax.plot(date_counts.index, date_counts.values, marker='o', label='Datos originales')
            ax.plot(date_counts.index, trend_poly(range(len(date_counts))), color='red', linestyle='--', label='Línea de tendencia')
            ax.set_title(f'{sender} - Tendencia de mensajes por día')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Cantidad de mensajes')
            ax.grid(True)
            ax.legend()
            
            # Rotar las fechas en el eje x
            ax.tick_params(axis='x', rotation=45)  # Rotación de 45 grados

        # Ajuste de diseño de la figura
        fig.tight_layout()

        # Guardar la figura como imagen
        plt.savefig('tendencias_top_remitentes.jpg')

        # Mostrar la figura
        plt.show()