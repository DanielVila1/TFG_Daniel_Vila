
import spacy
from pathlib import Path


# Cargar el modelo de spacy
#nlp=spacy.load("en_core_web_sm") 
nlp = spacy.load("en_core_sci_sm")

# Getting the ner component
ner=nlp.get_pipe('ner')

# New label to add
LABEL = "m2"

# Training examples in the required format
TRAIN_DATA =[ ("A previously healthy 7 year old Caucasian boy was hospitalised.", {"entities": [(21, 31, "AGE")]}),
              ("evaluation of acute ataxia and failure to thrive", {"entities": [(14, 26, "DISEASE")]}),
              ("Laboratory studies revealed megaloblastic anaemia", {"entities": [(28,49, "DISEASE")]}),
              ("A 25 year old woman", {"entities": [(2,13, "AGE")]}),
              ("presented a challenging diagnosis of acute rheumatic fever", {"entities": [(37,58, "DISEASE")]}),
              ("We report a 4 year old girl", {"entities": [(12,22, "AGE")]}),
              ("A patient presented with fever", {"entities": [(25,30, "DISEASE")]}), ###
              ("The patient fulfilled the criteria for Sweet syndrome", {"entities": [(39,53, "DISEASE")]}),
              ("A 77 year old man ", {"entities": [(2,13, "AGE")]}),
              ("Fever started 1 day after vaccine administration", {"entities": [(0,5, "DISEASE")]}), ###
              ("he began to experience headache", {"entities": [(23,31, "DISEASE")]}), ###
              ("which later progressed gradually to severe encephalopathy", {"entities": [(36,57, "DISEASE")]}),
              ("history of continuous cough", {"entities": [(11,27, "DISEASE")]}), ####
              ("chest X ray suggesting aspiration pneumonia", {"entities": [(23,43, "DISEASE")]}),
              ("This is a distinctive case of posterior circulation stroke", {"entities": [(30,58, "DISEASE")]}),
              ("presenting with a new continuous cough", {"entities": [(22,38, "DISEASE")]}),  ###
              ("A day before presentation, he developed a sudden onset disequilibrium", {"entities": [(49,69, "DISEASE")]}), ###
              ("he developed sense of vertigo", {"entities": [(13,29, "DISEASE")]}), ###
              ("with associated nausea", {"entities": [(16,22, "DISEASE")]}), ###
              ("several episodes of vomiting while standing", {"entities": [(20,28, "DISEASE")]}),  ###
              ("He described a history of left facial paraesthesia", {"entities": [(31,50, "DISEASE")]}),
              ("Detailed neurological examination revealed subtle left sided incoordination", {"entities": [(61,75, "DISEASE")]}),  ###
              ("There was evident dysarthria", {"entities": [(18,28, "DISEASE")]}),
              ("There was evident impairment in swallowing", {"entities": [(18,42, "DISEASE")]}), ###
              ("the patient was initially suspected to have COVID 19", {"entities": [(44,52, "DISEASE")]}), # 
              ("medical history of hypertension", {"entities": [(19,31, "DISEASE")]}), ###
              ("medical history of Alzheimer’s dementia", {"entities": [(19,39, "DISEASE")]}),
              ("He was investigated with a MRI (figure 1)", {"entities": [(27,30, "DISEASE")]}),
              ("He was investigated with a MRI (fig 1)", {"entities": [(27,30, "DISEASE")]}),
              ("Computed tomography scan of the brain showed left occipital hyperintensity indicating bleeding", {"entities": [(45,74, "DISEASE"),(86,94, "DISEASE") ],}),
              ("Tests showed apathy", {"entities": [(13,19, "DISEASE")]}),
              ("The examination revealed siderosis", {"entities": [(25,34, "DISEASE")]}),
              ("Routine blood tests were regular", {"entities": [(8,19, "TEST")]}),
              ("Computed tomography scan of the brain showed left occipital hyperintensity", {"entities": [(0,24, "TEST"), (50, 74, "DISEASE")]}), ###
              ("Neurological examination revealed bilateral sensorineural hearing", {"entities": [(0,24, "TEST"), (34, 65, "DISEASE")]}),  ###
              ("On neurological examination, the patient was alert, friendly, cooperative and oriented to time , place and person", {"entities": [(3,27, "TEST")]}),
              ("Superficial CNS siderosis is caused by chronic bleeding", {"entities": [(12,15, "DISEASE"), (39, 55, "DISEASE")]}),
              ("The examination revealed brain herniation", {"entities": [(25,41, "DISEASE")]}),
              ("Coagulation studies were regular ( partial thromboplastin time (PTT), international normalised ratio  ( INR ), antithrombin (AT) III, protein C+S, factor VIII , activated protein C resistance, anticardiolipin antibodies ). ", {"entities": [(0,19, "TEST")]}),
              ("history of progressive neurological symptoms manifesting as ataxia, dysarthria and vertigo", {"entities": [(60,66, "DISEASE"), (68,78, "DISEASE"), (83,90, "DISEASE")]}),
              ("The patient was apparently normal 5 years back when he had an episode of fever DISEASE for 4–5 days ", {"entities": [(73,78, "DISEASE")]}),
              ("After 1 month of ataxia, the patient started having a slurred speech. ", {"entities": [(17,23, "DISEASE"),(54,68, "DISEASE")]}),
              ("There was no history of seizures, fever and headache", {"entities": [(24,32, "DISEASE"), (34,39, "DISEASE"), (44,52, "DISEASE")]}),
              ("The patient had horizontal nystagmus", {"entities": [(27,36, "DISEASE")]}),
              ("There was no history of altered sensorium , motor weakness or sensory loss", {"entities": [(24,41, "DISEASE"), (44,58, "DISEASE"), (62,74, "DISEASE")]}),
              ("A 13 month old male child born of a second degree consanguineous marriage presented with delayed milestones; notably, he was not able to pull to sit or stand and he was swaying from side to side when pulled to sit.", {"entities": [(2,14, "AGE"), (89,107, "DISEASE")]}),
              ("The central nervous system examination was remarkable for generalised hypotonia and gross developmental delay", {"entities": [(4,38, "TEST"), (58,79, "DISEASE"),(84,109, "DISEASE")]}),
              ("On attempted sitting he showed truncal ataxia and on approaching an object showed premature grasp and tremulousness.", {"entities": [(31,45, "DISEASE"), (82,97, "DISEASE"), (102,115, "DISEASE")]}),
              ("There was no nystagmus.", {"entities": [(13,22, "DISEASE")]}),
              ("A 64 year old woman presented with progressive hearing loss.", {"entities": [(2,13, "AGE"), (35,59, "DISEASE")]}),
              ("He had suffered mild perinatal hypoxic injury, not requiring prolonged intensive care.", {"entities": [(16,45, "DISEASE")]}),
              ("A 39 year old man with a history of sickle cell disease (SCD) presented with left leg weakness. ", {"entities": [(2,13, "AGE"), (36,61, "DISEASE"), (77,94, "DISEASE")]}),
              ("He had a normal CT head and CT angiogram, but MRI head showed multiple acute bilateral cortical infarcts including in the right precentral gyrus.", {"entities": [(16,23, "TEST"),(28,40, "TEST"), (46,54, "TEST"), (71,104, "DISEASE")]}),
              ("General examination was normal", {"entities": [(0,19, "TEST")]}),
              ("The MRI findings were more in keeping with an embolic source", {"entities": [(4,7, "TEST")]}),
              ("He also had an echocardiogram which revealed a patent foramen ovale", {"entities": [(15,29, "TEST"), (47,67, "DISEASE")]}),
              ("Imaging demonstrated a right frontoparietal haemorrhage of non vascular origin with perilesional oedema.", {"entities": [(0,7, "TEST"),(23,55, "DISEASE"),(84,103, "DISEASE")]}),
              ("Improvement was evident 72 hours after antibiotic initiation, and PCR confirmed periventricular temporoparietal hyperintensity", {"entities": [(66,69, "TEST"), (80,126, "TEST")]}),
              ("There is a progresive slurred speach", {"entities": [(11,36, "DISEASE")]}),
              ("Pending family genetic study for SPG4 ", {"entities": [(15,28, "TEST")]}),
              ("medical history of Alzheimer’s dementia", {"entities": [(19,39, "DISEASE")]})
           ]



