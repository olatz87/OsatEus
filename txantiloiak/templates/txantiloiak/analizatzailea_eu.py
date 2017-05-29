#AINHOARENA!!!

#!/usr/bin/python3
# -*- coding: utf-8 -*-

##Exekutatu aurretik Java-ren bertsioa aldatu behar da:
#setenv JAVA_HOME /usr/java/java18/
#setenv PATH $JAVA_HOME/bin:$PATH


import nltk,os,codecs,json,jsonrpclib,copy,sys
# from nltk.tag.stanford import NERTagger
# from nltk.tag.stanford import POSTagger
# from nltk.tag.stanford import StanfordTagger
#from nltk.tokenize.stanford import StanfordTokenizer
from pprint import pprint
from wrapper.wrapper_eustagger import Wrapper

#Zerbitzariak erabiltzeko  (ts_en.py zerbitzaria)
class TermZerbitzaria:
    def __init__(self, port_number = 9608):
        self.server = jsonrpclib.Server("http://158.227.106.115:%d" % port_number)

    def deskribapenakJaso(self):
        return json.loads(self.server.deskribapenakJaso(),encoding="utf-8")

    def deskribapenArabera(self):
        return json.loads(self.server.deskribapenArabera(),encoding="utf-8")

    def sct2term(self,sctId):
        return json.loads(self.server.sct2term(sctId),encoding="utf-8")

    def sct2desc(self,sctId):
        return json.loads(self.server.sct2desc(sctId),encoding="utf-8")

    def sct2hierarkiak(self,sctId):
        return json.loads(self.server.sct2hierarkiak(sctId),encoding="utf-8")

    def desc2sct(self,desc,lemma):
        return json.loads(self.server.desc2sct(desc,lemma))

    def kontzeptuakJaso(self):
        return json.loads(self.server.kontzeptuakJaso(),encoding="utf-8")

    def lema2sct(self,desc,lemma):
        return json.loads(self.server.lema2sct(desc,lemma))

'''
class EustaggerLite:
    def __init__(self, port_number=9606):
        self.server = jsonrpclib.Server("http://158.227.106.115:%d" % port_number)

    def parse(self, text):
        return self.server.parse(text)
'''

#izen bereziak identifikatzeko. EPONIMOAK = Down, Hopkins,... 
def eponimoakIdentifikatu(tagged):
    """
    Analizatutako testua pasata (tagged), bertan agertzen diren medikuen izen bereziak identifikatzen ditu, 
    NamedEntity-ri "EPONYM" etiketa esleituz
    """
    aurrekaria = False
    aurkituta = True
    epoFitx = '/ixadata/users/operezdevina001/Doktoretza/SintaxiMaila/Eponimoak/eponimoak.txt'
    lag = []
    lagForma = ''
    eponimoak = set()
    eponimo = []
    strOut = []
    parenthesis = ['-RSB-','-LSB-','-RRB-','-LRB-','AND/OR']
    with codecs.open(epoFitx,encoding="utf-8") as fitx:
        for line in fitx:
            line = line.strip()
            eponimoak.add(line.lower())
            eponimo.insert(len(eponimo), line)
    for token in tagged:
        forma,info = token
        if ',' in forma or '/' in forma or forma == "":
            strOut.append([forma,info])
            continue
            ##################################### Eponimoak euskaraz identifikatzeko
        elif forma[0].isupper():
            lagLemmaEponimo = ""
            for i in range(len(eponimo)):
            #park eta parkinson bezalako bereizketak egiteko(formarekin konparatu). len() erabiliko da eponimo luzeena .txt fitxategitik lortzeko.
                if len(lagLemmaEponimo) < len(eponimo[i].lower()) and eponimo[i].lower() in forma.lower() and forma.lower()[0: len(eponimo[i])] == eponimo[i].lower():	     
                    info["Lemma"] = eponimo[i].lower()
                    info["NamedEntityTag"]='EPONYM'
                    lagLemmaEponimo = info["Lemma"]
                    aurkituta = True
        if not forma.isupper() and forma.lower() in ['van','von','de','den','der','del','la','le','di','da','du']:
            aurrekaria = True
            lag.append(token)
            lagForma += forma+'_'
            #print("a", lagForma)
            #continue
        elif aurrekaria:
            fBerria = lagForma+forma
            #print("fb", fBerria)
            if forma not in parenthesis and forma[0].isupper():
                forma = fBerria
                info["CharacterOffsetBegin"]=lag[0][1]["CharacterOffsetBegin"]
                info["Lemma"] = fBerria
                #info["POfS"]='NNP'
                info["NamedEntityTag"]='EPONYM'
            else:
                for el in lag:
                    strOut.append(el)
            aurrekaria = False
            lag = []
            lagForma = ''
        elif forma[0].isupper() and forma.lower() in eponimoak:
            info["NamedEntityTag"] = "EPONYM"
        elif forma.isupper() and forma not in parenthesis and len(forma) > 1:
            info["NamedEntityTag"] = "ABBRE"
        elif forma not in parenthesis and '-' in forma and not aurkituta:
            asko = forma.split('-')
            for elem in asko: 
                if elem.lower() in eponimoak:
                    info["NamedEntityTag"] = "EPONYM"
                elif elem and elem[0].islower() or len(elem) <= 2 or elem.isdigit():
                    info["NamedEntityTag"] = "O"
                    break
        if info["NamedEntityTag"] in ["EPONYM","ABBRE"]:
            if info["NamedEntityTag"] == "EPONYM":
                lagMaius = forma.split('-')
                maius = False
                for lm in lagMaius:
                    #print(line,lm)
                    if lm[-1].isupper():
                        maius = True
                if maius:
                    info["Lemma"] = forma
        if not aurrekaria:
            strOut.append([forma,info])
    if aurrekaria:
       for el in lag:
           strOut.append(el)
    return strOut

