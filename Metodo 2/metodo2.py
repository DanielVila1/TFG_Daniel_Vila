import scispacy
import spacy
from spacy import displacy

import en_core_sci_sm
import en_ner_bc5cdr_md

import googletrans
from googletrans import Translator


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

nlp = spacy.load("en_core_sci_sm")




# Cargar el NER entrenado
path = ""
output_dir=Path(path)
nlp1 = spacy.load(output_dir)


# Informe de entrada
test_doc = Path('informe.txt').read_text()

# Traduccion
translator = Translator()
src = 'es'
dest = 'en'
traduccion = translator.translate(txt, src=src, dest=dest)
test_doc = traduccion.text


test_doc = decontracted(test_doc)

doc = nlp(test_doc)

# Lematización
def lemmatize(note, nlp):
    doc = nlp(note)
    lemNote = [wd.lemma_ for wd in doc]
    return " ".join(lemNote)
lem_clinical_note= lemmatize(test_doc, nlp)


doc = nlp1(lem_clinical_note)

# Modificar parametros de visualización
def get_entity_options():
    entities = ["DISEASE", "CHEMICAL", "I_Disease"]
    colors = {'DISEASE': 'linear-gradient(180deg, #66ffcc, #abf763)', 'CHEMICAL': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)', "NEG_ENTITY":'linear-gradient(90deg, #ffff66, #ff6600)'}
    options = {"ents": entities, "colors": colors}    
    return options
options = get_entity_options()

#displacy.render(doc, style='ent', options=options)

for element in doc.ents:
	print(element, element.label_)

displacy.serve(doc, style='ent', options=options)