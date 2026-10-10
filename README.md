# TurboBot

Bot Discord w Pythonie ([discord.py](https://discordpy.readthedocs.io/)).

## 1. Utwórz bota na Discordzie

1. Wejdź na https://discord.com/developers/applications → **New Application**.
2. Zakładka **Bot**:
   - **Reset Token** → skopiuj token (nikomu go nie pokazuj!).
   - W sekcji **Privileged Gateway Intents** włącz **SERVER MEMBERS INTENT** i **MESSAGE CONTENT INTENT**.
3. Zakładka **OAuth2 → URL Generator**:
   - Scopes: `bot` i `applications.commands`
   - Bot Permissions: np. `Send Messages`, `Embed Links`, `Manage Messages`, `Read Message History`
   - Otwórz wygenerowany link i dodaj bota na swój serwer.

## 2. Uruchom (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env   # potem wklej token do .env
python bot.py
```

> Jeśli `Activate.ps1` jest zablokowany, uruchom raz:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Komendy

Każda działa jako `/komenda` i jako `!komenda`.

| Komenda | Opis |
|---|---|
| `ping` | opóźnienie bota |
| `hello` | powitanie |
| `roll [ścianki]` | rzut kostką |
| `userinfo [użytkownik]` | info o użytkowniku |
| `clear <ile>` | usuwa wiadomości (wymaga uprawnienia *Zarządzanie wiadomościami*) |
| `help` | lista komend (tylko `!help`) |

## Struktura

```
bot.py            # start bota, ładowanie cogów, synchronizacja komend slash
cogs/
  general.py      # podstawowe komendy
  moderation.py   # komendy moderacyjne
  events.py       # powitania + obsługa błędów
```

Żeby dodać nowe komendy, utwórz nowy plik w `cogs/` (wzoruj się na `general.py`) — zostanie załadowany automatycznie.

**Wskazówka:** wpisz ID swojego serwera w `GUILD_ID` w `.env` — nowe komendy slash będą widoczne od razu po restarcie bota.
