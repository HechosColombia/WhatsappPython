# Import libraries / Importa librerías
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
    current_date_time = None
    current_sender = None

    for line in chat_data:
        line = re.sub(r'\u2009|\u202F', ' ', line)  # Replace special thin space characters / Reemplazar caracteres especiales de espacio fino
        if re.match(date_time_pattern, line):
            try:
                date_time, message = line.split(' - ', 1)
                date_time = date_time.strip()
                if ':' in message:
                    sender, message = message.split(': ', 1)
                else:
                    sender = 'Sistema'
                date_time = pd.to_datetime(date_time, format='%d/%m/%Y, %I:%M %p', errors='coerce')  # Parse date and time / Analizar fecha y hora
                if pd.isnull(date_time):
                    date_time = pd.to_datetime(date_time, format='%d/%m/%Y, %H:%M %p', errors='coerce')
                current_date_time = date_time
                current_sender = sender
                messages.append([current_date_time, current_sender, message.strip()])
            except Exception as e:
                print(f"Error processing line: {line}")  # Error processing line
                print(f"Exception: {e}")  # Exception
                pass
        else:
            if current_date_time and current_sender:
                messages[-1][2] += ' ' + line.strip()  # Concatenate messages for a sender in the same line / Concatenar mensajes de un remitente en la misma línea
            else:
                print(f"Line does not match the pattern: {line}")  # Line does not match the pattern

    return pd.DataFrame(messages, columns=['DateTime', 'Sender', 'Message'])

# Clean and structure the data / Limpiar y estructurar los datos
chat_df = preprocess_chat(chat_data)

if chat_df.empty:
    print("No messages found in the file.")  # No messages found in the file
else:
    # Step 3: Analysis of message count by member / Paso 3: Análisis del conteo de mensajes por miembro
    message_counts = chat_df['Sender'].value_counts()

    # Plot of message count by member / Plot del conteo de mensajes por miembro
    plt.figure(figsize=(10, 6))
    message_counts.plot(kind='bar', color='skyblue')
    plt.title('Message Count by Member / Conteo de mensajes por miembro')
    plt.xlabel('Member / Miembro')
    plt.ylabel('Number of messages / Cantidad de mensajes')
    plt.xticks(rotation=45)
    plt.show()

    # Step 5: Analysis of most common words / Paso 5: Análisis de las palabras más comunes
    def get_most_common_words(messages, num_words=30):
        words = ' '.join(messages).lower().split()
        common_words = Counter(words).most_common(num_words)
        return common_words

    most_common_words = get_most_common_words(chat_df['Message'])

    # Plot of most common words / Plot de las palabras más comunes
    words, counts = zip(*most_common_words)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title('Most common words / Palabras más comunes')
    plt.xlabel('Words / Palabras')
    plt.ylabel('Frequency / Frecuencia')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Step 6: Sentiment analysis / Paso 6: Análisis de sentimiento
    sentiment_analyzer = SentimentIntensityAnalyzer()
    chat_df['Sentiment'] = chat_df['Message'].apply(lambda x: sentiment_analyzer.polarity_scores(x)['compound'])

    # Plot of sentiment analysis / Plot del análisis de sentimiento
    plt.figure(figsize=(10, 6))
    chat_df['Sentiment'].hist(bins=20, color='skyblue')
    plt.title('Distribution of message sentiment / Distribución del sentimiento de los mensajes')
    plt.xlabel('Sentiment / Sentimiento')
    plt.ylabel('Frequency / Frecuencia')
    plt.tight_layout()
    plt.show()
