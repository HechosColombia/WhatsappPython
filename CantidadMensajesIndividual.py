import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# Load the chat file / Cargar el archivo de chat
file_path = r'ChatWhatsApp.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    chat_data = file.readlines()

# Function to clean and structure chat data / Función para limpiar y estructurar los datos del chat
def preprocess_chat(chat_data):
    messages = []
    date_time_pattern = r'^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s?[ap]\.?\s?[mM]\.?\s?-'
    current_date_time = None
    current_sender = None

    for line in chat_data:
        line = re.sub(r'\u2009|\u202F', ' ', line)  # Replace fine space characters / Reemplazar caracteres especiales de espacio fino
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
                print(f"Error processing line: {line}")  # Error al procesar la línea
                print(f"Exception: {e}")  # Excepción
                pass
        else:
            if current_date_time and current_sender:
                messages[-1][2] += ' ' + line.strip()
            else:
                print(f"Line does not match pattern: {line}")  # Línea no coincide con el patrón
    return pd.DataFrame(messages, columns=['DateTime', 'Sender', 'Message'])

# Clean and structure the data / Limpiar y estructurar los datos
chat_df = preprocess_chat(chat_data)

if chat_df.empty:
    print("No messages found in the file.")  # No se encontraron mensajes en el archivo
else:
    # Step 3: Analysis of message counts by sender / Paso 3: Análisis del conteo de mensajes por remitente
    message_counts = chat_df['Sender'].value_counts()

    # Plot of message counts by sender / Plot del conteo de mensajes por remitente
    plt.figure(figsize=(10,6))
    message_counts.plot(kind='bar', color='skyblue')
    plt.title('Message Counts by Sender')  # Conteo de mensajes por remitente
    plt.xlabel('Sender')  # Remitente
    plt.ylabel('Number of Messages')  # Cantidad de mensajes
    plt.xticks(rotation=45)
    plt.show()

    # Step 5: Analysis of most common words by sender / Paso 5: Análisis de las palabras más comunes por remitente
    def get_most_common_words_by_sender(chat_df, sender, num_words=20):
        sender_messages = chat_df[chat_df['Sender'] == sender]['Message']
        words = ' '.join(sender_messages).lower().split()
        common_words = Counter(words).most_common(num_words)
        return common_words

    senders = chat_df['Sender'].unique()

    # Plot of most common words by sender / Plot de las palabras más comunes por remitente
    for sender in senders:
        most_common_words_sender = get_most_common_words_by_sender(chat_df, sender, num_words=20)
        words, counts = zip(*most_common_words_sender)
        plt.figure(figsize=(10,6))
        plt.bar(words, counts, color='skyblue')
        plt.title(f'Most Common Words by {sender}')  # Palabras más comunes por {sender}
        plt.xlabel('Words')  # Palabras
        plt.ylabel('Frequency')  # Frecuencia
        plt.xticks(rotation=45)
        plt.tight_layout()  # Adjust layout to avoid overlapping elements / Ajuste para evitar superposición de elementos
        plt.savefig(f'most_common_words_{sender}.jpg')  # Save as JPG image / Guardar como imagen JPG
        plt.show()

    # Step 6: Sentiment analysis / Paso 6: Análisis de sentimiento
    sentiment_analyzer = SentimentIntensityAnalyzer()
    chat_df['Sentiment'] = chat_df['Message'].apply(lambda x: sentiment_analyzer.polarity_scores(x)['compound'])

    # Plot of sentiment analysis / Plot del análisis de sentimiento
    plt.figure(figsize=(10,6))
    chat_df['Sentiment'].hist(bins=20, color='skyblue')
    plt.title('Distribution of Message Sentiment')  # Distribución del sentimiento de los mensajes
    plt.xlabel('Sentiment')  # Sentimiento
    plt.ylabel('Frequency')  # Frecuencia
    plt.tight_layout()  # Adjust layout to avoid overlapping elements / Ajuste para evitar superposición de elementos
    plt.savefig('sentiment_analysis.jpg')  # Save as JPG image / Guardar como imagen JPG
    plt.show()
