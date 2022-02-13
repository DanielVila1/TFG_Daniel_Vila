import scispacy
import spacy
from spacy import displacy

import googletrans
from googletrans import Translator

from negspacy.negation import Negex

from spacy.tokens import Span

import en_core_sci_sm
import en_ner_bc5cdr_md

import os
import json
from sutime import SUTime

from pathlib import Path

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

# Modelo en_ner_bc5cdr_md (disease, chemical)
nlp_bc5cdr = spacy.load("en_ner_bc5cdr_md")

# Modelo en_core_sci_sm (ENTITY)
nlp_core = spacy.load("en_core_sci_sm")

# Negaciones (negspacy, negex)
nlp_core.add_pipe("negex", config={"ent_types":["DISEASE"]})


# Informe de entrada
test_doc = Path('informe.txt').read_text()

# Traduccion
translator = Translator()
src = 'es'
dest = 'en'
traduccion = translator.translate(txt, src=src, dest=dest)
test_doc = traduccion.text

test_doc = decontracted(test_doc)

# Aplicar el nlp
# doc es el documento con las entidades
doc = nlp_core(test_doc)

# doc2 es el documento con las enfermedades y quimicos
doc2 = nlp_bc5cdr(test_doc)


ents = list(doc.ents)
ents2 = list(doc2.ents)
y = 0

# Añadir etiqueta temporal
sutime = SUTime(mark_time_ranges=True, include_range=True)

print(json.dumps(sutime.parse(test_doc), sort_keys=True, indent=4))
print(sutime.parse(test_doc))
time_terms = sutime.parse(test_doc)


for idx, e in enumerate(doc2.ents):
	if e._.negex == True:
		new_ent = Span(doc2, e.start, e.end, label="TIME")
		ents[idx] = new_ent
	else:
		ents[idx] = e

for tt in time_terms:
	idx = idx + 1
	new_ent = Span(doc2, tt['start'], tt['end'], label="TIME")
	ents[idx] = new_ent

doc2.ents = ents2



# Modificar parametros de visualización
def get_entity_options():
    entities = ["DISEASE", "CHEMICAL", "I_Disease", "B_Disease", "ENTITY", "NEG_ENTITY", "TIME"]
    colors = {'DISEASE': 'linear-gradient(180deg, #66ffcc, #abf763)', 'CHEMICAL': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)', "NEG_ENTITY":'linear-gradient(90deg, #ffff66, #ff6600)', 'ENTITY': 'linear-gradient(590dfg, #5232cc, #bbf763)', "TIME":'linear-gradient(50deg, #ffbb66, #ff4440)'}
    options = {"ents": entities, "colors": colors}    
    return options




options = get_entity_options()


for element in doc2.ents:
	print(element, element.label_)


displacy.serve(doc2, style='ent', options=options)