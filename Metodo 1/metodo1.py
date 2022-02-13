import nltk

# Descomentar la primera vez para descargar
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('treebank')

from nltk.stem import PorterStemmer
from nltk.corpus import treebank

from spacy import displacy
import en_core_web_sm

import googletrans
from googletrans import Translator

import json
import requests # Database access
import re
import urllib.request # En caso de que de error de SSL usar este metodo 



#numInforme = input("Numero de informe: \n")

informeName = "informe.txt"

nlp = en_core_web_sm.load()




# Junta todas las permutaciones en una busqueda
def permutaciones1(keywords):

	busquedaP = [] # Busqueda con el elemento previo
	busquedaN = [] # Busqueda con el elemento posterior
	busquedaT = [] # Busqueda con el previo y el posterior
	busquedaU = [] # Busqueda solo con el NN-
	busquedas = [[]] 
	

	ln = len(keywords)


	n = 0
	prevI = ("","")
	while(n < ln):
		actual = keywords[n]

		#if actual[1] == 'NN' or actual[1] == 'NNP' :
		# NN, NNP, NNS
		if actual[1].startswith('NN') and (actual[0] != prevI[0]):  
			busquedaP.append(actual)
			busquedaN.append(actual)
			busquedaT.append(actual)
			busquedaU.append(actual)
			if n > 0:
				prevI = keywords[n-1]
				busquedaP.append(prevI)
				busquedaT.append(prevI)
			if n+1 < ln:
				nextI = keywords[n+1]
				busquedaN.append(nextI)
				busquedaT.append(nextI)

			busquedas.append(set(busquedaP))
			busquedas.append(set(busquedaN))
			busquedas.append(set(busquedaT))
			busquedas.append(set(busquedaU))

		n+=1
	permutaciones = []
	for b in busquedas:
		if b not in permutaciones:
			permutaciones.append(b)

	print(permutaciones[1:])

	return permutaciones[1:]

# Determinar negaciones
def put_sign2(words):
	wordsSign = []
	names = []
	synonyms = []

	for index, word in enumerate(words):
		wordsSign.append({'name': [], 'synonym': []})
		wordsSignName = procesar(word["name"])

		if word['synonym'] != None:
			wordsSignSynonym = procesar(word['synonym'])
		else:
			wordsSignSynonym = []
		for phrasesSN in wordsSignName:
			for wordsSN in phrasesSN:
				wordsSign[index]['name'].append(wordsSN)
		for phrasesSS in wordsSignSynonym:
			for wordsSS in phrasesSS:
				wordsSign[index]['synonym'].append(wordsSS)

	return wordsSign

# Eliminar contracciones
def decontracted(phrase):
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


# Determinar términos cronológicos
def temporales(txt):
	result = []
	for x in txt.split("."):
		frase = nlp(decontracted(x))

		for dic in diccionario_temporales:
			if dic in frase.text:
				result.append(frase.text)
				break
	return result

# Obtener la raiz de las palabras para una busqueda mas generica
def stemming(relevant):
	namesSteemed = [[[("", "", "", ""),("", "", "", "")], [("", "","", ""),("", "","", "")]]]
	namesSteemedAux = []
	aux = ('', '', False, 0)
	ps = PorterStemmer()
	namesSteemed.pop()

	for idx1, term in enumerate(relevant):
		for idx2, word in enumerate(term):
			w = ps.stem(word[0])
			if word[0].endswith("y") and w.endswith("i"):
				w = w[:-1] + "y"
			aux = (w, word[1], word[2], word[3], word[4], word[0])

			namesSteemedAux.append(aux)

		namesSteemed.append(namesSteemedAux)
		namesSteemedAux = []

	return namesSteemed

# Obtener la raiz de las frases a comparar para calcular la coincidencia
def stemming2(phrase):

	porter = PorterStemmer()

	token_words= nltk.word_tokenize(phrase)
	token_words
	stem_sentence=[]
	for word in token_words:
		stem_sentence.append(porter.stem(word))
		stem_sentence.append(" ")
	return "".join(stem_sentence)



