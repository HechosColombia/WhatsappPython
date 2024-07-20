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
        date_counts = filtered_chat_df['Date'].dt.date.value_counts().sort_index()

        # Crear un DataFrame con las fechas y la cantidad de mensajes
        date_counts_df = pd.DataFrame({'Date': date_counts.index, 'Count': date_counts.values})

        # Guardar el DataFrame en un archivo Excel
        output_file_path = 'frecuencia_mensajes_por_dia.xlsx'
        date_counts_df.to_excel(output_file_path, index=False)

        # Mostrar la tabla de frecuencia de mensajes por día para verificar los datos
        print(date_counts_df)
        # Calcular la línea de tendencia
        trend_line_degree = 1  # Grado del polinomio para la línea de tendencia (lineal en este caso)
        trend_coefficients = np.polyfit(range(len(date_counts)), date_counts.values, trend_line_degree)
        trend_poly = np.poly1d(trend_coefficients)

        # Plot de la frecuencia de mensajes por día
        if not date_counts.empty:
            plt.figure(figsize=(10,6))
            plt.plot(date_counts.index, date_counts.values, marker='o', label='Datos originales')
            plt.plot(date_counts.index, trend_poly(range(len(date_counts))), color='red', linestyle='--', label='Línea de tendencia')
            plt.title('Frecuencia de mensajes por día con línea de tendencia')
            plt.xlabel('Fecha')
            plt.ylabel('Cantidad de mensajes')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()
            plt.tight_layout()  # Ajuste para evitar superposición de elementos
            plt.savefig('frecuencia_mensajes_con_tendencia.jpg')  # Guardar como imagen JPG
            plt.show()
        else:
            print("No hay datos de frecuencia de mensajes para mostrar.")