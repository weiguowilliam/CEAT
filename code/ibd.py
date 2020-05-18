"""
calculate confusion matrix for Intersectional biases(not for emergent biases)

use all words in intersectional paper as possible words
"""

import pandas as pd
import pickle
import numpy as np
from scipy import spatial
from scipy.special import comb, perm
import random
import scipy.stats
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from itertools import product
from sklearn.metrics import confusion_matrix

################### name ###############################

latino_female = ['Maria','Yesenia','Adriana','Liset','Mayra','Alma','Ana','Carolina','Iliana','Sonia',
                    'Karina','Alejandra','Brenda','Vanessa','Diana'][0:15]
latino_male = ['Jesús','Rigoberto','César','Rogelio','Angel','José','Pedro','Antonio','Alberto','Alejandro',
                  'Alfredo','Jorge','Juan','Miguel','Ricardo'][0:15]

european_female = ['Melanie','Colleen','Ellen','Emily','Sarah','Rachel',
'Carrie','Stephanie','Megan','Amanda','Nancy', 'Katie','Heather','Betsy','Kristin'][0:15]
european_male = ['Frank', 'Lauren', 'Jill', 'Roger', 'Neil', 'Geoffrey',
 'Brad', 'Stephen', 'Peter', 'Brendan', 'Meredith', 'Jack', 
 'Allison', 'Matthew', 'Jonathan', 'Josh', 'Andrew', 'Greg',
  'Justin', 'Alan', 'Todd', 'Ryan', 'Courtney', 'Adam',
   'Laurie', 'Brett', 'Harry', 'Anne', 'Paul'][0:15]

african_female = ['Yvette','Aisha','Malika','Latisha','Keisha','Tanisha','Tamika',
'Yolanda','Nichelle','Latoya','Lakisha','Shereen','Shaniqua','Jasmine','Tia','Kenya'][0:15]
african_male = ['Lionel', 'Wardell', 'Deion', 'Jamel', 'Marcellus', 'Ebony', 
'Kareem', 'Torrance', 'Lamar', 'Jamal', 'Leroy', 'Lavon', 'Tyrone', 'Alphonse'
, 'Hakim', 'Malik', 'Terrence', 'Rasheed', 'Theo', 'Jerome', 'Alonzo', 
'Jermaine', 'Tyree', 'Lamont', 'Darnell'][0:15]


#################### bias ###############################
african_common_bias = ['ghetto', 'unrefined', 'criminals', 'athletic', 'loud', 'gangsters', 'poor', 'uneducated', 'dangerous', 'violent', 'tall', 'lazy']

african_male_intersectional_bias = ['darkskinned', 'rapper', 'hypersexual']

african_male_bias = ['athletic', 'loud', 'tall', 
                     'violent', 'dangerous', 'poor', 'unintelligent', 
                     'gangsters', 'lazy', 'criminals']+african_male_intersectional_bias

african_female_intersectional_bias = ['bigbutt','overweight','confident','darkskinned','assertive',
                                      'promiscuous','unfeminine','aggressive','fried-chicken']

african_female_bias = ['loud','ghetto','unrefined','athletic','unintelligent']+african_female_intersectional_bias

european_common_bias = ['high-status', 'rich', 'intelligent', 'arrogant', 'privileged', 'blond', 'racist', 'all-American', 
                        'ignorant', 'red-neck', 'attractive','tall', 'patronizing', 'blue-eyes', 'overweight']

european_male_intersectional_bias = ['assertive','successful','educated']
european_male_bias = ['rich','intelligent','arrogant','high-status','blond','racist','all-American',
                     'leader','privileged','attractive','tall', 'sexist'] + european_male_intersectional_bias

european_female_intersectional_bias = ['ditsy','sexually-liberal']
european_female_bias = ['arrogant','blond','rich','attractive','petite','tall','materialistic','racist',
                       'intelligent','feminine','emotional','submissive','high-status'] + european_female_intersectional_bias

male_common_bias = ['tall','respected','intelligent','high-status','leader','sexist','provider',
                   'aggressive','unfaithful','ambitious','arrogant','messy','fixer-upper']

female_common_bias = ['emotional','caring','soft','talkative','petite','submissive','dependent','motherly',
                     'feminine','manipulative','attractive','materialistic','jealous']

latino_female_bias = ['feisty','curvy', 'loud', 'attractive', 'cook', 'darkskinned', 'uneducated', 'hardworker' ,'promiscuous','unintelligent','short','sexy', 'maids']

