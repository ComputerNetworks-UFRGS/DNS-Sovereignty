import dns.resolver
import subprocess
import concurrent.futures
import os
import re
import glob
import shutil
from datetime import date
import downloader

iphash = {}
ip6hash = {}
asnhash = {}

pastanova = "Resultados" + str(date.today())
os.mkdir(pastanova)

arquivo = glob.glob('routeviews-rv2*')
arquivo = str(arquivo)
arquivo = arquivo[:-2]
arquivo = arquivo[2:]


with open (arquivo, "r") as ip:
	for line in ip:
		token = line.split('	')
		rede = token[0]
		asn = token[2]
		iphash[rede] = asn

<<<<<<< HEAD:Medicao.py
#os.remove(arquivo)			
=======
os.remove(arquivo)			
>>>>>>> bd3860eed0eecfc7ce7e56685ace9f68dd0fe7c0:TCC8.py

arquivo = glob.glob('routeviews-rv6*')
arquivo = str(arquivo)
arquivo = arquivo[:-2]
arquivo = arquivo[2:]

with open (arquivo, "r") as ip6:
	for line in ip6:
		token = line.split('	')
		rede = token[0]
		asn = token[2]
		ip6hash[rede] = asn
		
<<<<<<< HEAD:Medicao.py
#os.remove(arquivo)

arquivo = glob.glob('*.as-org2info.txt')
arquivo = str(arquivo)
arquivo = arquivo[:-2]
arquivo = arquivo[2:]


=======


arquivo = glob.glob('*.as-org2info.txt')
arquivo = str(arquivo)
arquivo = arquivo[:-2]
arquivo = arquivo[2:]


>>>>>>> bd3860eed0eecfc7ce7e56685ace9f68dd0fe7c0:TCC8.py
with open (arquivo, "r") as asn:
	for line in asn:		
		token = line.split('|')
		try:
			asn = token[0]
			org = token[2]
			asnhash[asn] = org
		except:
			pass
<<<<<<< HEAD:Medicao.py
#os.remove(arquivo)
=======
os.remove(arquivo)
>>>>>>> bd3860eed0eecfc7ce7e56685ace9f68dd0fe7c0:TCC8.py
	
Domainlist = []


arquivo = glob.glob('*.csv')
arquivo = str(arquivo)
arquivo = arquivo[:-2]
arquivo = arquivo[2:]


with open (arquivo, 'r') as dominios:
	for dominio in dominios:
		dominio = ''.join([i for i in dominio if not i.isdigit()])
		dominio = dominio[1:]
		Domainlist.append(dominio)
		
<<<<<<< HEAD:Medicao.py


=======


>>>>>>> bd3860eed0eecfc7ce7e56685ace9f68dd0fe7c0:TCC8.py
shutil.move ("/home/user/" + arquivo, "/home/user/" + pastanova)

def getArecords (nsrecord):
	nsrecord = nsrecord[:-1]
	Arecord = []
	try:
		query = dns.resolver.resolve(nsrecord, 'A')
		for item in query:
			Arecord.append(item.to_text())
		return Arecord
		
	except:
		pass


def getAAAArecords (nsrecord):
	nsrecord = nsrecord[:-1]
	AAAArecord = []
	try:
		query = dns.resolver.resolve(nsrecord, 'AAAA')
		for item in query:
			AAAArecord.append(item.to_text())
		return AAAArecord
		
	except:
		pass


def querydominio (dominio):
	domainNSList = []
	Arecords = []
	AAAArecords = []
	dominio = dominio[:-1]
	listaempresas = []
	tempA = []
	tempAAAA = []
	
	try:	
		NS = dns.resolver.resolve(dominio, 'NS')
		for answer in NS.response.answer:
			for item in answer.items:
				domainNSList.append(item.to_text())
		
		
		for nsrecord in domainNSList:
			tempA = getArecords(nsrecord)
			for ip in tempA:
				Arecords.append(ip)
			tempAAAA = getAAAArecords(nsrecord)
			for ip in tempAAAA:
				AAAArecords.append(ip)
		
		
		
		for line in Arecords:
			token = line.split('.')
			token[3] = 0
			mascara = str(token[0]) + "." + str(token[1]) + "." + str(token[2]) + "." + str(token[3])
			try:
				empresa = asnhash[iphash[mascara][:-1]]
				if empresa not in listaempresas:
					listaempresas.append(empresa)
			
			except:
				pass
		
		for line in AAAArecords:
			token = line.split(':')
			mascara = str(token[0]) + ":" + str(token[1]) + ":" + str(token[2]) + "::"
			try:
				empresa = asnhash[ip6hash[mascara][:-1]]
				if empresa not in listaempresas:
					listaempresas.append(empresa)
			except:
				pass
		
		
		if len(listaempresas) != 0:
			try:
				print (dominio, domainNSList, Arecords, AAAArecords, listaempresas)
				
				listaempresas = str(listaempresas)
				with open ('Medição dia' + str(date.today()), 'a') as file:
						file.write('#######################################################')
						file.write("\n")
						file.write("dominio \n")
						file.write(str(dominio))
						file.write("\nlista de NS records \n")
						file.write(str(domainNSList))
						file.write("\nlista de A records \n")
						file.write(str(Arecords))
						file.write("\nlista de AAAA records \n")
						file.write(str(AAAArecords))
						file.write("\nlista de empresas \n")
						file.write(str(listaempresas))
						file.write("\n")
						file.close()
				
			except:
				pass
		else:
			with open ('Erro Medição dia' + str(date.today()), 'a') as file:
				file.write('nao encontrado a empresa do dominio' + ' ' + dominio)
				file.write('\n')
	except:
		pass
		
	

with concurrent.futures.ProcessPoolExecutor(max_workers=200) as executor:
	for result in executor.map(querydominio, Domainlist):
		pass

<<<<<<< HEAD:Medicao.py

=======
shutil.move ("/home/user/Medição dia" + str(date.today()), "/home/user/" + pastanova)
shutil.move ("/home/user/Erro Medição dia" + str(date.today()), "/home/user/" + pastanova)
>>>>>>> bd3860eed0eecfc7ce7e56685ace9f68dd0fe7c0:TCC8.py


concentracao = {}
controle = 1

with open ('Medição dia' + str(date.today()), 'r') as arquivo:
	for line in arquivo:
		line = str(line)		
		if controle == 11:
			if line in concentracao.keys():
				concentracao[line] = concentracao[line] + 1
			else:
				concentracao[line] = 1
			controle = 1
		else:	
			controle = controle + 1



for item in sorted (concentracao, key = concentracao.get, reverse=True):
<<<<<<< HEAD:Medicao.py
	with open ('Concentracao dia' + str(date.today()), 'a') as file:
		porcentagem = concentracao[item]/10000
		#print(porcentagem)
		file.write(item.strip() + ':' + str(concentracao[item]).strip() + ':' + str(porcentagem) + '\n')
		
		

shutil.move ("/home/user/Concentracao dia" + str(date.today()), "/home/user/" + pastanova)
shutil.move ("/home/user/Medição dia" + str(date.today()), "/home/user/" + pastanova)
shutil.move ("/home/user/Erro Medição dia" + str(date.today()), "/home/user/" + pastanova)



=======
	with open ('Concentracao dia' + str(date.today()), 'w') as file:
		file.write(item, concentracao[item])

shutil.move ("/home/user/Concentracao dia" + str(date.today()), "/home/user/" + pastanova)
>>>>>>> bd3860eed0eecfc7ce7e56685ace9f68dd0fe7c0:TCC8.py
