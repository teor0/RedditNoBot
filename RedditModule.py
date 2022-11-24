 """RedditModule

Questo modulo contiene le seguenti funzioni:
    * get_number_post_comment - ritorna il numero di commenti all'interno di un post
    * delete_specific_post - effettua la remove come mod di un post specifico

License:
    MIT License

    Copyright (c) 2022 Matteo Orlando

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

Author: 
    Matteo Orlando
    """
import datetime


def get_number_post_comment(reddit_instance, submission_id):
    """Funzione per ottenere il numero di commenti in un post

    Parameters
    ---------
    reddit_istance : Reddit Instance
        instanza utilizzata per interagire con l'API
    submission_id : str
        ID del post

    Returns
    -------
    int
        ritorna il numero dei commenti del post
    """
    submission = reddit_instance.submission(submission_id)
    return len(submission.comments.list())


def delete_specific_post(reddit_instance, sub, flair, hours_threshold, min_comment):
    """Funzione per rimuovere come moderatore un post sotto le seguenti condizioni:
        - flair del post è quello passato alla funzione
        - ore passate rispetto alla pubblicazione sono maggiore di un limite
        - numero di commenti inferiore ad un minimo
        N.B. i post candidati alla rimozione sono tra i primi 10 nuovi post

    Parameters
    ---------
    reddit_istance : Reddit Instance
        instanza utilizzata per interagire con l'API
    sub : str
        nome del subreddit su cui cercare i post
    flair : str
        flair utilizzato per individuare specifici post
    hours_threshold : float
        ore dopo la quale il post è candidato alla rimozione
    min_comment : int
        numero minimo di commenti che non fanno scattare la rimozione

    """
    subreddit = reddit_instance.subreddit(sub)
    for submission in subreddit.new(limit=10):
        now = datetime.datetime.now()
        dt = datetime.datetime.fromtimestamp(submission.created_utc)
        hours_passed = (now-dt).total_seconds()/3600
        if submission.link_flair_template_id == flair and hours_passed > hours_threshold \
                and get_number_post_comment(reddit_instance,submission.id) < min_comment:
            submission.mod.remove()
