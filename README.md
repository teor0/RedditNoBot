# About RedditNoBot
Bot per il subreddit r/SabakuNoMaiku. Il codice comprende una serie di metodi utili per cancellare post da Reddit, estrapolare informazioni utili da una live Twitch, calcolare la durata di una playlist intera ed altro ancora. Il codice comprende l'utilizzo di: [API Youtube](https://developers.google.com/youtube/v3) e [PRAW](https://praw.readthedocs.io/en/stable/index.html).

EN:
A reddit bot for r/SabakuNoMaiku. The code contains a series of utility method to delete post from Reddit, scraping information from a live on Twitch, calculating the duration of a playlist and other things. The code make use of [Youtube API](https://developers.google.com/youtube/v3) and [PRAW](https://praw.readthedocs.io/en/stable/index.html).


---

# Requirements
- Python version 3.10+
- make
- Python3-venv
---

## Installation and running
Per installare il bot, occorre scaricare o clonare la repository e utilizzare [Makefile](https://github.com/kiurem66/RedditNoBot/blob/main/Makefile). Per avviare la procedura di installazione, eseguire `sudo make install` oppure essendo root, `make install`.
La cartella di installazione del bot è `/opt/SabakuNoBot`, si può cambiare modificando la variabile BASE all'interno del Makefile. Per eliminare il bot e tutti i suoi file si può eseguire `sudo make clean` oppure come root `make clean` o cancellando manualmente la cartella di installazione. È possibile usare `make help` per mostrare un piccolo aiuto.
**ATTENZIONE**: Il comando `make install` necessità dei permessi del superuser, altrimenti fallirà.

Il file [BotReddit.py](https://github.com/kiurem66/RedditNoBot/blob/main/BotReddit.py) viene utilizzato come script principale da cui utilizzare i metodi scritti nei moduli. L'idea è quella di ricevere un comando tramite input e di agire di conseguenza. I file [streamon.sh](https://github.com/kiurem66/RedditNoBot/blob/main/streamon.sh) e [streamoff.sh](https://github.com/kiurem66/RedditNoBot/blob/main/streamoff.sh) vengono impiegati tramite il daemon cron per monitorare lo stato online/offline dello streamer d'interesse.

Infine il file [Cypher.py](https://github.com/kiurem66/RedditNoBot/blob/main/Cypher.py), è utile per realizzare il file che memorizza le credenziali varie che il Bot impiega.

EN:

To install the bot, clone or download the repository and use the [Makefile](https://github.com/kiurem66/RedditNoBot/blob/main/Makefile). To use the makefile, run `sudo make install` or as root `make install`. The installation folder of the bot is `/opt/SabakuNoBot`, you can change it by changing, the BASE variable inside Makefile. You can delete everything via `sudo make clean` or running as root `make clean`, or deleting the installation folder manualy. For help use `make help`.
**DISCLAIMER**: You need to run `make install`  with root permission otherwise it won't work.

The [BotReddit.py](https://github.com/kiurem66/RedditNoBot/blob/main/BotReddit.py) file it's used to run the functions written in the modules. The idea is to get comands as input and execute specific scripts. The [streamon.sh](https://github.com/kiurem66/RedditNoBot/blob/main/streamon.sh) and [streamoff.sh](https://github.com/kiurem66/RedditNoBot/blob/main/streamoff.sh) files are used with cron to monitor the online/offline status of the target streamer.

The file [Cypher.py](https://github.com/kiurem66/RedditNoBot/blob/main/Cypher.py), can be used to store credentials as the Bot request.


---
