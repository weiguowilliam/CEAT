#generate vectors for all words for all sentences in Bert-small-case, gpt, GPT-2, also should for elmo
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import torch

import spacy
from transformers import BertModel, BertTokenizer
from transformers import GPT2Tokenizer, GPT2LMHeadModel,GPT2Model
from allennlp.commands.elmo import ElmoEmbedder
from transformers import OpenAIGPTTokenizer, OpenAIGPTModel
import logging
logging.getLogger('transformers.tokenization_utils').disabled = True
import numpy as np
import json
import pickle

tokenizer_gpt2 = GPT2Tokenizer.from_pretrained('gpt2')
model_gpt2 = GPT2LMHeadModel.from_pretrained('gpt2', output_hidden_states=True)
model_gpt2.eval()

tokenizer_bert = BertTokenizer.from_pretrained('bert-base-cased')
model_bert = BertModel.from_pretrained('bert-base-cased')
model_bert.eval()

tokenizer_gpt = OpenAIGPTTokenizer.from_pretrained('openai-gpt')
model_gpt = OpenAIGPTModel.from_pretrained('openai-gpt')
model_gpt.eval()

def bert(i):
    n = '/sentences_pickle/weat{}.pickle'.format(i)
    pickle_in = open(n,"rb")
    sen_dict = pickle.load(pickle_in)
    pickle_in.close()
    
    out_dict_bert = {wd:[] for wd in sen_dict}
    # out_dict_gpt2 = {wd:[] for wd in sen_dict}
    for wd in sen_dict:
        for sen in sen_dict[wd]:
            #bert part
            input_ids = torch.tensor(tokenizer_bert.encode(sen, add_special_tokens=False)).unsqueeze(0) 
            outputs = model_bert(input_ids)
            exact_state_vector = outputs[0][0,:,:].detach().numpy() #it's a matrix containing vectors for all subtokens
            out_dict_bert[wd].append(exact_state_vector)

    
    m = '/vector_pickle/weat{}_bert.pickle'.format(i)
    pickle_out = open(m,"wb")
    pickle.dump(out_dict_bert,pickle_out)
    pickle_out.close()

def gpt2(i):
    n = '/sentences_pickle/weat{}.pickle'.format(i)
    pickle_in = open(n,"rb")
    sen_dict = pickle.load(pickle_in)
    pickle_in.close()
    
    out_dict_bert = {wd:[] for wd in sen_dict}
    # out_dict_gpt2 = {wd:[] for wd in sen_dict}
    for wd in sen_dict:
        for sen in sen_dict[wd]:
            #bert part
            input_ids = torch.tensor(tokenizer_gpt2.encode(sen,add_prefix_space=True)).unsqueeze(0) 
            outputs = model_gpt2(input_ids)
            exact_state_vector = outputs[2][-1][0,:,:].detach().numpy() #it's a matrix containing vectors for all subtokens
            out_dict_bert[wd].append(exact_state_vector)

    
    m = '/vector_pickle/weat{}_gpt2.pickle'.format(i)
    pickle_out = open(m,"wb")
    pickle.dump(out_dict_bert,pickle_out)
    pickle_out.close()

def gpt(i):
    n = '/sentences_pickle/weat{}.pickle'.format(i)
    pickle_in = open(n,"rb")
    sen_dict = pickle.load(pickle_in)
    pickle_in.close()
    
    out_dict_bert = {wd:[] for wd in sen_dict}
    # out_dict_gpt2 = {wd:[] for wd in sen_dict}
    for wd in sen_dict:
        for sen in sen_dict[wd]:
            #bert part
            input_ids = torch.tensor(tokenizer_gpt.encode(sen)).unsqueeze(0) 
            outputs = model_gpt(input_ids)
            exact_state_vector = outputs[0][0,:,:].detach().numpy() #it's a matrix containing vectors for all subtokens
            out_dict_bert[wd].append(exact_state_vector)

    
    m = '/vector_pickle/weat{}_gpt.pickle'.format(i)
    pickle_out = open(m,"wb")
    pickle.dump(out_dict_bert,pickle_out)
    pickle_out.close()

def elmo(i):
    n = '/sentences_pickle/weat{}.pickle'.format(i)
    pickle_in = open(n,"rb")
    sen_dict = pickle.load(pickle_in)
    pickle_in.close()
    nlp = spacy.load("en_core_web_sm")

    out_dict_bert = {wd:[] for wd in sen_dict}

    options_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_options.json"
    weight_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"
    elmo = ElmoEmbedder(options_file,weight_file)

    for wd in sen_dict:
        for sen in sen_dict[wd]:
            doc = nlp(sen)
            sen_tokens = [token.text for token in doc]
            q_embeddings = elmo.embed_sentence(sen_tokens)
            exact_vector = q_embeddings[:,:,:].sum(axis=0)
            out_dict_bert[wd].append(exact_vector)
    
    m = '/vector_pickle/weat{}_elmo.pickle'.format(i)
    pickle_out = open(m,"wb")
    pickle.dump(out_dict_bert,pickle_out)
    pickle_out.close()


for i in range(1,11):
    elmo(i)
    print("ELmo for {} is finished.".format(i))
    bert(i)
    print("Bert for {} is finished.".format(i))
    gpt(i)
    print("GPT for {} is finished.".format(i))
    gpt2(i)  
    print("GPT-2 for {} is finished.".format(i))  





