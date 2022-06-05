import json
import spacy
from tqdm import tqdm
from spacy.tokens import DocBin

with open('./NER_Training/NER_train_data.json', 'r') as file:
    data = json.load(file) # import training data obtained from https://tecoholic.github.io/ner-annotator/

def rand_split_list(list, split_ratio):

    import random
    random.shuffle(list)
    split = round(len(list)*split_ratio)
    train_data = list[:split]
    test_data = list[split:]

    return train_data, test_data

train, valid = rand_split_list(list = data, split_ratio = 0.8)


def convert(input_list,output_path):
    nlp = spacy.blank("en") # load a new spacy model
    db = DocBin() # create a DocBin object
    TRAIN_DATA = input_list
    try:
        for text, annot in tqdm(TRAIN_DATA): # data in previous format
            doc = nlp.make_doc(text) # create doc object from text
            ents = []
            for start, end, label in annot["entities"]: # add character indexes
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                if span is None:
                    print("Skipping entity")
                else:
                    ents.append(span)
            doc.ents = ents # label the text with the ents
            db.add(doc)
    except:
        pass
    db.to_disk(output_path)

convert(input_list= train, output_path="./NER_Training/training_db/training_data_outcomes.spacy")
convert(input_list= valid, output_path="./NER_Training/training_db/validation_data_outcomes.spacy")