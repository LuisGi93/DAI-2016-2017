# -*- coding: utf-8 -*-
import tweepy, datetime, time
import os
# Consumer keys and access tokens, used for OAuth


class PopularidadNoticias ():
    consumer_key =  os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']


# OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
    ide=0
    # https://dev.twitter.com/docs/api/1.1/get/search/tweets

    def search(self,noticia):

        cont =0

        splitted = noticia.split()

        mins=splitted[0]+" " +splitted[1]+" " +splitted[3]

        for word in range(len(splitted)):
            if splitted[word][0].isupper() and word > 3:
                mins+=" " + splitted[word] + " "


        if(self.ide==0):
            for tweet in self.api.user_timeline(id='elmundoes', count=100):

                if (datetime.datetime.now() - tweet.created_at).days < 1:
                    cont=cont+1
                    if(cont==5):
                        self.ide=tweet.id
                        break

        h=0

        for page in tweepy.Cursor(self.api.search,q=mins, count=600,rpp=1000,since_id=self.ide).pages():
            for twee in page:
                    h=h+1

        print "Va la noticia"
        print noticia
        print h
        return h


    def search_city(self,ciudad):

        cont =0
        if(self.ide==0):
            for tweet in self.api.user_timeline(id='elmundoes', count=100):

                if (datetime.datetime.now() - tweet.created_at).days < 1:
                    cont=cont+1
                    if(cont==5):
                        self.ide=tweet.id
                        break

        h=0
        for page in tweepy.Cursor(self.api.search,q=ciudad, count=100,rpp=100,since_id=self.ide).pages():
            for twee in page:
                    h=h+1

        print "Va la city"
        print ciudad
        print h
        return h
