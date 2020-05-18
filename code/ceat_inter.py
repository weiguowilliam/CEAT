"""
Run CEAT with new defined P-value for race-by-gender
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import scipy.stats
import time as t
import pickle
import random

############ name ################

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



af_bias = ['loud','ghetto','unrefined','athletic','unintelligent']+['bigbutt','overweight','confident','darkskinned','promiscuous','unfeminine','aggressive','fried-chicken']
em_bias_foraf = ['successful','educated']+['rich','intelligent','arrogant','high-status','blond','racist','all-American','leader','privileged','attractive','tall', 'sexist']

af_unique_bias = ['bigbutt','overweight','confident','darkskinned','promiscuous','unfeminine','aggressive','fried-chicken']
em_unique_bias_foraf = ['successful','educated']

lf_bias = ['feisty','curvy', 'loud',  'cook', 'darkskinned', 'uneducated', 'hardworker' ,'promiscuous','unintelligent','short','sexy', 'maids']
em_bias_forlf = ['assertive','successful','educated']+['rich','intelligent','arrogant','high-status','blond','racist','all-American','leader','privileged','attractive','tall', 'sexist']

lf_unique_bias = ['feisty','curvy','cook','promiscuous','sexy','maids']
em_unique_bias_forlf = ['successful','educated','assertive']



def associate(w,A,B):
    return cosine_similarity(w.reshape(1,-1),A).mean() - cosine_similarity(w.reshape(1,-1),B).mean()

def difference(X,Y,A,B):
    # return np.sum(np.apply_along_axis(associate,1,X,A,B)) - np.sum(np.apply_along_axis(associate,1,Y,A,B))

    return np.sum([associate(X[i,:],A,B) for i in range(X.shape[0])]) - np.sum([associate(Y[i,:],A,B) for i in range(Y.shape[0])])

def effect_size(X,Y,A,B):
    # delta_mean = np.mean(np.apply_along_axis(associate,1,X,A,B)) - np.mean(np.apply_along_axis(associate,1,Y),A,B)
    delta_mean =  np.mean([associate(X[i,:],A,B) for i in range(X.shape[0])]) - np.mean([associate(Y[i,:],A,B) for i in range(Y.shape[0])])

    # s = np.apply_along_axis(associate,1,np.concatenate((X,Y),axis=0),A,B)
    XY = np.concatenate((X,Y),axis=0)
    s = [associate(XY[i,:],A,B) for i in range(XY.shape[0])]

    std_dev = np.std(s,ddof=1)

    return delta_mean/std_dev

def inn(a_huge_key_list):
    L = len(a_huge_key_list)
    i = np.random.randint(0, L)
    return a_huge_key_list[i]

weat_groups = [ # 4*2=8
    [african_female,european_male,af_bias,em_bias_foraf], #af-inter
    [african_female,european_male,af_unique_bias,em_unique_bias_foraf], #af-emerg
    # [african_male,european_male,african_male_bias,european_male_bias], #am-inter
    # [african_male,european_male,african_male_intersectional_bias,european_male_intersectional_bias],#am-emerg
    [latino_female,european_male,lf_bias,em_bias_forlf],#lf-inter
    [latino_female,european_male,lf_unique_bias,em_unique_bias_forlf],# lf-emerg
    # [latino_male,european_male,latino_male_bias,european_male_bias],#lm-inter
    # [latino_male,european_male,latino_male_intersectional_bias,european_male_intersectional_bias] #lm-emerg
]

# weat_groups = [ # 4*2=8
#     [african_female,european_male,african_female_bias,european_male_bias], #af-inter
#     [african_female,european_male,african_female_intersectional_bias,european_male_intersectional_bias], #af-emerg
#     # [african_male,european_male,african_male_bias,european_male_bias], #am-inter
#     # [african_male,european_male,african_male_intersectional_bias,european_male_intersectional_bias],#am-emerg
#     [latino_female,european_male,latino_female_bias,european_male_bias],#lf-inter
#     [latino_female,european_male,latino_female_intersectional_bias,european_male_intersectional_bias],# lf-emerg
#     # [latino_male,european_male,latino_male_bias,european_male_bias],#lm-inter
#     # [latino_male,european_male,latino_male_intersectional_bias,european_male_intersectional_bias] #lm-emerg
# ]

def cweat(weat_groups = weat_groups, model='bert',test=1, num_p = 1000, num_mean = 10000,pickle_save= False):
    nm = "data/word_vector/ceat_race_{}_vector.pickle".format(model)
    weat_dict = pickle.load(open(nm,'rb'))
    nm_1 = "name_{}_vector.pickle".format(model)
    name_dict = pickle.load(open(nm_1,'rb'))
    
    el_o = []
    el_s = []
    # get observed es
    t0 = t.time()
    for i in range(num_mean):
        X = np.array([name_dict[wd][np.random.randint(0,len(name_dict[wd]))] for wd in weat_groups[test-1][0]])
        Y = np.array([name_dict[wd][np.random.randint(0,len(name_dict[wd]))] for wd in weat_groups[test-1][1]])
        A = np.array([weat_dict[wd][np.random.randint(0,len(weat_dict[wd]))] for wd in weat_groups[test-1][2]])
        B = np.array([weat_dict[wd][np.random.randint(0,len(weat_dict[wd]))] for wd in weat_groups[test-1][3]])
        el_o.append(effect_size(X,Y,A,B))
    
    mes_o = np.mean(el_o)
    t1 = t.time()
    # print("Observation finished: {}".format(mes_o))
    # print("observation time: {}".format(t1-t0))

    
    
    if pickle_save == True:
        n = '{0}_{1}_eslst.pickle'.format(model,test)
        pickle.dump(el_o,open(n,'wb'))

    # get shuffle
    t2 = t.time()
    for i in range(num_p):

        #shuffle word group for one time
        target_union = weat_groups[test-1][0] + weat_groups[test-1][1]
        l_1 = random.sample(target_union, k=len(weat_groups[test-1][0]))
        l_2 = [wd for wd in target_union if wd not in l_1]

        el_tem = []

        for j in range(num_mean):
            X = np.array([name_dict[wd][np.random.randint(0,len(name_dict[wd]))] for wd in l_1])
            Y = np.array([name_dict[wd][np.random.randint(0,len(name_dict[wd]))] for wd in l_2])
            A = np.array([weat_dict[wd][np.random.randint(0,len(weat_dict[wd]))] for wd in weat_groups[test-1][2]])
            B = np.array([weat_dict[wd][np.random.randint(0,len(weat_dict[wd]))] for wd in weat_groups[test-1][3]])

            # X = np.array([inn(adj_array[wd]) for wd in l_1])
            # Y = np.array([inn(adj_array[wd]) for wd in l_2])
            # A = np.array([inn(adj_array[wd]) for wd in l_3])
            # B = np.array([inn(adj_array[wd]) for wd in l_4])

            el_tem.append(effect_size(X,Y,A,B))
        el_s.append(np.mean(el_tem))

        if i in [200,400,600,800]:
            m,s = np.mean(el_s), np.std(el_s,ddof=1)
            p_2 = 1 - scipy.stats.norm.cdf(mes_o,loc = m, scale = s)
            print("temporary p valus:{}".format(p_2))

    t3 = t.time()

    print("Shuffle finished. Time for shuffle: {}".format(t3-t2))
    # pickle.dump(el_s,open('data/permuted_es/e_af_1000.pickle','wb'))

    m,s = np.mean(el_s), np.std(el_s,ddof=1)
    p_2 = 1 - scipy.stats.norm.cdf(mes_o,loc = m, scale = s)
    # print("P value: {}".format(p_2))

    return mes_o, p_2


def sample_statistics(X,Y,A,B,num = 100):
    XY = np.concatenate((X,Y),axis=0)
   
    def inner_1(XY,A,B):
        X_test_idx = np.random.choice(XY.shape[0],X.shape[0],replace=False)
        Y_test_idx = np.setdiff1d(list(range(XY.shape[0])),X_test_idx)
        X_test = XY[X_test_idx,:]
        Y_test = XY[Y_test_idx,:]
        return difference(X_test,Y_test,A,B)
    
    s = [inner_1(XY,A,B) for i in range(num)]

    return np.mean(s), np.std(s,ddof=1)

def p_value(X,Y,A,B,num=100):
    m,s = sample_statistics(X,Y,A,B,num)
    d = difference(X,Y,A,B)
    p = 1 - scipy.stats.norm.cdf(d,loc = m, scale = s)
    return p

def cweat_for_p(weat_groups = weat_groups, model='bert',test=1, num_p = 1000, num_mean = 10000,pickle_save= False):
    nm = "data/word_vector/ceat_race_{}_vector.pickle".format(model)
    weat_dict = pickle.load(open(nm,'rb'))
    nm_1 = "name_{}_vector.pickle".format(model)
    name_dict = pickle.load(open(nm_1,'rb'))
    
    el_o = []
    # el_s = []
    pl = []
    # get observed es
    for i in range(num_mean):
        X = np.array([name_dict[wd][np.random.randint(0,len(name_dict[wd]))] for wd in weat_groups[test-1][0]])
        Y = np.array([name_dict[wd][np.random.randint(0,len(name_dict[wd]))] for wd in weat_groups[test-1][1]])
        A = np.array([weat_dict[wd][np.random.randint(0,len(weat_dict[wd]))] for wd in weat_groups[test-1][2]])
        B = np.array([weat_dict[wd][np.random.randint(0,len(weat_dict[wd]))] for wd in weat_groups[test-1][3]])
        el_o.append(effect_size(X,Y,A,B))
        pl.append(p_value(X,Y,A,B,num=100))

    nn = 'data/ceat_inter_pses/{0}_{1}.pickle'.format(model,test)
    pickle.dump(pl,open(nn,'wb')) 

    pses = np.mean((np.array(pl) < 0.05))
    pes = np.mean(el_o)
    return pes,pses


if __name__ == '__main__':
    # e_lst =[]
    p_lst = []
    for ee in range(1,5):
        print(ee)
        for m in ['bert','elmo','gpt','gpt2']:
            pes, pses = cweat_for_p(weat_groups=weat_groups,test=ee,model=m,num_p=1000, num_mean = 10000)
            # e_lst.append(e)
            print("pes is: {}".format(pes))
            print("pses is: {}".format(pses))
            # print("es is : {}".format(e))  
            # print(weat_groups[ee-1])
            
            print(  )  
        # d = {'e':e_lst,'p':p_lst}
        # pickle.dump(d,open('ceat_race_result_gptgpt2.pickle','wb'))
    