# Determina el porcentaje de coincidencia entre la frase 
# del informe y el término HPO para poder seleccionar
# el más adecuado
def match(original, find, phraseNum):

	original = original.split(".")	
	findS = ""
	for word in find:
		findS = findS + " " + word[0]

	# Raices 
	string1 = stemming2(original[phraseNum])
	string2 = stemming2(findS)

	# Eliminar caracteres no alfanumericos
	s1aux = ''.join(filter(str.isalnum, string1))
	s2aux = ''.join(filter(str.isalnum, string2))

	s1 = string1.split(" ")
	s2 = string2.split(" ")

	# Se quita el ultimo elemento porque detecta que es un ''
	N = len(s2[:-1])


	for accI in range(len(s1)):
		s1[accI] = s1[accI].lower()
	for accI in range(len(s2)):
		s2[accI] = s2[accI].lower()

	matches = 0

	s1 = s1[:-1]
	s2 = s2[:-1]

	for w_ in s2:
		if w_ in s1:
			matches += 1

	if N != 0:
		accuracy = str((matches / N) * 100)
	else:
		accuracy = "0"
	return str(matches) + "/" + str(N) + " = " + accuracy + " %"

# Búsquedas en la ontología
idxTempAux = -1
def buscar2(relevant, permuta):
	global idxTempAux

	relevant = stemming(relevant)

	for keywords in relevant:  
		while keywords[0][3] > idxTempAux:
			idxTempAux += 1
			resultado.write("\n\n\n" +"HIST: " + lista_temporales[idxTempAux])
		
		sign_error = False
		empty = True
		busqueda = ""
		originales = ""
		synonymsNegation = [("","")]

		muchasCoincidencias = False

		for words in keywords:
			busqueda = busqueda.replace("–", "-")
			busqueda = busqueda.replace("’", '\'')

			
			if "'" in words[0]:
				busqueda = busqueda + "%20" + words[0].split("'")[0]
				originales = originales + " " + words[5]
			else:
				busqueda = busqueda + "%20" + words[0]
				originales = originales + " " + words[5]

			busqueda = busqueda.replace("–", "-")
			busqueda = busqueda.replace("’", '\'')


		# Si las busquedas no van acompañandas de un elemento significante no se realizan
		busquedaT = nltk.word_tokenize(busqueda)
		busquedaTagged = nltk.pos_tag(busquedaT)
		meaningless = True
		for element in busquedaTagged:
			if 'NN' in element:
				meaningless = False
				break
			if 'NNS' in element:
				meaningless = False
				break
			if 'NNP' in element:
				meaningless = False
				break


		if meaningless:
			print("No sense: ", busqueda)
			break

		url = "https://hpo.jax.org/api/hpo/search/?q="+ busqueda +"&max=-1&offset=0&category=terms"

		r = urllib.request.urlopen(url).read()
		jsonResponse = json.loads(r.decode('utf-8'))

		y = jsonResponse

		resultado.write("\n\t______________\n\n" + "\tTerm: "+ originales)

		# Contexto
		resultado.write("\n\tContext: "+ str(keywords[0][4]-1) + "\n")


		if len(y["terms"]) >= 9:
			muchasCoincidencias = True

		if y["terms"] == [] and not permuta:
			buscar2(permutaciones1(keywords), True)
			continue


		if muchasCoincidencias:
			negationsAux = put_sign2(y["terms"][:10])
		else:
			negationsAux  = put_sign2(y["terms"])
	
		i = 0
		sign_error = False

		for finds in negationsAux:

			if sign_error:
				break
			
			for name in finds["name"]:
				for kWord in keywords:
					if (negationsAux == []):
						break
					if (name[0].lower()  in kWord[0].lower() ) or (kWord[0].lower()  in name[0].lower() ):
						if name[1] != kWord[2]:
							comprobar = False
							if  (name[0] in "conscious") or ("conscious" in name[0]):
								comprobar = True
							sign_error = True
							negationsAux.pop(i)
							break
			i+=1

		

		# Si se considera que la búsqueda es poco precisa
		"""
		if len(y["terms"]) >= 100:
			continue
		"""
		for t in negationsAux:
			
			empty = True
			if t.get("name") != [] or t.get("synonym") != []:
				empty = False

				if muchasCoincidencias:
					all_same = False
					for t2 in t.get("name"):
						if(t2[0].lower() == words[0].lower()):
							all_same = True
						else:
							all_same = False
							break
					if all_same:
						resultado.write("\n(Muchas coincidencias) ")

				resultado.write("\n\tEncontrado:\n")

				resultado.write("\t\tName:")

				for t2 in t.get("name"):
					resultado.write(" " + t2[0])

				resultado.write("\t  Coincidencia: " + (match(txt, t.get("name"), keywords[0][4])))
				resultado.write("\n\t\tSynonym:")

				for t2 in t.get("synonym"):
					resultado.write(" " + t2[0])
				
				resultado.write("\t  Coincidencia: " + (match(txt, t.get("synonym"), keywords[0][4])))


			if(empty and not permuta):
				buscar2(permutaciones1(keywords), True)
				


