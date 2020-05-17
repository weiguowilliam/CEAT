"""
Detection of emergent biases from the emergent paper.

Test with 2 accuracy. (i.e. for AF)
1. emergent bias of AF + emergent bias of EM
2. emergent bias of AF + intersectional bias of AF
"""

import random
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

############## name ###########################
adj_abw = ['shrill', 'loud', 'argumentative', 'irrational', 'angry', 'abusive', 'obnoxious', 'controlling', 'nagging', 'brash', 'hostile', 'emasculating', 'mean', 'harsh', 'sassy', 'aggressive', 'opinionated', 'domineering']
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

#################### bias ###########################

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

latino_female_intersectional_bias = ['feisty','curvy','cook','promiscuous','sexy','maids']

latino_female_bias = ['feisty','curvy', 'loud', 'attractive', 'cook', 'darkskinned', 'uneducated', 'hardworker' ,'promiscuous','unintelligent','short','sexy', 'maids']

latino_male_intersectional_bias = ['promiscuous', 'jealous', 'violent', 'drunks']

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

def inner(uniscore_1,uniscore_2,multiscore_1,multiscore_2,multiscore_3,thre_u,thre_m):
    if (uniscore_1>thre_u)+(uniscore_2>thre_u)  == 0:  
        if (multiscore_1 > thre_m) + (multiscore_2 > thre_m)+(multiscore_3>thre_m) != 0:
            return True
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    acc_lst = []
    tp_lst = []
    acc_lst_af = []
    tp_lst_af = []
    tp_lst_lf = []
    acc_lst_lf = []
    acc_lst_abw = []
    tp_lst_abw = []
    use_em = 2
    european_male_intersectional_bias = european_male_intersectional_bias+african_male_bias+latino_male_bias
    for tt in np.array(range(5,19))/10:
        [t_u, t_m] = [tt]*2
        output_lst = []

    ################# af ###########################
        df = pd.read_csv('race_all_words_new.csv')
        csv_lst = list(df['paper'])

        
        af_bias = [wd for wd in african_female_intersectional_bias] #only account the emergent bias
        if use_em == 1:
            em_bias = [wd for wd in european_male_intersectional_bias]
            share_wd = [wd for wd in african_female_intersectional_bias if wd in european_male_intersectional_bias]
        elif use_em == 0:
            em_bias = [wd for wd in african_female_bias if wd not in african_female_intersectional_bias]
            
            share_wd = []
        elif use_em == 2:
            
            em_bias = ['rich','tall','intelligent','assertive','arrogant','successful','high-status','blond','racist']
            share_wd = [wd for wd in african_female_intersectional_bias if wd in em_bias]
        else: #-1
            em_bias_1 = [wd for wd in european_male_intersectional_bias]
            em_bias_2 = [wd for wd in african_female_bias if wd not in african_female_intersectional_bias]
            em_bias = list(set(em_bias_1 + em_bias_2))
            share_wd = [wd for wd in african_female_intersectional_bias if wd in em_bias]

        if share_wd != []:
            for wd in share_wd:
                af_bias.remove(wd)
                em_bias.remove(wd)
        


        em_bias = em_bias[:len(af_bias)]



        wd_lst = list(df['paper'])
        afef_lst = list(df['afef'])
        afam_lst = list(df['afam'])
        afem_lst = list(df['afem'])
        ae_lst = list(df['ae'])
        fm_lst = list(df['fm_a'])
        
        true_lst = [1] * len(af_bias) + [0] * len(em_bias)
        pred_lst = []
        for wd in af_bias+em_bias:
            idx = wd_lst.index(wd)
            pred_lst.append(inner(uniscore_1 = ae_lst[idx], uniscore_2=fm_lst[idx], multiscore_1=afef_lst[idx], multiscore_2=afam_lst[idx],multiscore_3 = afem_lst[idx],thre_u = t_u, thre_m=t_m))
        
        cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
        # print(true_lst)
        # print(pred_lst)
        # print(af_bias+em_bias)
        tp_wd_lst = [wd for idx,wd in enumerate(af_bias+em_bias) if (pred_lst[idx] == True) and (true_lst[idx] == 1)]
        # print(tp_wd_lst)
        # print(cm)
        tn_1, fn_1, tp_1, fp_1 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
        acc_1 = (cm[0,0]+cm[1,1])/len(true_lst)
        output_lst.append([tn_1, fn_1, tp_1, fp_1, acc_1])
        acc_lst_af.append(acc_1)
        tp_lst_af.append(tp_1)

    #################### am ###################
        # df = pd.read_csv('paper_am.csv')
        # csv_lst = list(df['paper'])
        
        # am_bias = [wd for wd in african_male_intersectional_bias]
        # # em_bias = [wd for wd in european_male_intersectional_bias]
        # if use_em == 1:
        #     em_bias = [wd for wd in european_male_intersectional_bias]
        #     share_wd = [wd for wd in african_male_intersectional_bias if wd in european_male_intersectional_bias]
        # elif use_em == 0:
        #     em_bias = [wd for wd in african_male_bias if wd not in african_male_intersectional_bias]
        #     share_wd = []
        # else:
        #     em_bias_1 = [wd for wd in european_male_intersectional_bias]
        #     em_bias_2 = [wd for wd in african_male_bias if wd not in african_male_intersectional_bias]
        #     em_bias = list(set(em_bias_1 + em_bias_2))
        #     share_wd = [wd for wd in african_male_intersectional_bias if wd in em_bias]

        # for wd in share_wd:
        #     am_bias.remove(wd)
        #     em_bias.remove(wd)


        # wd_lst = list(df['paper'])
        # ae_lst = list(df['ae'])
        # fm_lst = list(df['fm'])
        # amem_lst = list(df['amem'])
        # afam_lst = list(df['afam'])
        
        # true_lst = [1] * len(am_bias) + [0] * len(em_bias)
        # pred_lst = []
        # for wd in am_bias+em_bias:
        #     idx = wd_lst.index(wd)
        #     pred_lst.append(inner(uniscore_1 = ae_lst[idx], uniscore_2=-fm_lst[idx], multiscore_1=amem_lst[idx], multiscore_2=-afam_lst[idx],thre_u = t_u, thre_m=t_m))
        #     # pred_lst.append(inner(multiscore_1 = amem_lst[idx], multiscore_2 = -afam_lst[idx], thre_m = t))
        
        # cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
        # tn_2, fn_2, tp_2, fp_2 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
        # acc_2 = (cm[0,0]+cm[1,1])/len(true_lst)
        # print(cm)

        # output_lst.append([tn_2, fn_2, tp_2, fp_2, acc_2])   

    ################# lf ##############

        df = pd.read_csv('race_all_words_new.csv')
        csv_lst = list(df['paper'])
        
        lf_bias = [wd for wd in latino_female_intersectional_bias]
        if use_em == 1:
            em_bias = [wd for wd in european_male_intersectional_bias]
            share_wd = [wd for wd in latino_female_intersectional_bias if wd in european_male_intersectional_bias]
        elif use_em == 0:
            em_bias = [wd for wd in latino_female_bias if wd not in latino_female_intersectional_bias]
            share_wd = []
        elif use_em == 2:
            # em_bias = [wd for wd in european_male_bias]
            em_bias= ['rich','tall','intelligent','assertive','arrogant','successful']
            share_wd = [wd for wd in latino_female_intersectional_bias if wd in em_bias]
        else:
            em_bias_1 = [wd for wd in european_male_intersectional_bias]
            share_wd = [wd for wd in latino_female_intersectional_bias if wd in european_male_intersectional_bias]
            em_bias_2 = [wd for wd in latino_female_bias if wd not in latino_female_intersectional_bias]
            em_bias = list(set(em_bias_1+em_bias_2))

        if share_wd != []:
            for wd in share_wd:
                lf_bias.remove(wd)
                em_bias.remove(wd)
        
        em_bias = em_bias[:len(lf_bias)]


        print(lf_bias)
        print(em_bias)

        wd_lst = list(df['paper'])
        le_lst = list(df['le'])
        fm_lst = list(df['fm_l'])
        lfef_lst = list(df['lfef'])
        lflm_lst = list(df['lflm'])
        lfem_lst = list(df['lfem'])
        
        true_lst = [1] * len(lf_bias) + [0] * len(em_bias)
        pred_lst = []
        for wd in lf_bias+em_bias:
            idx = wd_lst.index(wd)
            pred_lst.append(inner(uniscore_1 = le_lst[idx], uniscore_2=fm_lst[idx], multiscore_1=lfef_lst[idx], multiscore_2=lflm_lst[idx],multiscore_3 = lfem_lst[idx],thre_u = t_u, thre_m=t_m))
            # pred_lst.append(inner(multiscore_1 = lfef_lst[idx], multiscore_2 = lflm_lst[idx], thre_m = t))
        
        cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
        tn_3, fn_3, tp_3, fp_3 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
        # print(cm)
        acc_3 = (cm[0,0]+cm[1,1])/len(true_lst)

        acc_lst_lf.append(acc_3)
        tp_lst_lf.append(tp_3)
        # output_lst.append([tn_3, fn_3, tp_3, fp_3, acc_3])

    ################## lm ######################
        # df = pd.read_csv('paper_le.csv')
        # csv_lst = list(df['paper'])
        
        # lm_bias = [wd for wd in latino_male_intersectional_bias]
        # if use_em == 1:
        #     em_bias = [wd for wd in european_male_intersectional_bias]
        #     share_wd = [wd for wd in latino_male_intersectional_bias if wd in european_male_intersectional_bias]
        # elif use_em == 0:
        #     em_bias = [wd for wd in latino_male_bias if wd not in latino_male_intersectional_bias]
        #     share_wd = []
        # else:
        #     em_bias_1 = [wd for wd in european_male_intersectional_bias]
        #     share_wd = [wd for wd in latino_male_intersectional_bias if wd in european_male_intersectional_bias]        
        #     em_bias_2 = [wd for wd in latino_male_bias if wd not in latino_male_intersectional_bias]
        #     em_bias = list(set(em_bias_1+em_bias_2))

        # if share_wd != []:
        #     for wd in share_wd:
        #         lm_bias.remove(wd)
        #         em_bias.remove(wd)


        # wd_lst = list(df['paper'])
        # le_lst = list(df['le'])
        # fm_lst = list(df['fm'])
        # lmem_lst = list(df['lmem'])
        # lflm_lst = list(df['lflm'])
        
        # true_lst = [1] * len(lm_bias) + [0] * len(em_bias)
        # pred_lst = []
        # for wd in lm_bias+em_bias:
        #     idx = wd_lst.index(wd)
        #     pred_lst.append(inner(uniscore_1 = le_lst[idx], uniscore_2=-fm_lst[idx], multiscore_1=lmem_lst[idx], multiscore_2=-lflm_lst[idx],thre_u = t_u, thre_m=t_m))
        #     # pred_lst.append(inner(multiscore_1 = lmem_lst[idx], multiscore_2 = -lflm_lst[idx], thre_m = t))
        
        # cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
        # tn_4, fn_4, tp_4, fp_4 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
        # print(cm)
        # acc_4 = (cm[0,0]+cm[1,1])/len(true_lst)

        # output_lst.append([tn_4, fn_4, tp_4, fp_4, acc_4])

        # tn_all = tn_1+tn_3
        # fn_all = fn_1+fn_3
        # tp_all = tp_1+tp_3
        # fp_all = fp_1+fp_3
        # acc_all = (tn_all+tp_all)/(tn_all+tp_all+fn_all+fp_all)
        # acc_af = (tn_1+tp_1)/(tn_1+tp_1+fn_1+fp_1)
        # acc_lf = (tn_3+tp_3)/(tn_3+tp_3+fn_3+fp_3)
        # acc_lst.append(acc_all)
        # acc_lst_af.append(acc_af)
        # acc_lst_lf.append(acc_lf)
        # tp_lst.append(tp_all)



        # acc_all = (tn_1+tn_2+tn_3+tn_4+tp_1+tp_2+tp_3+tp_4)/(tn_1+tn_2+tn_3+tn_4+tp_1+tp_2+tp_3+tp_4+fn_1+fn_2+fn_3+fn_4+fp_1+fp_2+fp_3+fp_4)
        # output_lst.append([tn_all,fn_all,tp_all,fp_all,acc_all])
        # print("all acc: "+str(acc_all))
        # c_all  = np.array([[tn_all,fp_all],[fn_all,tp_all]])
        # print(c_all)
        # acc_lst.append(acc_all)
        # tp_lst.append(tp_all)
    
    # print(acc_lst)
    print(acc_lst_af)
    # print(tp_lst_af)
    print(acc_lst_lf)
    # print(tp_lst_lf)
    # print(tp_lst)

