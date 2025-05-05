from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit#dodatek do Flask umożliwiwa komunikacje w czasie rzeczywistym
import threading#wątki


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)


message_lock = threading.Lock()#zabezpiecznie dostepu do listy wiadomosci by kilka watkow nie pisalo do niej jednoczenie (Race condition)
messages = []

@app.route('/')#renderowanie wygladu chatu
def index():
    return render_template('chat.html')

@app.route('/threads')#pokazuje aktywna liczbe watkow wdanym momencie
def thread_count():
    return f"Aktualna liczba wątków: {threading.active_count()}"


# odpowiedzane za przychodze wiadomosci
# Funkcja obsługująca zdarzenie 'message' z SocketIO (czyli przychodzącą wiadomość od klienta)
@socketio.on('message')
def handle_message(msg):
    # Wywołanie pomocniczej funkcji, która zwraca liczbę aktywnych wątków (można to zobaczyć np. w konsoli)
    print(thread_count())

    # Blok 'with' z użyciem locka - zapewnia, że tylko jeden wątek na raz może modyfikować listę messages
    with message_lock:
        # Dodanie otrzymanej wiadomości do listy przechowywanej na serwerze
        messages.append(msg)
        # Wydrukowanie wiadomości w konsol
        print(f"Message received: {msg}")

    # Wysłanie wiadomości do wszystkich polaczych klientow
    send(msg, broadcast=True)

@socketio.on('join_chat')#odpowiedzialna za historie chatu dla nowych userow
def handle_join_chat():
    print("Nowy klient wszedł na czat.")
    with message_lock:
        for msg in messages:#wszystkie wiadomosci dla nowych userow
            emit('message', msg)  # emit działa tylko do klienta, który wywołał zdarzenie


if __name__ == '__main__':
    print("Starting chat server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