#informeName = "Resultados\\test\\informe" + numInforme + ".txt"
txt_data = open(informeName,"rt")
txt = txt_data.read()
txt_data.close()

txt = txt.encode('ascii', 'ignore').decode('ascii')

# Traduccion
translator = Translator()
src = 'es'
dest = 'en'
traduccion = translator.translate(txt, src=src, dest=dest)
test_doc = traduccion.text

txt = decontracted(test_doc)
txt = txt.replace("-"," ")
txt = txt.replace("'"," \'")
txt = txt.replace("/"," / ")


aux = 0
auxTxt = txt.replace("–", "-")
auxTxt = auxTxt.replace("-"," - ")
auxTxt = auxTxt.replace("<"," < ")
auxTxt = auxTxt.replace(">"," > ")
auxTxt = auxTxt.replace("<"," < ")

auxTxt = auxTxt.replace("/"," / ")
auxTxt = auxTxt.replace("("," ( ")
auxTxt = auxTxt.replace(")"," ) ")

sentences = auxTxt.split(". ")
tokens = [''] * len(sentences)
tagged = [''] * len(sentences)


for sentence in (sentences):
  tokens[aux] = nltk.word_tokenize(sentence)
  tokens[aux]
  tagged[aux] = nltk.pos_tag(tokens[aux])
  tagged[aux][0:6]
  aux += 1
 



# Stopwords
with open ("stopwords.txt", "r") as file:
    irrelevant = file.readlines()

relevant = [[[("", "", "", ""),("", "", "", "")], [("", "","", ""),("", "","", "")]]]

negations = ["no", "not", "don", "doesn", "didn", "none", "never", "nobody", "isn", "shouldn", "wouldn", "couldn", "won", "negative"]


porter = PorterStemmer()

diccionario_temporalesAux = ["year", "month", "week", "day", "hour", "years", "months", "weeks", "days", "hours"]

diccionario_temporalesStemmed = []

for termTemp in diccionario_temporalesAux:
	diccionario_temporalesStemmed.append(porter.stem(termTemp))

diccionario_temporales = diccionario_temporalesAux + diccionario_temporalesStemmed




#aux1 = 0
#aux2 = 0

# Obtener las negaciones mediante iterar cada lista de hijos 
# que están afectados por la negación

negativeWords = []




# Obtener los terminos afectados por el detonante de la negacion
def get_negations(tokens, sentenceNLP):

	if tokens == []:
		return
	child_list = []

	for token in tokens:
		for child in token.children:
			for index, tok in enumerate(sentenceNLP):
				if tok == child and tok.dep_ != "ccomp":
					if tok.head == child.head:
						"""
						print("tok.text = ", tok.text)
						print("tok H = ", tok.head)
						print("child H = ", child.head)
						print("tok dep = ", tok.dep)
						print("child dep = ", child.dep)
						"""
						if tok not in child_list:
							child_list.append(child)
							negativeWords.append((child, index))

	get_negations(child_list, sentenceNLP)

	if negativeWords == None:
		return []
	else:
		return negativeWords




