# -*- coding: utf-8 -*-
import requests
import os
import random
import sys
import time
from bs4 import BeautifulSoup

class Gather():
    baseDir = ""

    history = set()
    conf = dict()

    def __init__( self, path, host ) :
        self.baseDir = path

        if not os.path.isdir( path ) :
            return Exception()

        if not os.path.exists( os.path.join( path, "html") ) :
            os.makedirs( os.path.join( path, "html" ), True )

        if not os.path.exists( os.path.join( path, "gather") ) :
            os.makedirs( os.path.join( path, "gather" ), True )

        self.targetHost = host
        self.loadRK()

    def loadRK( self ):
        if os.path.exists( os.path.join( self.baseDir, "rkdic.txt" ) ) :
            f = open( os.path.join( self.baseDir, "rkdic.txt" ), "r" )
            for i in f :
                history.add( i )

    def saveRK( self ):
        with open( os.path.join( self.baseDir, "rkdic.txt" ), "w" ) as f :
            f.write( "\n".join( self.rkDic ) )

    def noblocking( self ):
        time.sleep( random.randrange(10,30)*0.1 )

    def gatheringByKeyword( self, keyword, debug=False ) :
        if keyword in self.history :
            return [], [], []

        data = []

        bs = self.getHTML( keyword )

        titles = self.getTitleFromHTML( bs )
        contents = self.getContentFromHTML( bs )

        for x,y in zip( titles, contents ) :
            data.append( keyword + "\t" + x + "\t" + y )

        self.history.add( keyword )

        related_keywords = self.getRelatedKeywordFromHTML( bs )
        for rk in related_keywords :
            if rk in self.history :
                continue;

            rk_sub = self.getHTML( rk )

            rk_titles = self.getTitleFromHTML( rk_sub )
            rk_contents = self.getContentFromHTML( rk_sub )

            for x,y in zip( rk_titles, rk_contents ) :
                data.append( rk + "\t" + x + "\t" + y )

            self.history.add( rk )

        return related_keywords, data

    def getHTML( self, keyword ) :
        content = ""
        targetFile = os.path.join( self.baseDir, "html", keyword+".txt" )

        if not os.path.exists( targetFile ) :
            self.noblocking()
            url = "https://m.search.naver.com/search.naver?where=m_blog&query="+keyword
            params = { 'User-agent':'Mozilla/5.0','Accept':'text/html'}
            response = requests.get( url, params=params )

            content = response.text
            ofs = open( targetFile, "w" , encoding='utf-8' )
            ofs.write( content )
            ofs.close()
        else :
            ifs = open( targetFile, "r", encoding='utf-8' )
            content = ifs.read()
            ifs.close()

        bs = BeautifulSoup( content, 'html5lib' );

        return bs

    def getRelatedKeywordFromHTML( self, bs ) :
        related_keywords = []

        try :
            related_keyword_list = bs.findAll( 'div', {'class','keyword _rk_hcheck'} )[0].findAll('a')
        except:
            return related_keywords

        for rk in related_keyword_list :
            related_keywords.append( rk.text )

        return related_keywords

    def getTitleFromHTML( self, bs ) :
        titles = []

        try :
            title_list = bs.findAll( 'div', {'class','api_txt_lines total_tit'} )
        except :
            titles

        for tl in title_list :
            titles.append( tl.text )

        return titles

    def getContentFromHTML( self, bs ) :
        contents = []

        try :
            content_list = bs.findAll( 'div', { 'class', 'total_dsc' } )
        except :
            return contents
        for cn in content_list :
            contents.append( cn.text )

        return contents

def gather_wiki() :
    content = ""

    url = "https://en.wikipedia.org/wiki/Category:High_fashion_brands"
    params = { 'User-agent':'Mozilla/5.0','Accept':'text/html'}
    response = requests.get( url, params=params )

    content = response.text

    bs = BeautifulSoup( content, 'html5lib' );

    groups = bs.findAll( 'div', { 'class': 'mw-category-group' } )

    print ( "find %d group " % len( groups ) )

    NER = []

    for group in groups :
        targetItem = group.findAll( 'a' )
        print ( "find %d item " % len( targetItem ) )
        for item in targetItem :
            NER.append( item.text )

    return NER

def gather_wiki2() :
    content = ""

    url = "https://en.wikipedia.org/w/index.php?title=Category:High_fashion_brands&pagefrom=Loro+Piana#mw-pages"
    params = { 'User-agent':'Mozilla/5.0','Accept':'text/html'}
    response = requests.get( url, params=params )

    content = response.text

    bs = BeautifulSoup( content, 'html5lib' );

    groups = bs.findAll( 'div', { 'class': 'mw-category-group' } )

    print ( "find %d group " % len( groups ) )

    NER = []

    for group in groups :
        targetItem = group.findAll( 'a' )
        print ( "find %d item " % len( targetItem ) )
        for item in targetItem :
            NER.append( item.text )

    return NER

def gather_theicionic() :
    content = ""
    base_url = "http://www.theiconic.com.au"

    time.sleep( random.randrange(10,30)*0.1 )

    url = "/fashion-glossary/"
    params = { 'User-agent':'Mozilla/5.0','Accept':'text/html'}
    response = requests.get( base_url+url, params=params )

    content = response.text

    bs = BeautifulSoup( content, 'html5lib' );

    groups = bs.findAll( 'div', { 'class','alphabet-section'} )

    print ( "find %d group " % len( groups ) )

    NER = []

    for group in groups :
        targetItem = group.findAll( 'a' )
        print ( "find %d item " % len( targetItem ) )

        for item in targetItem :
            url = item.get('href')

            print ( url )
            time.sleep( random.randrange(10,30)*0.1 )
            params = { 'User-agent':'Mozilla/5.0','Accept':'text/html'}

            response = ""
            if url.find( 'http://' ) >= 0 :
                response = requests.get( url, params=params )
            else :
                response = requests.get( base_url+url, params=params )

            content = response.text

            bs = BeautifulSoup( content, 'html5lib' );

            figcation = bs.findAll( 'figcaption' )

            for fig in figcation :
                if fig.find( 'span', { 'class':'brand'} ) == None :
                    continue
                NER.append( ( fig.find( 'span', { 'class':'brand'} ).text \
                    , fig.find( 'span', { 'class':'name'} ).text ) )
    return NER


def saveToFile( fileName, items ) :
    fout = open( os.path.join( os.getcwd(), "gatheringFashion", ( "%s.txt"%fileName )), "w" )
    fout.write( "\n".join( items ))
    fout.close()

#saveToFile( "en.wikipedia.org1", gather_wiki() )
#saveToFile( "en.wikipedia.org2", gather_wiki2() )
saveToFile( "www.theiconinc.com.au", gather_theicionic() )
