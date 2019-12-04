import tweepy
import time
print ('This is LeituraBOT')
import re
from datetime import datetime
from datetime import date
import random
import math


CONSUMER_KEY = 'c71PY7NavJS54HYF24itFlPw1'
CONSUMER_SECRET = 'pz43BasgOFO7dp9lqEvPEk3W7umAuFJJ1EmC7g1J5JhvjD2mUK'
ACCESS_KEY = '1200436542730313729-XhNyUYRgH3lEWNAbbS2BjVQdGdrGUH'
ACCESS_SECRET = 'ODH8lR5eHInW6sSK5oevlyiBk8u8i9FQX2Yzuk0quCock'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class Leitor:
  def __init__(self, usuario, meta, atual):
    self.usuario = usuario
    self.meta = meta
    self.atual = atual


d1 = datetime.strptime('2020-01-01', '%Y-%m-%d')

FILE_NAME = 'last_seen_id.txt'

def retrieve_sugestoes():
    sugestoes=[]
    with open('sugestoes.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]

            # add item to the list
            sugestoes.append(currentPlace)
    return sugestoes

def store_sugestoes(sugestoes):
    with open('sugestoes.txt', 'w') as filehandle:
        for listitem in sugestoes:
            filehandle.write('%s\n' % listitem)
    return

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

lista = [['@nicolaom102', 0, 1000],['nicolaom102', 7320, 38],['jgk019', 7320, 0],['heterdeu', 7320, 0],['Ancapistola', 7320, 0],['gordola_', 7320, 0],['Etoempire', 120, 20],['OficialMLima', 6000, 0],['Tezokin', 4015, 0],['ReZNeW_', 10000, 0],['phcarvalho27', 7320, 0],['buendadeos', 7320, 0],['YutrobogWasaLie', 7150, 0],['0P1N3', 7320, 0],['alexokivillela', 9, 8],['GuaranaLeao', 500, 34],['Carlos_VIIseth', 7320, 0],['brenoaraujooo', 7320, 0],['Eduardo30620042', 587, 226],['elvinhoaraujo', 7320, 0],['Fernandobr7506', 7320, 0],['aPUTAqTEPARIUs2', 8000, 0],['UNSionista', 100, 0],['Bieelkkkk2', 7320, 0],['Espadaence', 7320, 0],['kantmorreu', 7320, 0],['PauloDroopy', 7320, 0],['ShitImposto', 7320, 0],['josehemkemaier', 5000, 0]]

leitores = [Leitor("@nicolaom102",0,1000)]

sugestoes = []

u=0

for q in lista:
    t = lista[u]
    a = Leitor(t[0],t[1],t[2])
    leitores.append(a)
    u=u+1

def store_leitores(lista_de_leitores):
    with open('leitores.txt', 'w') as filehandle:
        for listitem in lista_de_leitores:
            newL = [listitem.usuario,listitem.meta,listitem.atual]
            filehandle.write('%s\n' % newL)
    return


def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        i=0
        for x in leitores:
            if x.usuario == str(mention.user.screen_name):
                print ("leitor encontrado")
                idusuario = i
                break
            i=i+1
        else:
            print ("leitor novo")
            leitores.append(Leitor(str(mention.user.screen_name),7320,0))
            idusuario = len(leitores) - 1

        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if 'registrar sugestão' in mention.full_text.lower() or 'registrar sugestao' in mention.full_text.lower():
            sugestoes = retrieve_sugestoes()
            sugestaoLeitura = 'https://twitter.com/' + str(mention.user.screen_name) + '/status/' + str(mention.id)
            sugestoes.append(sugestaoLeitura)
            store_sugestoes(sugestoes)
            api.update_status('@' + str(mention.user.screen_name) +
                    ' Sua sugestão foi registrada. Obrigado pela dica! ' + sugestaoLeitura, mention.id)
            print ('sugestão registrada')
        elif 'quero uma sugestão' in mention.full_text.lower() or 'quero uma sugestao' in mention.full_text.lower():
            sugestoes = retrieve_sugestoes()
            tamanho = len(sugestoes)
            aleatorio = math.floor(random.random() * tamanho)
            api.update_status('@' + str(mention.user.screen_name) +
                    ' Segue uma sugestão para leitura! ' + sugestoes[aleatorio], mention.id)
            print ('sugestão enviada')
        elif 'definir meta' in mention.full_text.lower() or 'estabelecer meta' in mention.full_text.lower():
            nm = re.findall('\d+', mention.full_text)
            if nm == []:
                return
            else:
                novameta = int(nm[0])
            leitores[idusuario].meta = novameta
            print('nova meta definida ' + str(mention.user.screen_name) + ' - meta do ano foi atualizada para ' + str(leitores[idusuario].meta) , flush=True)
            api.update_status('@' + str(mention.user.screen_name) +
                    ' a sua meta do ano foi atualizada para ' + str(leitores[idusuario].meta), mention.id)
        elif 'paginas' in mention.full_text.lower() or 'páginas' in mention.full_text.lower():
            numPaginasLidas = re.findall('\d+', mention.full_text)
            if numPaginasLidas == []:
                return
            else:
                PaginasLidas = int(numPaginasLidas[0]) + int(leitores[idusuario].atual)
            print (PaginasLidas)
            leitores[idusuario].atual = PaginasLidas
            leiturasPorDia = leitores[idusuario].meta / 366
            porcentagem = round(int(PaginasLidas) / int(leitores[idusuario].meta),4)*100
            hoje = datetime.strptime(str(date.today()), '%Y-%m-%d')
            diasPassados = abs((hoje - d1).days)
            if date.today().strftime("%Y")==2019:
                diasPassados=0
            leituraEmDia = round(diasPassados * leiturasPorDia)
            if leituraEmDia < PaginasLidas:
                situacao = "adiantado(a)! Se continuar assim você vai superar sua meta!"
            if leituraEmDia > PaginasLidas:
                situacao = "atrasado(a)... vamos correr atras do prejuizo!"
            if leituraEmDia == PaginasLidas:
                situacao = "em dia! Continue assim!"
            later = ""
            #later = ". Ate agora era para você ter lido "+ str(leituraEmDia) +  " paginas. Você esta " + str(situacao)
            print('leitura registrada ' + str(mention.user.screen_name) + ' - leitura total: ' + str(leitores[idusuario].atual) , flush=True)
            api.update_status('@' + str(mention.user.screen_name) +
                    ' Você ja leu ' + str(leitores[idusuario].atual) + ' paginas! Você completou ' + str(round(porcentagem,2)) + "% da sua meta do ano (" + str(leitores[idusuario].meta) +
                    ")" + later, mention.id)
        elif 'cancelar' in mention.full_text.lower():
            numPaginasLidas = re.findall('\d+', mention.full_text)
            PaginasLidas = int(leitores[idusuario].atual) - int(numPaginasLidas[0])
            leitores[idusuario].atual = PaginasLidas
            leiturasPorDia = leitores[idusuario].meta / 366
            porcentagem = round(int(PaginasLidas) / int(leitores[idusuario].meta),4)*100
            hoje = datetime.strptime(str(date.today()), '%Y-%m-%d')
            diasPassados = abs((hoje - d1).days)
            if date.today().strftime("%Y")==2019:
                diasPassados=0
            leituraEmDia = round(diasPassados * leiturasPorDia)
            if leituraEmDia < PaginasLidas:
                situacao = "adiantado(a)! Se continuar assim você vai superar sua meta!"
            if leituraEmDia > PaginasLidas:
                situacao = "atrasado(a)... vamos correr atras do prejuizo!"
            if leituraEmDia == PaginasLidas:
                situacao = "em dia! Continue assim!"
            later = ""
            #later = ". Ate agora era para você ter lido "+ str(leituraEmDia) +  " paginas. Você esta " + str(situacao)
            print('leitura cancelada ' + str(mention.user.screen_name) + ' - leitura total: ' + str(leitores[idusuario].atual) , flush=True)
            api.update_status('@' + str(mention.user.screen_name) +
                    ' Você cancelou ' + str(numPaginasLidas[0]) + " paginas. O saldo agora é de " + str(leitores[idusuario].atual) + ' paginas! Você completou ' + str(round(porcentagem,2)) + "% da sua meta do ano (" + str(leitores[idusuario].meta) +
                    ")" + later, mention.id)
        store_leitores(leitores)

while True:
    reply_to_tweets()
    time.sleep(15)
