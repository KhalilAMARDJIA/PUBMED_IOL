python -m spacy init fill-config ./NER_Training/base_config.cfg ./NER_Training/config.cfg

python -m spacy debug data ./NER_Training/config.cfg

python -m spacy train ./NER_Training/config.cfg --output ./NER_Training/models/outcome_model