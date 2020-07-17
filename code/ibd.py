"""
IBD, EIBD test and draw roc curve
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
import matplotlib.pyplot as plt




################### name ###############################

african_female = ['Yvette','Aisha','Malika','Latisha','Keisha','Tanisha',
'Tamika', 'Yolanda','Nichelle','Latoya','Lakisha','Shereen','Shaniqua',
'Jasmine','Tia'][0:12]
# delete:  Kenya

african_male = ['Lionel', 'Wardell',  'Jamel', 'Marcellus',
  'Jamal', 'Leroy',  'Tyrone', 'Alphonse'
, 'Hakim', 'Terrence', 'Jerome', 'Alonzo'][0:12]
#delete: Deion, Ebony, Kareem,Lamar,Lavon,Malik,Rasheed,Jermaine,
# Tyree,Lamont,Darnell,Torrance,Theo

european_female = ['Melanie','Colleen','Ellen','Emily','Sarah','Rachel',
'Carrie','Stephanie','Megan','Nancy', 'Katie','Heather','Betsy',
'Kristin'][0:12]
#delete: Amanda

european_male = ['Frank',   'Roger', 'Neil', 'Geoffrey',
 'Brad', 'Stephen', 'Peter',   'Jack', 
'Matthew', 'Jonathan', 'Josh', 'Andrew', 'Greg',
  'Justin', 'Alan',    'Adam',
    'Harry',  'Paul'][0:12]
#delete: Lauren,Jill,Brendan,Meredith,Allison,Todd,Ryan,Courtney,Laurie,Brett,Anne

mexican_female = ['Maria','Yesenia','Adriana','Liset','Mayra','Alma',
'Carolina','Iliana','Sonia',
                    'Karina','Alejandra','Brenda','Vanessa','Diana'][0:12]
# delete: Ana
mexican_male = ['Jesús','Rigoberto','César','Rogelio','José','Pedro',
'Antonio','Alberto','Alejandro',
                  'Alfredo','Juan','Miguel','Ricardo'][0:12]
# delete: Angel,Jorge


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

european_female_intersectional_bias = ['ditsy'] #,'sexually-liberal'
european_female_bias = ['arrogant','blond','rich','attractive','petite','tall','materialistic','racist',
                       'intelligent','feminine','emotional','submissive','high-status'] + european_female_intersectional_bias

male_common_bias = ['tall','respected','intelligent','high-status','leader','sexist','provider',
                   'aggressive','unfaithful','ambitious','arrogant','messy','fixer-upper']

female_common_bias = ['emotional','caring','soft','talkative','petite','submissive','dependent','motherly',
                     'feminine','manipulative','attractive','materialistic','jealous']


mexican_female_intersectional_bias = ['feisty','curvy','cook','promiscuous','sexy','maids']

mexican_female_bias = ['feisty','curvy', 'loud', 'attractive', 'cook', 'darkskinned', 'uneducated', 'hardworker' ,'promiscuous','unintelligent','short','sexy', 'maids']

mexican_male_intersectional_bias = ['promiscuous', 'jealous', 'violent', 'drunks']

mexican_male_bias = ['macho', 'poor', 'darkskinned', 'day-laborer', 'promiscuous', 'short', 'hardworker', 'jealous', 'uneducated', 'illegal-immigrant', 'arrogant', 'unintelligent', 'aggressive', 'violent', 'drunks']


mexican_common_bias = ['poor', 'illegal-immigrant', 'darkskinned', 'uneducated', 'family-oriented', 'lazy', 'day-laborer', 'unintelligent', 'loud', 'gangster', 'short', 'overweight', 'macho', 'hardworker']

insect = ['ant', 'caterpillar', 'flea', 'locust', 'spider', 'bedbug', 'centipede', 'fly', 'maggot', 'tarantula', 'bee', 'cockroach', 'gnat', 'mosquito', 'termite', 'beetle', 'cricket', 'hornet', 'moth', 'wasp', 'blackfly', 'dragonfly', 'horsefly', 'roach', 'weevil']

# flower = ['aster', 'clover', 'hyacinth', 'marigold', 'poppy', 'azalea', 'crocus', 'iris', 'orchid', 'rose', 'bluebell', 'daffodil', 'lilac', 'pansy', 'tulip', 'buttercup', 'daisy', 'lily', 'peony', 'violet', 'carnation', 'gladiola', 'magnolia', 'petunia', 'zinnia']

# paper_lst = list(set(african_common_bias+african_male_bias+african_female_bias+european_common_bias+european_male_bias+european_female_bias+male_common_bias+female_common_bias+mexican_female_bias+mexican_male_bias+mexican_common_bias+insect+flower))


paper_lst = list(set(african_common_bias+african_male_bias+african_female_bias+european_common_bias+european_male_bias+european_female_bias+male_common_bias+female_common_bias+mexican_female_bias+mexican_male_bias+mexican_common_bias+insect))

# without gender and race bias
# paper_lst = list(set(african_male_bias+african_female_bias+european_male_bias+european_female_bias+mexican_female_bias+mexican_male_bias+insect))


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


def inner_ibd(multiscore_1, multiscore_2, multiscore_3,multiscore_4,multiscore_5, thre_m):
    if (multiscore_1>thre_m) or (multiscore_2>thre_m) or (multiscore_3>thre_m) or (multiscore_4>thre_m)or (multiscore_5>thre_m):
    # if (multiscore_1>thre_m) or (multiscore_2>thre_m) :
        return 1 # intersectional -> 1
    else:
        return 0

def inner_eibd(uniscore_1,uniscore_2,uniscore_3,multiscore_1,multiscore_2,multiscore_3,multiscore_4,multiscore_5,thre_u,thre_m):
    if (uniscore_1>thre_u)+(uniscore_2>thre_u)+(uniscore_3>thre_u)  != 3:  # only drop the itmes who is both high in gender and race
        # if use ==0, drop the items who is either high in gender or high in race -> get less positive answer
        if (multiscore_1 > thre_m) + (multiscore_2 > thre_m)+(multiscore_3>thre_m)+(multiscore_4>thre_m)+ (multiscore_5>thre_m) != 0:
            return True
        else:
            return False
    else:
        return False

t = 0.8
ac_lst = []
ac_lst_1 = []

tpr_af = []
fpr_af = []
tpr_lf = []
fpr_lf = []
tp_af = []
tp_lf = []

# for t in  np.array(range(5,18))/10:
for t in np.array(range(-200,200,5))/100:


######af ####
    df = pd.read_csv('race_all_words_6.csv')
    wd_lst =  list(df['paper'])
    af_bias = [wd for wd in african_female_bias]
    no_bias = [wd for wd in paper_lst if wd not in af_bias]
    

    afef_lst = list(df['afef'])
    afam_lst = list(df['afam'])
    afem_lst = list(df['afem'])
    aflf_lst = list(df['aflf'])
    aflm_lst = list(df['aflm'])

    true_lst = [1] * len(af_bias) + [0] * len(no_bias)
    pred_lst = []
    for wd in af_bias+no_bias:
        idx = wd_lst.index(wd)
        pred_lst.append(inner_ibd(multiscore_1 = afef_lst[idx], multiscore_2 = afam_lst[idx],multiscore_3 = afem_lst[idx],
                                  multiscore_4 = aflf_lst[idx], multiscore_5 = aflm_lst[idx], thre_m = t))

    cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
    tn_1, fn_1, tp_1, fp_1 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
    acc_1 = (cm[0,0]+cm[1,1])/len(true_lst)
    tpr_af.append(tp_1/(tp_1+fn_1))
    fpr_af.append(fp_1/(fp_1+tn_1))
    ac_lst.append(acc_1)
    tp_af.append(tp_1)


######lf ####
    df = pd.read_csv('race_all_words_6.csv')
    wd_lst =  list(df['paper'])
    af_bias = [wd for wd in mexican_female_bias]
    # no_bias = [wd for wd in wd_lst if wd not in af_bias]
    no_bias = [wd for wd in paper_lst if wd not in af_bias]


    afef_lst = list(df['lfef'])
    afam_lst = list(df['lflm'])
    afem_lst = list(df['lfem'])
    aflf_lst = list(df['lfaf'])
    aflm_lst = list(df['lfem'])

    true_lst = [1] * len(af_bias) + [0] * len(no_bias)
    pred_lst = []
    for wd in af_bias+no_bias:
        idx = wd_lst.index(wd)
        pred_lst.append(inner_ibd(multiscore_1 = afef_lst[idx], multiscore_2 = afam_lst[idx], multiscore_3 = afem_lst[idx],
                                  multiscore_4 = aflf_lst[idx], multiscore_5 = aflm_lst[idx],thre_m = t))

    cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
    tn_1, fn_1, tp_1, fp_1 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
    tpr_lf.append(tp_1/(tp_1+fn_1))
    fpr_lf.append(fp_1/(fp_1+tn_1))
    acc_1 = (cm[0,0]+cm[1,1])/len(true_lst)
    ac_lst_1.append(acc_1)
    tp_lf.append(tp_1)

# # t = 1.3 get highest accuracy

tpr_af_use = []
for i in list(zip(tpr_af,fpr_af,ac_lst)):
    if i not in tpr_af_use:
        tpr_af_use.append(i)

fpr = [i[1] for i in tpr_af_use]
tpr = [i[0] for i in tpr_af_use]

import matplotlib
matplotlib.rcParams['figure.figsize'] = [7, 7] # for square canvas
matplotlib.rcParams['figure.subplot.left'] = 0
matplotlib.rcParams['figure.subplot.bottom'] = 0
matplotlib.rcParams['figure.subplot.right'] = 1
matplotlib.rcParams['figure.subplot.top'] = 1
plt.scatter(fpr,tpr)
plt.plot(fpr,tpr,label='AF intersectional bias',linewidth=2,color='black',markeredgecolor='black',marker='o')
plt.plot([0,1],[0,1],ls='--',linewidth=2,color='black')
plt.xlabel('False positive rate',fontsize=40,weight='bold')
plt.ylabel('True positive rate',fontsize=40,weight='bold')
plt.legend(loc='lower right',fontsize=32,prop={'weight':'bold','size':30})
plt.xticks(fontsize= 26)
plt.yticks(fontsize= 26)
plt.scatter(0.10714285714285714, 0.35714285714285715,s=200,color='black')
plt.xlim(-0.01,1.01)
plt.ylim(-0.01,1.01)
plt.savefig('roc/af_inter.pdf',bbox_inches='tight')
plt.show()

tpr_lf_use = []
for i in list(zip(tpr_lf,fpr_lf,ac_lst_1)):
    if i not in tpr_lf_use:
        tpr_lf_use.append(i)

fpr = [i[1] for i in tpr_lf_use]
tpr = [i[0] for i in tpr_lf_use]

import matplotlib
matplotlib.rcParams['figure.figsize'] = [7, 7] # for square canvas
matplotlib.rcParams['figure.subplot.left'] = 0
matplotlib.rcParams['figure.subplot.bottom'] = 0
matplotlib.rcParams['figure.subplot.right'] = 1
matplotlib.rcParams['figure.subplot.top'] = 1
plt.scatter(fpr,tpr)
plt.plot(fpr,tpr,label='MF intersectional bias',linewidth=2,color='black',markeredgecolor='black',marker='o')
plt.plot([0,1],[0,1],ls='--',linewidth=2,color='black')
plt.xlabel('False positive rate',fontsize=40,weight='bold')
plt.ylabel('True positive rate',fontsize=40,weight='bold')
plt.legend(loc='lower right',fontsize=32,prop={'weight':'bold','size':30})
plt.xticks(fontsize= 26)
plt.yticks(fontsize= 26)
# plt.scatter(0.07692307692307693, 0.6153846153846154,s=200)
plt.scatter(0.10588235294117647, 0.38461538461538464,s=200,color='black')
plt.xlim(-0.01,1.01)
plt.ylim(-0.01,1.01)
plt.savefig('roc/lf_inter.pdf',bbox_inches='tight')
plt.show()

tpr_af_lst = []
fpr_af_lst = []
tpr_lf_lst = []
fpr_lf_lst = []
ac_af_lst = []
ac_lf_lst = []
tp_af_lst = []
tp_lf_lst = []

use_em = 2
# 1: use em; 0: use itself's intersectional bias(drop the emergent one) -1: both 0 & 1
# european_male_intersectional_bias = european_male_intersectional_bias+african_male_bias+mexican_male_bias
# for tt in np.array(range(5,18))/10:
for tt in np.array(range(-200,200,5))/100:
    # accuracy based on method 2(af+em)
    [t_u, t_m] = [tt]*2
    output_lst = []

################# af ###########################
    df = pd.read_csv('race_all_words_6.csv')
    csv_lst = list(df['paper'])
    # print([wd for wd in african_female_bias if wd in european_male_bias])



    af_bias = [wd for wd in african_female_intersectional_bias]
    em_bias = [wd for wd in paper_lst if wd not in af_bias]



    wd_lst = list(df['paper'])
    afef_lst = list(df['afef'])
    afam_lst = list(df['afam'])
    afem_lst = list(df['afem'])
    aflf_lst = list(df['aflf'])
    aflm_lst = list(df['aflm'])
    ae_lst = list(df['ae'])
    fm_lst = list(df['fm_a'])
    al_lst = list(df['al'])

    true_lst = [1] * len(af_bias) + [0] * len(em_bias)
    pred_lst = []
    for wd in af_bias+em_bias:
        idx = wd_lst.index(wd)
        pred_lst.append(inner_eibd(uniscore_1 = ae_lst[idx], uniscore_2=fm_lst[idx], uniscore_3 =al_lst[idx],
                                   multiscore_1=afef_lst[idx], multiscore_2=afam_lst[idx],multiscore_3 = afem_lst[idx],
                                   multiscore_4 = aflf_lst[idx],multiscore_5=aflm_lst[idx],
                                   thre_u = t_u, thre_m=t_m))

    cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
    # print(true_lst)
    # print(pred_lst)
    # print(af_bias+em_bias)
    tp_wd_lst = [wd for idx,wd in enumerate(af_bias+em_bias) if (pred_lst[idx] == True) and (true_lst[idx] == 1)]
    # print(tp_wd_lst)
    # print(cm)
    tn_1, fn_1, tp_1, fp_1 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
    acc_1 = (cm[0,0]+cm[1,1])/len(true_lst)
    tpr_af_lst.append(tp_1/(tp_1+fn_1))
    fpr_af_lst.append(fp_1/(fp_1+tn_1))
    ac_af_lst.append(acc_1)
    tp_af_lst.append(tp_1)
    
    
    df = pd.read_csv('race_all_words_6.csv')
    csv_lst = list(df['paper'])




    lf_bias = [wd for wd in mexican_female_intersectional_bias]
    em_bias = [wd for wd in paper_lst if wd not in lf_bias]


    wd_lst = list(df['paper'])
    le_lst = list(df['le'])
    fm_lst = list(df['fm_l'])
    la_lst = list(df['la'])
    lfef_lst = list(df['lfef'])
    lflm_lst = list(df['lflm'])
    lfem_lst = list(df['lfem'])
    lfaf_lst = list(df['lfaf'])
    lfam_lst = list(df['lfam'])

    true_lst = [1] * len(lf_bias) + [0] * len(em_bias)
    pred_lst = []
    for wd in lf_bias+em_bias:
        idx = wd_lst.index(wd)
        pred_lst.append(inner_eibd(uniscore_1 = le_lst[idx], uniscore_2=fm_lst[idx], uniscore_3 = la_lst[idx],
                                   multiscore_1=lfef_lst[idx], multiscore_2=lflm_lst[idx],multiscore_3 = lfem_lst[idx],
                                   multiscore_4=lfaf_lst[idx],multiscore_5=lfam_lst[idx],
                                   thre_u = t_u, thre_m=t_m))
        # pred_lst.append(inner(multiscore_1 = lfef_lst[idx], multiscore_2 = lflm_lst[idx], thre_m = t))

    cm = confusion_matrix(y_true= true_lst, y_pred= pred_lst)
    tn_3, fn_3, tp_3, fp_3 = cm[0,0],cm[1,0],cm[1,1], cm[0,1]
    # print(cm)
    acc_3 = (cm[0,0]+cm[1,1])/len(true_lst)

    tpr_lf_lst.append(tp_3/(tp_3+fn_3))
    fpr_lf_lst.append(fp_3/(fp_3+tn_3))
    ac_lf_lst.append(acc_3)
    tp_lf_lst.append(tp_3)

tpr_af_use = []
for i in list(zip(tpr_af_lst,fpr_af_lst,ac_af_lst)):
    if i not in tpr_af_use:
        tpr_af_use.append(i)

fpr = [i[1] for i in tpr_af_use]
tpr = [i[0] for i in tpr_af_use]

import matplotlib
matplotlib.rcParams['figure.figsize'] = [7, 7] # for square canvas
matplotlib.rcParams['figure.subplot.left'] = 0
matplotlib.rcParams['figure.subplot.bottom'] = 0
matplotlib.rcParams['figure.subplot.right'] = 1
matplotlib.rcParams['figure.subplot.top'] = 1
plt.scatter(fpr,tpr)
plt.plot(fpr,tpr,label='AF emerg inter bias',linewidth=2,color='black',markeredgecolor='black',marker='o')
plt.plot([0,1],[0,1],c='black',ls='--',linewidth=2)
plt.xlabel('False positive rate',fontsize=40,weight='bold')
plt.ylabel('True positive rate',fontsize=40,weight='bold')
plt.legend(loc='lower right',fontsize=32,prop={'weight':'bold','size':30})
plt.xticks(fontsize= 26)
plt.yticks(fontsize= 26)
plt.scatter(0.11235955056179775, 0.4444444444444444,s=200,color='black')
# plt.scatter(0.07692307692307693, 0.6153846153846154)
plt.xlim(-0.01,1.01)
plt.ylim(-0.01,1.01)

plt.savefig('roc/af_unique.pdf',bbox_inches='tight')

tpr_lf_use = []
for i in list(zip(tpr_lf_lst,fpr_lf_lst,ac_lf_lst)):
    if i not in tpr_lf_use:
        tpr_lf_use.append(i)

fpr = [i[1] for i in tpr_lf_use]
tpr = [i[0] for i in tpr_lf_use]

import matplotlib
matplotlib.rcParams['figure.figsize'] = [7, 7] # for square canvas
matplotlib.rcParams['figure.subplot.left'] = 0
matplotlib.rcParams['figure.subplot.bottom'] = 0
matplotlib.rcParams['figure.subplot.right'] = 1
matplotlib.rcParams['figure.subplot.top'] = 1
plt.scatter(fpr,tpr)
plt.plot(fpr,tpr,label='MF emerg inter bias',linewidth=2,color='black',markeredgecolor='black',marker='o')
plt.plot([0,1],[0,1],c='black',ls='--',linewidth=2)
plt.xlabel('False positive rate',fontsize=40,weight='bold')
plt.ylabel('True positive rate',fontsize=40,weight='bold')
plt.legend(loc='lower right',fontsize=32,prop={'weight':'bold','size':30})
plt.xticks(fontsize= 26)
plt.yticks(fontsize= 26)
plt.scatter(0.358695652173913, 0.8333333333333334,s=200,color='black')
# plt.scatter(0.07692307692307693, 0.6153846153846154)
plt.xlim(-0.01,1.01)
plt.ylim(-0.01,1.01)
plt.savefig('roc/lf_unique.pdf',bbox_inches='tight')