def errekOsatu(i,hInd,formak,hvalue,fAgertuak,multzoak,abstrakzioak,si):
    if i < len(formak):
        mulLagR = copy.deepcopy(multzoak[si])
        absLagR = copy.deepcopy(abstrakzioak[si])
        multzoak[si].append(formak[i])
        abstrakzioak[si].append(formak[i])
        sib = errekOsatu(i+1,hInd,formak,hvalue,fAgertuak,multzoak,abstrakzioak,si)
        #pprint(multzoak)
        # print('i',i,'sib',sib)
        for ml in hInd:
            if ml[0] == i:
	        # print("BINGO",ml)
	        # print(multzoak)
                mulLag = copy.deepcopy(mulLagR)
                absLag = copy.deepcopy(absLagR)
                ind = hInd.index(ml)
	        # print('ind',ind)
	        # print(sib)
                multzoak.append(mulLag)
                abstrakzioak.append(absLag)
	        # print(multzoak)
	        # print(abstrakzioak)
                multzoak[sib].append(fAgertuak[ind].replace(" ","_"))
                abstrakzioak[sib].append(hvalue[ind])
 	        # print(multzoak)
	        # print(abstrakzioak)
                sib = errekOsatu(ml[1],hInd,formak,hvalue,fAgertuak,multzoak,abstrakzioak,sib)
        return sib
    else:
        # print(si+1)
        return si+1


