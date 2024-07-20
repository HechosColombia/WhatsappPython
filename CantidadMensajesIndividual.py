import pandas as pd
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
    date_time_pattern = r'^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s?[ap]\.?\s?[mM]\.?\s?-'
    current_date_time = None
    current_sender = None

    for line in chat_data:
        line = re.sub(r'\u2009|\u202F', ' ', line)  # Reemplazar caracteres especiales de espacio fino
        if re.match(date_time_pattern, line):
            try:
                date_time, message = line.split(' - ', 1)
                date_time = date_time.strip()
                if ':' in message:
                    sender, message = message.split(': ', 1)
                else:
                    sender = 'Sistema'
                date_time = pd.to_datetime(date_time, format='%d/%m/%Y, %I:%M %p', errors='coerce')
                if pd.isnull(date_time):
                    date_time = pd.to_datetime(date_time, format='%d/%m/%Y, %H:%M %p', errors='coerce')
                current_date_time = date_time
                current_sender = sender
                messages.append([current_date_time, current_sender, message.strip()])
            except Exception as e:
                print(f"Error al procesar la línea: {line}")
                print(f"Excepción: {e}")
                pass
        else:
            if current_date_time and current_sender:
                messages[-1][2] += ' ' + line.strip()
            else:
                print(f"Línea no coincide con el patrón: {line}")
    return pd.DataFrame(messages, columns=['DateTime', 'Sender', 'Message'])

# Limpiar y estructurar los datos
chat_df = preprocess_chat(chat_data)

if chat_df.empty:
    print("No se encontraron mensajes en el archivo.")
else:
    # Paso 3: Análisis del conteo de mensajes por remitente
    message_counts = chat_df['Sender'].value_counts()

    # Plot del conteo de mensajes por remitente
    plt.figure(figsize=(10,6))
    message_counts.plot(kind='bar', color='skyblue')
    plt.title('Conteo de mensajes por remitente')
    plt.xlabel('Remitente')
    plt.ylabel('Cantidad de mensajes')
    plt.xticks(rotation=45)
    plt.show()

    # Paso 5: Análisis de las palabras más comunes por remitente
    def get_most_common_words_by_sender(chat_df, sender, num_words=20):
        sender_messages = chat_df[chat_df['Sender'] == sender]['Message']
        words = ' '.join(sender_messages).lower().split()
        common_words = Counter(words).most_common(num_words)
        return common_words

    senders = chat_df['Sender'].unique()

    # Plot de las palabras más comunes por remitente
    for sender in senders:
        most_common_words_sender = get_most_common_words_by_sender(chat_df, sender, num_words=20)
        words, counts = zip(*most_common_words_sender)
        plt.figure(figsize=(10,6))
        plt.bar(words, counts, color='skyblue')
        plt.title(f'Palabras más comunes por {sender}')
        plt.xlabel('Palabras')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45)
        plt.tight_layout()  # Ajuste para evitar superposición de elementos
        plt.savefig(f'palabras_mas_comunes_{sender}.jpg')  # Guardar como imagen JPG
        plt.show()

    # Paso 6: Análisis de sentimiento
    sentiment_analyzer = SentimentIntensityAnalyzer()
    chat_df['Sentiment'] = chat_df['Message'].apply(lambda x: sentiment_analyzer.polarity_scores(x)['compound'])

    # Plot del análisis de sentimiento
    plt.figure(figsize=(10,6))
    chat_df['Sentiment'].hist(bins=20, color='skyblue')
    plt.title('Distribución del sentimiento de los mensajes')
    plt.xlabel('Sentimiento')
    plt.ylabel('Frecuencia')
    plt.tight_layout()  # Ajuste para evitar superposición de elementos
    plt.savefig('analisis_sentimiento.jpg')  # Guardar como imagen JPG
    plt.show()