def procesar(doc):

	resultado = []
	sentences = doc.split(". ")

	sentenceAcc = 0	# -1
	for sentence in sentences:

		sentenceAcc += 1
		docNegation = []
		sentenceNLP = nlp(sentence)
		
	
		# Negaciones directas
		negation_tokens = [tok for tok in sentenceNLP if tok.dep_ == 'neg']
		negation_head_tokens = [token.head for token in negation_tokens]
	
		# Negaciones mediante preposiciones (without)
		prepAux = [tok for tok in sentenceNLP if tok.dep_ == 'prep' and tok.text == "without"]
		negation_head_tokens = negation_head_tokens + prepAux
		
		# Negaciones para los resultados de tests clinicos
		testNeg = [tok for tok in sentenceNLP if tok.text == "negative"]
		testNegH = [token.head for token in testNeg]
		negation_head_tokens = negation_head_tokens + testNegH
		
		# Negaciones mediante det  (head head?)  *!*
		#detAux = [tok for tok in sentenceNLP if tok.dep_ == 'det' and tok.text == "no"]
		#detAuxH = [token.head for token in detAux]
		#detAuxHH =  [token.head for token in detAuxH]
		#negation_head_tokens = negation_head_tokens + detAuxH

		detAux = [tok for tok in sentenceNLP if tok.text == 'no' or tok.text == "non" or tok.text == 'no-' or tok.text == "non-"]
		
		softNeg = []
		boolAux = False
		for tok in sentenceNLP:
			if boolAux == True:
				softNeg.append(tok)
				boolAux = False
			if tok.text == 'no' or tok.text == "non" or tok.text == 'no-' or tok.text == "non-":
				boolAux = True


		# Indice de los terminos que implican negacion
		indexRootN = []
		indexRootN2 = []
		for index, tok in enumerate(sentenceNLP):
			if tok in negation_head_tokens:
				indexRootN.append(index)
				print("indexRootN = ", indexRootN)
			elif tok in softNeg:
				indexRootN2.append(index)
				print("indexRootN2 = ", indexRootN)


		aux = []
		negationList = []
		headList = []
		negationList = get_negations(negation_head_tokens, sentenceNLP)
	
		if negationList == None:
			negationList = []

		for index, word in enumerate(sentenceNLP):
			if "\n" in word.text:
				continue

			
			if (index in indexRootN) or (index in indexRootN2):
				docNegation.append((word.text,"Neg", sentenceAcc))
				continue
			auxBool = False

			
			for neg in negationList:
				if word.text.replace(".", "") == neg[0].text.replace(".", "") and index == neg[1]:
					docNegation.append((word.text,"Neg", sentenceAcc))
					auxBool = True

			
			if (not auxBool):
				docNegation.append((word.text,"Pos", sentenceAcc))

		resultado.append(docNegation)

	print("Resultado = ", resultado)

	return resultado
	


# Determinar si un término es relevante
def relevancia(tagged, negativos):

	temporal_id = -1
	aux1 = 0

	for tag, neg in zip(tagged, negativos):
		negAcc = -1
		phraseBool = True

		for tag2 in tag:
			negAcc += 1

			if phraseBool:
				for tempAux in diccionario_temporales:
					if (tempAux in tag2[0]):
						temporal_id += 1
						phraseBool = False
						break

			while (neg[negAcc][0] == " "):
				negAcc += 1

			if len(tag2) > 1:
				if aux1 == 1:
					if not tag2[0] + "\n" in irrelevant: 
						if "non" in tag2[0].lower():
							softNegation = True

						if tag2[1] == 'NN':
							relevant[-1][-1].append((tag2[0], tag2[1],  neg[negAcc][1], temporal_id, neg[negAcc][2]))
						elif tag2[1] == 'IN':
							aux = 1
						elif tag2[1] == 'JJ':
							relevant[-1][-1].append((tag2[0], tag2[1], neg[negAcc][1], temporal_id, neg[negAcc][2]))
						elif tag2[1] == 'RB':
							relevant[-1][-1].append((tag2[0], tag2[1], neg[negAcc][1], temporal_id, neg[negAcc][2]))
						elif tag2[1] == 'NNS':
							relevant[-1][-1].append((tag2[0], tag2[1], neg[negAcc][1], temporal_id, neg[negAcc][2]))
						elif tag2[1] == 'POS':
							relevant[-1][-1].append((tag2[0], tag2[1], neg[negAcc][1], temporal_id, neg[negAcc][2]))
						elif tag2[1] == 'NNP':
							relevant[-1][-1].append((tag2[0], tag2[1], neg[negAcc][1], temporal_id, neg[negAcc][2]))
						else:
							aux1 = 0
					else:
						aux1 = 0
				else:
					if tag2[1] == 'NN' or tag2[1] == 'JJ':
						if not tag2[0] in irrelevant:
							relevant[-1].append([(tag2[0], tag2[1], neg[negAcc][1], temporal_id, neg[negAcc][2])])
							aux1 = 1
			else:
				aux1 = 0
	relevant[0].pop(0)
	relevant[0].pop(0)


	return relevant[0]




procesado = procesar(txt)

relevant = relevancia(tagged, procesado)

resultadoName = "Resultados\\" + informeName
resultado = open(resultadoName,"w+")

lista_temporales = temporales(txt)
print("lista = ", lista_temporales)

buscar2(relevant, False)

resultado.close()



