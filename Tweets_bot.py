import sys
import time
import csv
import tweepy
from tweepy.auth import OAuthHandler

#====================Métodos====================
def main():
    acesso_api =__acesso_api()

    #busca por palavras chaves
    query = 'COVID OR CORONAVIRUS -filter:retweets'
    max_tts = 10

    #define nome do csv e chama método da lib csv
    csvFile = open("Resultados_tt.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["DATA",
                        "AUTOR",
                        "LOCALIZACAO",
                        "PLATAFORMA",
                        "TWEET"])

    lista_tts = __procura_tts(query,acesso_api,max_tts)
    for tt in lista_tts:
        print ("DATA: ", tt.created_at)
        print("AUTOR: ", tt.author.screen_name)
        print("LOCALIZACAO: ", tt.author.location)
        print("PLATAFORMA: ", tt.source)
        print("TWEET: ", tt.full_text)

        #Atribui os campos para um arq .csv
        csvWriter.writerow([tt.created_at,
                            tt.author.screen_name,
                            tt.author.location,
                            tt.source,
                            tt.full_text.encode('utf-8')])
    csvFile.close()


#para criar método privado, começa com 2x '_'
def __acesso_api():
    CONSUMER_KEY = ''  # API KEY TWITTER DEV
    CONSUMER_SECRET = ''  # API SECRET KEY TWITTER DEV
    ACCESS_KEY = ''  # ACCESS TOKEN
    ACCESS_SECRET = ''  # ACCESS TOKEN SECRET

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)  # Recebe a autorização para acessar o Twitter Dev
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)  # Loga na sessão do Twitter Dev

    return tweepy.API(auth, wait_on_rate_limit=True)  # Loga na sessão da api

def __procura_tts(query, acesso_api, max_tts):
    try:
        print("Procurando pelos tweets...")
        #return acesso_api.search(q=query, count=max_tts, result_type="recent", locale="br")
        return tweepy.Cursor(acesso_api.search, q=query, tweet_mode='extended', exclude_replies=True, count=max_tts, lang="pt", since="2020-04-03").items()

    except:
        err = sys.exc_info()[0]
        print(err)
        print("Não foi possível localizar nenhum tweet.")


#====================Processamento====================
while True:
    main()
    time.sleep(5)