latino_male_bias = ['macho', 'poor', 'darkskinned', 'day-laborer', 'promiscuous', 'short', 'hardworker', 'jealous', 'uneducated', 'illegal-immigrant', 'arrogant', 'unintelligent', 'aggressive', 'violent', 'drunks']

latino_common_bias = ['poor', 'illegal-immigrant', 'darkskinned', 'uneducated', 'family-oriented', 'lazy', 'day-laborer', 'unintelligent', 'loud', 'gangster', 'short', 'overweight', 'macho', 'hardworker']

paper_lst = list(set(african_common_bias+african_male_bias+african_female_bias+european_common_bias+european_male_bias+european_female_bias+male_common_bias+female_common_bias+latino_female_bias+latino_male_bias+latino_common_bias))


def get_effectsize(wd,A,B):
    cos_a = cosine_similarity(wd,A) #.mean()
    cos_b = cosine_similarity(wd,B) #.mean()
    cos_ab = np.concatenate((cos_a,cos_b),axis=1)
    delta_mean =   cos_a.mean() - cos_b.mean()
    std = np.std(cos_ab,ddof=1)
    return delta_mean/std

def get_mtx(lst,dic):
    out = dic[lst[0]]
    for wd in lst[1:]:
        out = np.concatenate((out,dic[wd]),axis=0)
    return out


def inner(multiscore_1, multiscore_2, multiscore_3, thre_m):
    if (multiscore_1>thre_m) or (multiscore_2>thre_m) or (multiscore_3>thre_m):
    # if (multiscore_1>thre_m) or (multiscore_2>thre_m) :
        return 1 # intersectional -> 1
    else:
        return 0

if __name__ == '__main__':
    t = 0.8
    ac_lst = []
    ac_lst_1 = []

    tpr_af = []
    fpr_af = []
    tpr_lf = []
    fpr_lf = []

    # for t in  np.array(range(5,18))/10:
    for t in np.array(range(1,20))/10:
    
    
    ######af ####
        df = pd.read_csv('race_all_words_new.csv')
        wd_lst =  list(df['paper'])
        af_bias = [wd for wd in african_female_bias if wd not in european_male_bias]
        # no_bias = [wd for wd in wd_lst if wd not in af_bias]
        no_bias = [wd for wd in european_male_bias if wd not in african_female_bias][:len(af_bias)]

        
        afef_lst = list(df['afef'])
        afam_lst = list(df['afam'])
        afem_lst = list(df['afem'])

        true_lst = [1] * len(af_bias) + [0] * len(no_bias)
        pred_lst = []
        for wd in af_bias+no_bias:
            idx = wd_lst.index(wd)
            pred_lst.append(inner(multiscore_1 = afef_lst[idx], multiscore_2 = afam_lst[idx],multiscore_3 = afem_lst[idx], thre_m = t))
        
        cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
        tn_1, fn_1, tp_1, fp_1 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
        print(cm)
        acc_1 = (cm[0,0]+cm[1,1])/len(true_lst)
        print(acc_1)
        ac_lst.append(acc_1)
    

    ######lf ####
        df = pd.read_csv('race_all_words_new.csv')
        wd_lst =  list(df['paper'])
        af_bias = [wd for wd in latino_female_bias if wd not in european_male_bias]
        # no_bias = [wd for wd in wd_lst if wd not in af_bias]
        no_bias = [wd for wd in european_male_bias if wd not in latino_female_bias][:len(af_bias)]

        print(af_bias)
        print(no_bias)
        
        afef_lst = list(df['lfef'])
        afam_lst = list(df['lflm'])
        afem_lst = list(df['lfem'])

        true_lst = [1] * len(af_bias) + [0] * len(no_bias)
        pred_lst = []
        for wd in af_bias+no_bias:
            idx = wd_lst.index(wd)
            pred_lst.append(inner(multiscore_1 = afef_lst[idx], multiscore_2 = afam_lst[idx], multiscore_3 = afem_lst[idx], thre_m = t))
        
        cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
        tn_1, fn_1, tp_1, fp_1 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
        print(cm)
        acc_1 = (cm[0,0]+cm[1,1])/len(true_lst)
        print(acc_1)
        ac_lst_1.append(acc_1)
    print(ac_lst)
    print(ac_lst_1)

    # t = 1.3 get highest accuracy


        
