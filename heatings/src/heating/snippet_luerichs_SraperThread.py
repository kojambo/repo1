# -*- coding: iso-8859-15 -*-
'''
Created on 20.10.2011

@author: luerich
'''

import threading
from BeautifulSoup import BeautifulSoup
import time
import random

class ScraperThread(threading.Thread):
    '''
    This is the thread to get the data
    '''
    def _time_to_wait(self):
        return random.uniform(.5, 1.5)

    # setting user agent
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:10.0)"
    HEADERS = { 'User-Agent': USER_AGENT}

    _HOST = "http://www.wasserwaermeluft.de"
    _PATH = "/nc/wissenswert/handwerkersuche/betrieb//-1//wwldb_searchresult/"
    URL = _HOST + _PATH
    PROXY = False
    PROXY_URL = 'http://153.96.220.2:81'
    
    # crit[23] = Heizungsmodernisierung
    # crit[59] = Heizungs-Check
    # crit[67] = Fachbetrieb für Optimierung von Heizungsanlagen
    # crit[24] = Heizungswartung
    # crit[28] = Wärmelieferung
    # crit[29] = Contracting
    # crit[32] = Fachkraft Solarthermie
    # crit[35] = Solarthermie 
    # crit[36] = Erdwärme/Wärmepumpen
    # crit[75] = Pellets/Biomasse
    # crit[38] = Photovoltaik
    # crit[45] = Gebäudeenergieberater des Handwerks
    # crit[46] = Energieberatung und Energiepass
    CRITERIA = ["crit[23]", "crit[59]", "crit[67]", "crit[24]", \
                "crit[28]", "crit[29]", "crit[32]", "crit[35]", \
                "crit[36]", "crit[75]", "crit[38]", "crit[45]", \
                "crit[46]"]
    
#    Fachkraft Solarthermie + Solarthermie
#    Fachkraft Solarthermie + Erdwärme
#    Solarthermie + Erdwärme
#    Fachkraft Solarthermie + Pellets/Biomasse
#    Solarthermie + Pellets/Biomasse
#    Erdwärme + Pellets/Biomasse
#    Photovoltaik + Solarthermie
#    Photovoltaik + Heizungsmodernisierung
#    Solarthermie + Biomasse + Erdwärme
    COMBINED_CRITERIA = [["crit[32]", "crit[35]"], \
                         ["crit[32]", "crit[36)"], \
                         ["crit[35]", "crit[36]"], \
                         ["crit[32]", "crit[75]"], \
                         ["crit[35]", "crit[75]"], \
                         ["crit[36]", "crit[75]"], \
                         ["crit[38]", "crit[35]"], \
                         ["crit[38]", "crit[23]"], \
                         ["crit[35]", "crit[75]", "crit[36]"]]
    
    # this concerns the criteria that will be loaded
    GET_SINGLE_RESULTS = True
    GET_COMBINED_RESULTS = True

    def __init__(self, plz, pool, distance):
        threading.Thread.__init__(self)
        self._pool = pool
        self._result = [plz]
        self._distance = distance
    
    def run(self):
        time1 = time.clock()
        
        criteria = []
        if self.GET_SINGLE_RESULTS:
            criteria.extend(self.CRITERIA)
        if self.GET_COMBINED_RESULTS:
            criteria.extend(self.COMBINED_CRITERIA)    
            
        for crit in criteria:
            multi = False if crit in self.CRITERIA else True
            soup = self.get_soup(crit, multi, self._distance)
            if soup != None:
                hits = len(soup.findAll('div', attrs={'class' : 'hws_eckring_small'}))
                self._result.append(hits)
#                print self.name + " found: " + str(hits) + " for " + str(crit)
                time.sleep(self._time_to_wait())
            else: 
                print self.name + " error while requesting " + str(crit)
                break
                
        print self.name + " done in " + str(round(time.clock() - time1, 2)) + " seconds (" + time.asctime() + ")"
        
    
    def get_soup(self, crit, multi, distance):
        plz = self._result[0]
        values = {'wwldb_searchform_submit' : '1' , 
                  'wwldb_searchform_plz' : plz,
                  'wwldb_searchform_umkreis' : distance}
        
        if multi:
            for c in crit:
                values[c] = '1'
        else:
            values[crit] = '1'
        
        try:
            if self.PROXY:
                response = self._pool.request_encode_body('POST', self.URL, fields=values, encode_multipart=False)
            else:
                response = self._pool.request_encode_body('POST', self._PATH, fields=values, encode_multipart=False)
        except:
            return None
        
        # get the page and parse it
        if response.status == 200:
            return BeautifulSoup(response.data)
        else:
            return None
    
    @property
    def name(self):
        return self._result[0]
    
    @property
    def result(self):
        return self._result 