def snomedIdentifikatu(tagged,des,luzeenaBool,mulBool,absBool):
    formak = []
    fArray = []
    lArray = []   
    tArray = tagged[:]
    hInd = []
    l = []
    hMultzokatzeko = {}
    hvalue = []
    cvalue = []
    fAgertuak = []
    eInd = []
    k = 0
    for token in tagged:
        forma,info = token
        formak.append(forma)
        llag = len(fArray)
        k += 1
        fArray.append(forma)
        lArray.append(info["Lemma"])
        #print("lA", lArray)
        for i in range(0,llag):
            #if k == len(tagged) and i == 0:
            #    continue
            l = lArray[i] + " " + info["Lemma"]
            f  = fArray[i] + " " + forma
            lArray[i] = l
            fArray[i] = f
            kodT = des.desc2sct('', l.lower())
            #kodT = des.desc2sct(f.lower(),'')
            hieT = des.sct2hierarkiak(kodT)
            print('KodT',kodT,'hieT',hieT,'f',f, 'l', l)
            if hieT:
                #print(f,hieT)
                hInd.append((i,k))
                hMultzokatzeko[(i,k)] = hieT
                hvalue.append(hieT)
                cvalue.append(kodT)
                fAgertuak.append(f)

        kod1 = des.desc2sct(forma.lower(),info["Lemma"])
        #print("   ", kod1)
        ############################
        #if not kod1:
        #    kod1 = des.i(forma.lower(),info["Lemma"])
        ###########################

        hieT1 = des.sct2hierarkiak(kod1)
        if hieT1:
            #print(forma,hieT1)
            hvalue.append(hieT1)
            cvalue.append(kod1)
            hInd.append((k-1,k))
            hMultzokatzeko[(k-1,k)] = hieT1
            fAgertuak.append(forma)
        if info["NamedEntityTag"] in ["PERSON","EPONYM"]:
            hInd.append((k-1,k))
            cvalue.append([""])
            fAgertuak.append(forma)
            if (k-1,k) in hMultzokatzeko:
                lagm = hMultzokatzeko[(k-1,k)]
                lagm.append("EPONYM")
                hMultzokatzeko[(k-1,k)]=lagm
                hvalue.append(lagm)
            else:
                hMultzokatzeko[(k-1,k)]=["EPONYM"]
                hvalue.append(["EPONYM"])
    #ZATI HAU, TERMINO LUZEENA BAKARRIK HARTZKEO ERABILTZEN DA
    if luzeenaBool:
        hOrdenatuak = sorted(hInd,key = lambda x: (x[0],-x[1]))
        hILag = []
        for hI in hOrdenatuak:
            aurkitua = False
            j = 0
            while not aurkitua and j < len(hILag):
                if hI[0] >= hILag[j][0] and hI[1] <= hILag[j][1]:
                    aurkitua = True
                j += 1
            if aurkitua:
                ind = hInd.index(hI)
                hInd.pop(ind)
                #print(fAgertuak)
                fAgertuak.pop(ind)
                hvalue.pop(ind)
                cvalue.pop(ind)
            else:
                hILag.append(hI)
    l = 0
    for inP in hInd:
        i = inP[0]
        j = inP[1]
        for k in range(i,j):
            lag = tArray[k]
            forma,info = lag
            etik = '#'.join(hvalue[l])+'-'+str(l)
            buk = ''
            if k == i and k != j-1:
                buk = '_HAS'
            elif k == j-1 and k != i:
                buk = '_BUK'
            elif i != j-1:
                buk = '_ERD'
            if "Hierarchy" in info :
                info["Hierarchy"] += '&' + etik + buk
            else:
                info["Hierarchy"] = etik + buk
            if "sctId" in info:
                info["sctId"] += '&' + '#'.join(cvalue[l]) + buk
            else: 
                info["sctId"] = '#'.join(cvalue[l]) +buk
            tArray[k] = lag
        l += 1

    # print("lArray", lArray)
    # print("fArray",fArray)
    # print("tArray",tArray)
    # print("hInd",hInd)
    # print("hvalue",hvalue)
    # print("cvalue",cvalue)
    # print("fAgertuak",fAgertuak)
    # print("formak",formak)
    # print("hMultzokatzeko",hMultzokatzeko)
    multzoak = [[]]
    abstrakzioak = [[]]
    if mulBool or absBool:

        sib = errekOsatu(0,hInd,formak,hvalue,fAgertuak,multzoak,abstrakzioak,0)
    #print("BUKAERAKOAK")
    #pprint(multzoak)
    #pprint(abstrakzioak)

    return tArray,multzoak,abstrakzioak


def analizatu(term,luzeenaBool=False,multzokatu=False,abstrakzioak=False):
    """
    term: analizatzeko terminoa
    luzeenaBool: multzokatze luzeenak bakarrik hartzeko
    multzokatu: multzokatzeak jaso nahi baditugu
    abstrakzioak: abstrakzioak jaso nahi baditugu
    """
    #eu = EustaggerLite()

    wr =Wrapper()
    result = wr.parse(term)
    if type(result) != type({}):
        #print(term,result)
        if multzokatu:
            if abstrakzioak:
                return None,None,None
            return None,None
        return None
    des = TermZerbitzaria()
    anal_den = []
    #for esaldi in result[term]["sentences"]:
    #    hitzak = esaldi["words"]
    #    print(hitzak)
    eponimoekin = eponimoakIdentifikatu(result["sentences"])
    analisia,multzoak,absak = snomedIdentifikatu(eponimoekin,des,luzeenaBool,multzokatu,abstrakzioak)
    anal_den += analisia

    if multzokatu:
        mulB = []
        for m in multzoak:
            if m not in mulB:
                mulB.append(m)
        if len(result["sentences"]) > 1:
            mulB = None
            absak = None
        if abstrakzioak:
            return anal_den,mulB,absak
        else:
            return anal_den,mulB
    elif abstrakzioak:
        return anal_den,absak
    return analisia

#def tokenizatu(term):
#    return StanfordTokenizer().tokenize(term)


if __name__ == "__main__":
    term = "Down-en syndrome"
    luz = True
    if len(sys.argv) >= 2:
        term = sys.argv[1]
        if len(sys.argv) >= 3:
            luz = False
    print(term)
    #start_time = time.time()
    hie = (analizatu(term,luz,False,False))
    #print(time.time() - start_time)
    print(hie)
