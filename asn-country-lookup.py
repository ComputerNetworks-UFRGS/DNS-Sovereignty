import os
import time
import pandas as pd
import numpy as np
import dns.resolver #dnspython
import pyasn
import requests

asndb = pyasn.pyasn('ipasn_230616.dat')

#https://catalog.caida.org/dataset/as_organizations/access

caidaOrgInfo = ""

MILLION = 1000000
#MILLION = 10000

def getArecords(domain):
	try:
		print("Looking up A records")
		answer = dns.resolver.resolve(str(domain), rdtype=dns.rdatatype.A)
		#print(answer.response.answer)
		return answer.response.answer[0][0]
	except Exception as e:
		print(e)

def getAAAArecords(domain):
	try:
		print("Looking up AAAA records")
		answer = dns.resolver.resolve(str(domain), rdtype=dns.rdatatype.AAAA)
		#print(answer.response.answer[0][0])
		return answer.response.answer[0][0]
	except:
		pass

def getNSrecord(domain):
	try:
		print("Looking up NS records")
		if domain == None:
			return "null"
		answer = dns.resolver.resolve(domain, 'NS')
		#print(answer.response.answer[0][0])
		return answer.response.answer[0][0]
	except:
		pass

def getASN(ip):
	try:
		print("Looking up ASN")
		if ip == None:
			return "null"
		answer = asndb.lookup(ip)
		#print(answer[0])
		return answer[0]
	except Exception as e:
		pass

def getASInfo(asn):
    print("Looking up ASN Info")
    url = f"https://api.asrank.caida.org/v2/restful/asns/{asn}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        return None

def getOrganizationName(orgId):
	print("Looking up Organization Name")
	url = f"https://api.asrank.caida.org/v2/restful/organizations/{orgId}"
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		return data['data']['organization']['orgName']
	else:
		return None



tranco = pd.read_csv("tranco_230616.csv",
	header=0,
	# names=["position","url"],
	# dtype={"position":int,"url":"string"} 
    names=["position","url","NS","NS-A","NS-AAAA","ASN","ASName","ASSource","ASCountry","OrgName"],
	dtype={"position":int,"url":"string","NS":"string","NS-A":"string","NS-AAAA":"string","ASN":"string","ASName":"string","ASSource":"string","ASCountry":"string","OrgName":"string"}
)

tranco_df = pd.DataFrame(tranco)
# tranco_df["NS"] = "null"
# tranco_df["NS-A"] = "null"
# tranco_df["NS-AAAA"] = "null"
# tranco_df["ASN"] = "null"
# tranco_df["ASName"] = "null"
# tranco_df["ASSource"] = "null"
#tranco_df["ASCountry"] = "null"
#tranco_df["OrgName"] = "null"


print(tranco)



requestsCount = 0

for i in range(472165,MILLION):
	#print(tranco_df.iloc[i])

	ns = tranco_df.at[i,"NS"]
	url = tranco_df.at[i,"url"]
	orgName = tranco_df.at[i,"OrgName"]
	#print(ns)
	ccTLD = url.split(".")[-1]
	#ccTLD=urlDecomposed[-1]

	if pd.isna(orgName) and (("br" == ccTLD) or ("ru" == ccTLD) or ("cn" == ccTLD) or ("in" == ccTLD) or ("eu" == ccTLD) or ("za" == ccTLD)):
		requestsCount+=1
		
		print("------------  Testing: " + url + " ----------------")
		
		urlNS = getNSrecord(url)
		tranco_df.at[i,"NS"] = str(urlNS)
		
		nsIP = getArecords(urlNS)
		if nsIP == None:
			continue
		tranco_df.at[i,"NS-A"] = str(nsIP)
		tranco_df.at[i,"NS-AAAA"]=str(getAAAArecords(urlNS))
		
		nsASN = getASN(str(nsIP))
		if nsASN == None:
			continue
		tranco_df.at[i,"ASN"]=str(nsASN)

		asInfo = getASInfo(nsASN)
		print(asInfo)
		if (asInfo != None):
				tranco_df.at[i,"ASName"]=asInfo['asn']['asnName']
				tranco_df.at[i,"ASSource"]=asInfo['asn']['source']
				tranco_df.at[i,"ASCountry"]=asInfo['asn']['country']['iso']
				tranco_df.at[i, "OrgName"]=getOrganizationName(asInfo['asn']['organization']['orgId'])
		
		tranco_df.to_csv('tranco_230616.csv',sep=',', index=False, encoding='utf-8')
	if requestsCount==1000:
		requestsCount=0
		time.sleep(60)
#print(tranco)
		