# Add the new label to ner
ner.add_label(LABEL)

# Resume training
optimizer = nlp.resume_training()
move_names = list(ner.move_names)

# List of pipes you want to train
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

# List of pipes which should remain unaffected in training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]


from spacy.training.example import Example


# Importing requirements
from spacy.util import minibatch, compounding
import random

# Begin training by disabling other pipeline components
with nlp.disable_pipes(*other_pipes) :

  sizes = compounding(1.0, 4.0, 1.001)
  # Training for 30 iterations     
  for itn in range(50):
    # shuffle examples before training
    random.shuffle(TRAIN_DATA)
    # batch up the examples using spaCy's minibatch
    batches = minibatch(TRAIN_DATA, size=sizes)
    # ictionary to store losses
    losses = {}
    for batch in batches:
      texts, annotations = zip(*batch)
      # Calling update() over the iteration
      example = []
      for i in range(len(texts)):
      	doc = nlp.make_doc(texts[i])
      	example.append(Example.from_dict(doc, annotations[i]))
      nlp.update(example, drop = 0.5, losses = losses)

      print("Losses", losses)


# Output directory
path = ""
output_dir=Path(path)

# Saving the model to the output directory
if not output_dir.exists():
  output_dir.mkdir()
nlp.meta['name'] = 'ner_m2'  # rename model
nlp.to_disk(output_dir)
