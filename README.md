## Opis projektu
Projekt został zrealizowany przez:
1. Marcina Borkowskiego
2. Piotr Strycharczyk

Projekt realizuje prosty czat internetowy oparty na **Flasku** i **Socket.IO**, umożliwiający komunikację w czasie rzeczywistym między wieloma użytkownikami. Aplikacja webowa renderuje interfejs użytkownika, natomiast serwer Flask odbiera i rozsyła wiadomości przy użyciu WebSocketów.

W celu zapewnienia bezpieczeństwa danych przy jednoczesnym współdzieleniu zasobów (lista wiadomości), zastosowano mechanizm blokady wątków (`threading.Lock`).

---

## Instrukcja uruchomienia

### Wymagania

- Python 3.x
- Pakiety:
  - Flask
  - Flask-SocketIO

### Instalacja

```bash
pip install flask flask-socketio
```

## Opis problemu
Projekt opiera się na przetwarzaniu równoległym wiadomości przychodzących od użytkowników. Każda wiadomość trafia do wspólnej listy messages. Ponieważ wiele klientów może wysyłać wiadomości równocześnie, istnieje ryzyko wyścigu wątków (race condition) lub uszkodzenia danych.

Aby temu zapobiec, zastosowano sekcję krytyczną z blokadą (message_lock), która gwarantuje, że tylko jeden wątek ma dostęp do listy messages w danym momencie.

## Watki
W aplikacji działają następujące typy wątków:
Główny wątek serwera odpowiada za uruchomienie aplikacji Flask.
Wątki Socket.IO	za każdego klienta czatu (przeglądarka) komunikuje się z serwerem poprzez osobny wątek WebSocket.
Wątek zliczający funkcja /threads pozwala podejrzeć liczbę aktywnych wątków.

## Sekcje krytyczne i ich rozwiązanie
Sekcja krytyczna
Lista messages przechowuje wszystkie wiadomości czatu. Jednoczesna modyfikacja tej listy przez wiele wątków może prowadzić do nieprawidłowego działania aplikacji.

Rozwiązanie
Zastosowano blokadę wątku (threading.Lock) o nazwie message_lock.

##  Funkcjonalności
Obsługa wielu użytkowników równocześnie

Wysyłanie i odbieranie wiadomości w czasie rzeczywistym

Automatyczne rozgłaszanie wiadomości do wszystkich klientów

Obsługa nazw użytkowników

Monitorowanie liczby aktywnych wątków