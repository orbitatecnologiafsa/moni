import pyttsx3
import speech_recognition as sr
from PyPDF2 import PdfReader
from transformers import pipeline

# Inicializar síntese de voz
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Inicializar reconhecimento de fala
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Diga algo...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Voce disse: {text}")
            return text
        except sr.UnknownValueError:
            return "Desculpe, não entendi o que você disse."
        except sr.RequestError:
            return "Erro ao se conectar ao serviço de reconhecimento de fala."

# Ler documento PDF
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)): 
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

# Inicializar modelo de NLP
qa_pipeline = pipeline("question-answering")

def answer_question(context, question):
    result = qa_pipeline(question=question, context=context)
    return result['answer']

# Palavra-chave para ativar o assistente
keyword = "moni"

# Exemplo de uso
pdf_text = read_pdf('c:/Users/orbita/Desktop/teste/FRASE1.pdf')

speak("Sistema carregado. Diga 'moni' para começar.")
while True:
    print("Aguardando palavra-chave...")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='pt-BR')
            if keyword in text.lower():
                speak("Estou ouvindo. Qual é a sua pergunta?")
                question = listen()
                if question.lower() in ["sair", "parar", "exit"]:
                    speak("Encerrando o assistente.")
                    break
                answer = answer_question(pdf_text, question)
                speak(answer)
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            speak("Erro ao se conectar ao serviço de reconhecimento de fala.")