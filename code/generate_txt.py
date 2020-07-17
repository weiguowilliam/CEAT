
"""
generate text for each word group and save as txt file separately
"""

import string
import datetime
import json
import random
import pickle
import csv


# weat 1
flowers = ['aster', 'clover', 'hyacinth', 'marigold', 'poppy', 'azalea', 'crocus', 'iris', 'orchid', 'rose', 'bluebell', 'daffodil', 'lilac', 'pansy', 'tulip', 'buttercup', 'daisy', 'lily', 'peony', 'violet', 'carnation', 
'magnolia', 'petunia', 'zinnia','gladiola'] #'gladiola' deleted since it not appear
insects = ['ant', 'caterpillar', 'flea', 'locust', 'spider', 'bedbug', 'centipede', 'fly', 'maggot', 'tarantula',
'bee', 'cockroach', 'gnat', 'mosquito', 'termite', 'beetle', 'cricket', 'hornet', 'moth', 'wasp', 
'dragonfly', 'horsefly', 'roach', 'weevil','blackfly'] # 'blackfly' deleted for sysmetric since it only appears 1 time.
pleasant = ['caress', 'freedom', 'health', 'love', 'peace', 'cheer', 'friend', 'heaven', 'loyal', 'pleasure', 'diamond', 'gentle', 'honest', 
'lucky', 'rainbow', 'diploma', 'gift', 'honor', 'miracle', 'sunrise', 'family',
'happy', 'laughter', 'paradise', 'vacation']
unpleasant = ['abuse', 'crash', 'filth', 'murder', 'sickness', 'accident', 'death', 'grief', 'poison', 'stink',
'assault', 'disaster', 'hatred', 'pollute', 'tragedy', 'divorce', 'jail', 'poverty', 'ugly', 'cancer', 'kill', 'rotten',
'vomit', 'agony', 'prison']

#weat 2
instruments = ['bagpipe', 'cello', 'guitar', 'lute', 'trombone', 'banjo', 'clarinet', 'harmonica', 'mandolin',
'trumpet', 'bassoon', 'drum', 'harp', 'oboe', 'tuba', 'bell', 'fiddle', 'harpsichord', 'piano', 'viola', 'bongo',
'flute', 'horn', 'saxophone', 'violin']
weapons = ['arrow', 'club', 'gun', 'missile', 'spear', 'axe', 'dagger', 'harpoon', 'pistol', 'sword', 'blade',
'dynamite', 'hatchet', 'rifle', 'tank', 'bomb', 'firearm', 'knife', 'shotgun', 'teargas', 'cannon', 'grenade',
'mace', 'slingshot', 'whip']
pleasant, unpleasant

#weat 3
#weat 3
european_3 = ['Adam', 'Harry', 'Roger', 'Alan', 
'Ryan', 'Andrew',  'Jack', 'Matthew', 'Stephen', 'Brad', 'Greg' , 'Paul', 
'Jonathan', 'Peter',  'Amanda', 'Courtney',  'Melanie', 'Katie', 'Kristin', 'Nancy', 'Stephanie', 
'Ellen', 'Lauren', 'Colleen', 'Emily', 'Megan', 'Rachel','Betsy','Justin','Frank','Josh','Heather'] #delte random: 'Betsy','Justin','Frank','Josh','Heather'

african_3 = [ 'Alonzo',   'Theo', 'Alphonse', 'Jerome',
'Leroy',  'Torrance', 'Darnell', 'Lamar', 'Lionel', 'Tyree', 'Deion', 'Lamont', 'Malik',
'Terrence', 'Tyrone',  'Lavon', 'Marcellus',  'Wardell', 'Nichelle',
 'Ebony',  'Shaniqua',  'Jasmine',
'Tanisha', 'Tia',  'Latoya', 'Yolanda',  'Yvette','Jamel','Shereen', 'Latisha','Lakisha','Malika'] #delete 'Jamel','Shereen', 'Latisha','Lakisha','Malika',  because not appear
pleasant_3 = [ 'caress', 'freedom', 'health', 'love', 'peace', 'cheer', 'friend', 'heaven', 'loyal', 'pleasure', 
'diamond', 'gentle', 'honest', 'lucky', 'rainbow', 'diploma', 'gift', 'honor', 'miracle', 'sunrise', 'family', 'happy', 'laughter', 'paradise', 'vacation']

unpleasant_3 = ['abuse', 'crash', 'filth', 'murder', 'sickness', 'accident', 'death', 'grief', 'poison', 'stink', 'assault', 'disaster', 
'hatred', 'pollute', 'tragedy', 'bomb', 'divorce', 'jail', 'poverty', 'ugly', 'cancer', 'evil', 'kill', 'rotten', 'vomit'] 
# bomb, evil in 3 not in 1, agony prison in 1 not in 3. #pleasant 3 = pleasant 1

#weat 4
european_4 = ['Brad', 'Brendan', 'Geoffrey', 'Greg', 'Brett',  'Matthew', 
'Todd', 'Allison', 'Anne', 'Carrie', 'Emily', 'Jill', 'Laurie',  'Meredith', 'Sarah','Neil'] #delete 'Neil' sysmetric
african_4 = ['Darnell', 'Hakim', 'Jermaine', 'Kareem', 'Jamal', 'Leroy', 'Rasheed',
 'Tyrone', 'Aisha', 'Ebony', 'Keisha', 'Kenya',   'Latoya', 'Tamika',
'Tanisha','Lakisha'] #delete Lakisha because not appear
pleasant_3, unpleasant_3

#weat 5
european_4, african_4
pleasant_5 = ['joy', 'love', 'peace', 'wonderful', 'pleasure', 'friend', 'laughter', 'happy']
unpleasant_5 = ['agony', 'terrible', 'horrible', 'nasty', 'evil', 'war', 'awful', 'failure']

#weat  6
male = ['John', 'Paul', 'Mike', 'Kevin', 'Steve', 'Greg', 'Jeff', 'Bill']
female = ['Amy', 'Joan', 'Lisa', 'Sarah', 'Diana', 'Kate', 'Ann', 'Donna']
career = ['executive', 'management', 'professional', 'corporation', 'salary', 'office', 'business', 'career']
family = ['home', 'parents', 'children', 'family', 'cousins', 'marriage', 'wedding', 'relatives']

#weat 7
math = ['math', 'algebra', 'geometry', 'calculus', 'equations', 'computation', 'numbers', 'addition']
arts = ['poetry', 'art', 'dance', 'literature', 'novel', 'symphony', 'drama', 'sculpture']
male_term = ['male', 'man', 'boy', 'brother', 'he', 'him', 'his', 'son']
female_term = ['female', 'woman', 'girl', 'sister', 'she', 'her', 'hers', 'daughter']

#weat 8
science = ['science', 'technology', 'physics', 'chemistry', 'Einstein', 'NASA', 'experiment', 'astronomy']
arts_8 = ['poetry', 'art', 'Shakespeare', 'dance', 'literature', 'novel', 'symphony', 'drama']
male_term_8 = ['brother', 'father', 'uncle', 'grandfather', 'son', 'he', 'his', 'him']
female_term_8 = ['sister', 'mother', 'aunt', 'grandmother', 'daughter', 'she', 'hers', 'her']

#weat 9
mental_disease = ['sad', 'hopeless', 'gloomy', 'tearful', 'miserable', 'depressed']
physical_disease = ['sick', 'illness', 'influenza', 'disease', 'virus', 'cancer']
temporary = ['impermanent', 'unstable', 'variable', 'fleeting', 'short', 'brief', 'occasional' ]
permanent = [ 'stable', 'always', 'constant', 'persistent', 'chronic', 'prolonged', 'forever']

#weat 10
young_name = ['Tiffany', 'Michelle', 'Cindy', 'Kristy', 'Brad', 'Eric', 'Joey', 'Billy']
old_name = [ 'Ethel', 'Bernice', 'Gertrude', 'Agnes', 'Cecil', 'Wilbert', 'Mortimer', 'Edgar']
pleasant_5, unpleasant_5

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
 'Brad', 'Stephen', 'Peter', 'Josh', 'Andrew',  'Jack', 
'Matthew', 'Jonathan',  'Greg',
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

af_bias = ['loud','ghetto','unrefined','athletic','unintelligent']+['bigbutt','overweight','confident','darkskinned','promiscuous','unfeminine','aggressive','chicken']
em_bias_foraf = ['rich', 'intelligent', 'arrogant', 'status', 'blond', 'racist', 'American', 'leader', 'privileged', 'attractive', 'tall', 'sexist', 'successful']

af_unique_bias = ['bigbutt','overweight','confident','darkskinned','promiscuous','unfeminine','aggressive','chicken']
em_unique_bias_foraf = ['rich', 'tall', 'intelligent', 'arrogant', 'successful', 'status', 'blond', 'racist']

lf_bias = ['feisty','curvy', 'loud',  'cook', 'darkskinned', 'uneducated', 'hardworker' ,'promiscuous','unintelligent','short','sexy', 'maids']
em_bias_forlf = ['rich', 'intelligent', 'arrogant', 'status', 'blond', 'racist', 'American', 'leader', 'privileged',  'tall', 'sexist', 'successful']

lf_unique_bias = ['feisty','curvy','cook','promiscuous','sexy','maids']
em_unique_bias_forlf = ['rich', 'tall', 'intelligent', 'assertive', 'arrogant', 'successful']

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))

N = 10000

wd_lst = list(set(flowers+insects+pleasant+unpleasant+instruments+weapons+european_3+african_3+pleasant_3+unpleasant_3+european_4+african_4+pleasant_5+\
    unpleasant_5+male+female+career+family+math+arts+male_term+female_term+science+arts_8+male_term_8+female_term_8+mental_disease+physical_disease+\
        temporary+permanent+young_name+old_name+african_female+african_male+european_female+european_male+mexican_female+mexican_male+af_bias+em_bias_foraf+\
            af_unique_bias+em_unique_bias_foraf+lf_bias+em_bias_forlf+lf_unique_bias+em_unique_bias_forlf))

count_d = {i:0 for i in wd_lst}
sen_d = {i:[] for i in wd_lst}

for i in range(1,13):


    if i<10:
        file_path = 'RC_2014'+'-0'+str(i)
        
    else:
        file_path = 'RC_2014'+'-'+str(i)

    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    print(file_path)

    with open(file=file_path,encoding='utf-8') as f:
        for idx,line in enumerate(f):
            comment_line = json.loads(line)
            comment = comment_line["body"]
            if comment != '[deleted]' and comment != '[removed]':
                comment = comment.replace("&gt;"," ")
                comment = comment.replace("&amp;"," ")
                comment = comment.replace("&lt;"," ")
                comment = comment.replace("&quot;"," ")
                comment = comment.replace("&apos;"," ")
                comment = comment.translate(translator)
                for wd in wd_lst:
                    wwd = " "+wd+" "
                    if wwd in comment:
                        count_d[wd] += 1
                        if count_d[wd] <= N:
                            sen_d[wd].append(comment)
                        elif (count_d[wd]>N) and (random.random() < N/float(count_d[wd]+1)):
                            replace = random.randint(0,len(sen_d[wd])-1)
                            sen_d[wd][replace] = comment
            # if idx == 5:
            #     break

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
print("pickle dump")

pickle.dump(sen_d,open('sen_dic_1.pickle','wb'))
pickle.dump(count_d,open('count_dic_1.pickle','wb'))

with open('count_1.csv', 'w') as f:
    for key in count_d.keys():
        f.write("%s,%s\n"%(key,count_d[key]))

with open('count_sample_1.csv', 'w') as f:
    for key in sen_d.keys():
        f.write("%s,%s\n"%(key,len(sen_d[key])))

# """
# generate text for each word group and save as txt file separately
# """

# import string
# import datetime
# import json
# import random
# import pickle
# import csv


# # weat 1
# flowers = ['aster', 'clover', 'hyacinth', 'marigold', 'poppy', 'azalea', 'crocus', 'iris', 'orchid', 'rose', 'bluebell', 'daffodil', 'lilac', 'pansy', 'tulip', 'buttercup', 'daisy', 'lily', 'peony', 'violet', 'carnation', 
# 'magnolia', 'petunia', 'zinnia'] #'gladiola' deleted since it not appear
# insects = ['ant', 'caterpillar', 'flea', 'locust', 'spider', 'bedbug', 'centipede', 'fly', 'maggot', 'tarantula',
# 'bee', 'cockroach', 'gnat', 'mosquito', 'termite', 'beetle', 'cricket', 'hornet', 'moth', 'wasp', 
# 'dragonfly', 'horsefly', 'roach', 'weevil'] # 'blackfly' deleted for sysmetric since it only appears 1 time.
# pleasant = ['caress', 'freedom', 'health', 'love', 'peace', 'cheer', 'friend', 'heaven', 'loyal', 'pleasure', 'diamond', 'gentle', 'honest', 
# 'lucky', 'rainbow', 'diploma', 'gift', 'honor', 'miracle', 'sunrise', 'family',
# 'happy', 'laughter', 'paradise', 'vacation']
# unpleasant = ['abuse', 'crash', 'filth', 'murder', 'sickness', 'accident', 'death', 'grief', 'poison', 'stink',
# 'assault', 'disaster', 'hatred', 'pollute', 'tragedy', 'divorce', 'jail', 'poverty', 'ugly', 'cancer', 'kill', 'rotten',
# 'vomit', 'agony', 'prison']

# #weat 2
# instruments = ['bagpipe', 'cello', 'guitar', 'lute', 'trombone', 'banjo', 'clarinet', 'harmonica', 'mandolin',
# 'trumpet', 'bassoon', 'drum', 'harp', 'oboe', 'tuba', 'bell', 'fiddle', 'harpsichord', 'piano', 'viola', 'bongo',
# 'flute', 'horn', 'saxophone', 'violin']
# weapons = ['arrow', 'club', 'gun', 'missile', 'spear', 'axe', 'dagger', 'harpoon', 'pistol', 'sword', 'blade',
# 'dynamite', 'hatchet', 'rifle', 'tank', 'bomb', 'firearm', 'knife', 'shotgun', 'teargas', 'cannon', 'grenade',
# 'mace', 'slingshot', 'whip']
# pleasant, unpleasant

# #weat 3
# #weat 3
# european_3 = ['Adam', 'Harry', 'Roger', 'Alan', 
# 'Ryan', 'Andrew',  'Jack', 'Matthew', 'Stephen', 'Brad', 'Greg' , 'Paul', 
# 'Jonathan', 'Peter',  'Amanda', 'Courtney',  'Melanie', 'Katie', 'Kristin', 'Nancy', 'Stephanie', 
# 'Ellen', 'Lauren', 'Colleen', 'Emily', 'Megan', 'Rachel'] #delte random: 'Betsy','Justin','Frank','Josh','Heather'

# african_3 = [ 'Alonzo',   'Theo', 'Alphonse', 'Jerome',
# 'Leroy',  'Torrance', 'Darnell', 'Lamar', 'Lionel', 'Tyree', 'Deion', 'Lamont', 'Malik',
# 'Terrence', 'Tyrone',  'Lavon', 'Marcellus',  'Wardell', 'Nichelle',
#  'Ebony',  'Shaniqua',  'Jasmine',
# 'Tanisha', 'Tia',  'Latoya', 'Yolanda',  'Yvette'] #delete 'Jamel','Shereen', 'Latisha','Lakisha','Malika',  because not appear
# pleasant_3 = [ 'caress', 'freedom', 'health', 'love', 'peace', 'cheer', 'friend', 'heaven', 'loyal', 'pleasure', 
# 'diamond', 'gentle', 'honest', 'lucky', 'rainbow', 'diploma', 'gift', 'honor', 'miracle', 'sunrise', 'family', 'happy', 'laughter', 'paradise', 'vacation']

# unpleasant_3 = ['abuse', 'crash', 'filth', 'murder', 'sickness', 'accident', 'death', 'grief', 'poison', 'stink', 'assault', 'disaster', 
# 'hatred', 'pollute', 'tragedy', 'bomb', 'divorce', 'jail', 'poverty', 'ugly', 'cancer', 'evil', 'kill', 'rotten', 'vomit'] 
# # bomb, evil in 3 not in 1, agony prison in 1 not in 3. #pleasant 3 = pleasant 1

# #weat 4
# european_4 = ['Brad', 'Brendan', 'Geoffrey', 'Greg', 'Brett',  'Matthew', 
# 'Todd', 'Allison', 'Anne', 'Carrie', 'Emily', 'Jill', 'Laurie',  'Meredith', 'Sarah'] #delete 'Neil' sysmetric
# african_4 = ['Darnell', 'Hakim', 'Jermaine', 'Kareem', 'Jamal', 'Leroy', 'Rasheed',
#  'Tyrone', 'Aisha', 'Ebony', 'Keisha', 'Kenya',   'Latoya', 'Tamika',
# 'Tanisha' ] #delete Lakisha because not appear
# pleasant_3, unpleasant_3

# #weat 5
# european_4, african_4
# pleasant_5 = ['joy', 'love', 'peace', 'wonderful', 'pleasure', 'friend', 'laughter', 'happy']
# unpleasant_5 = ['agony', 'terrible', 'horrible', 'nasty', 'evil', 'war', 'awful', 'failure']

# #weat  6
# male = ['John', 'Paul', 'Mike', 'Kevin', 'Steve', 'Greg', 'Jeff', 'Bill']
# female = ['Amy', 'Joan', 'Lisa', 'Sarah', 'Diana', 'Kate', 'Ann', 'Donna']
# career = ['executive', 'management', 'professional', 'corporation', 'salary', 'office', 'business', 'career']
# family = ['home', 'parents', 'children', 'family', 'cousins', 'marriage', 'wedding', 'relatives']

# #weat 7
# math = ['math', 'algebra', 'geometry', 'calculus', 'equations', 'computation', 'numbers', 'addition']
# arts = ['poetry', 'art', 'dance', 'literature', 'novel', 'symphony', 'drama', 'sculpture']
# male_term = ['male', 'man', 'boy', 'brother', 'he', 'him', 'his', 'son']
# female_term = ['female', 'woman', 'girl', 'sister', 'she', 'her', 'hers', 'daughter']

# #weat 8
# science = ['science', 'technology', 'physics', 'chemistry', 'Einstein', 'NASA', 'experiment', 'astronomy']
# arts_8 = ['poetry', 'art', 'Shakespeare', 'dance', 'literature', 'novel', 'symphony', 'drama']
# male_term_8 = ['brother', 'father', 'uncle', 'grandfather', 'son', 'he', 'his', 'him']
# female_term_8 = ['sister', 'mother', 'aunt', 'grandmother', 'daughter', 'she', 'hers', 'her']

# #weat 9
# mental_disease = ['sad', 'hopeless', 'gloomy', 'tearful', 'miserable', 'depressed']
# physical_disease = ['sick', 'illness', 'influenza', 'disease', 'virus', 'cancer']
# temporary = ['impermanent', 'unstable', 'variable', 'fleeting', 'short', 'brief', 'occasional' ]
# permanent = [ 'stable', 'always', 'constant', 'persistent', 'chronic', 'prolonged', 'forever']

# #weat 10
# young_name = ['Tiffany', 'Michelle', 'Cindy', 'Kristy', 'Brad', 'Eric', 'Joey', 'Billy']
# old_name = [ 'Ethel', 'Bernice', 'Gertrude', 'Agnes', 'Cecil', 'Wilbert', 'Mortimer', 'Edgar']
# pleasant_5, unpleasant_5

# african_female = ['Yvette','Aisha','Malika','Latisha','Keisha','Tanisha',
# 'Tamika', 'Yolanda','Nichelle','Latoya','Lakisha','Shereen','Shaniqua',
# 'Jasmine','Tia'][0:12]
# # delete:  Kenya

# african_male = ['Lionel', 'Wardell',  'Jamel', 'Marcellus',
#   'Jamal', 'Leroy',  'Tyrone', 'Alphonse'
# , 'Hakim', 'Terrence', 'Jerome', 'Alonzo'][0:12]
# #delete: Deion, Ebony, Kareem,Lamar,Lavon,Malik,Rasheed,Jermaine,
# # Tyree,Lamont,Darnell,Torrance,Theo

# european_female = ['Melanie','Colleen','Ellen','Emily','Sarah','Rachel',
# 'Carrie','Stephanie','Megan','Nancy', 'Katie','Heather','Betsy',
# 'Kristin'][0:12]
# #delete: Amanda

# european_male = ['Frank',   'Roger', 'Neil', 'Geoffrey',
#  'Brad', 'Stephen', 'Peter', 'Josh', 'Andrew',  'Jack', 
# 'Matthew', 'Jonathan',  'Greg',
#   'Justin', 'Alan',    'Adam',
#     'Harry',  'Paul'][0:12]
# #delete: Lauren,Jill,Brendan,Meredith,Allison,Todd,Ryan,Courtney,Laurie,Brett,Anne

# mexican_female = ['Maria','Yesenia','Adriana','Liset','Mayra','Alma',
# 'Carolina','Iliana','Sonia',
#                     'Karina','Alejandra','Brenda','Vanessa','Diana'][0:12]
# # delete: Ana
# mexican_male = ['Jesús','Rigoberto','César','Rogelio','José','Pedro',
# 'Antonio','Alberto','Alejandro',
#                   'Alfredo','Juan','Miguel','Ricardo'][0:12]

# af_bias = ['loud','ghetto','unrefined','athletic','unintelligent']+['bigbutt','overweight','confident','darkskinned','promiscuous','unfeminine','aggressive','fried-chicken']
# em_bias_foraf = ['rich', 'intelligent', 'arrogant', 'high-status', 'blond', 'racist', 'all-American', 'leader', 'privileged', 'attractive', 'tall', 'sexist', 'successful']

# af_unique_bias = ['bigbutt','overweight','confident','darkskinned','promiscuous','unfeminine','aggressive','fried-chicken']
# em_unique_bias_foraf = ['rich', 'tall', 'intelligent', 'arrogant', 'successful', 'high-status', 'blond', 'racist']

# lf_bias = ['feisty','curvy', 'loud',  'cook', 'darkskinned', 'uneducated', 'hardworker' ,'promiscuous','unintelligent','short','sexy', 'maids']
# em_bias_forlf = ['rich', 'intelligent', 'arrogant', 'high-status', 'blond', 'racist', 'all-American', 'leader', 'privileged',  'tall', 'sexist', 'successful']

# lf_unique_bias = ['feisty','curvy','cook','promiscuous','sexy','maids']
# em_unique_bias_forlf = ['rich', 'tall', 'intelligent', 'assertive', 'arrogant', 'successful']

# now = datetime.datetime.now()
# print(now.strftime("%Y-%m-%d %H:%M:%S"))

# translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))

# N = 10000

# wd_lst = list(set(flowers+insects+pleasant+unpleasant+instruments+weapons+european_3+african_3+pleasant_3+unpleasant_3+european_4+african_4+pleasant_5+\
#     unpleasant_5+male+female+career+family+math+arts+male_term+female_term+science+arts_8+male_term_8+female_term_8+mental_disease+physical_disease+\
#         temporary+permanent+young_name+old_name+african_female+african_male+european_female+european_male+mexican_female+mexican_male+af_bias+em_bias_foraf+\
#             af_unique_bias+em_unique_bias_foraf+lf_bias+em_bias_forlf+lf_unique_bias+em_unique_bias_forlf))

# count_d = {i:0 for i in wd_lst}
# sen_d = {i:[] for i in wd_lst}

# for i in range(1,13):


#     if i<10:
#         file_path = 'RC_2014'+'-0'+str(i)
        
#     else:
#         file_path = 'RC_2014'+'-'+str(i)

#     now = datetime.datetime.now()
#     print(now.strftime("%Y-%m-%d %H:%M:%S"))
    
#     print(file_path)

#     with open(file=file_path,encoding='utf-8') as f:
#         for idx,line in enumerate(f):
#             comment_line = json.loads(line)
#             comment = comment_line["body"]
#             if comment != '[deleted]' and comment != '[removed]':
#                 comment = comment.replace("&gt;"," ")
#                 comment = comment.replace("&amp;"," ")
#                 comment = comment.replace("&lt;"," ")
#                 comment = comment.replace("&quot;"," ")
#                 comment = comment.replace("&apos;"," ")
#                 comment = comment.translate(translator)
#                 for wd in wd_lst:
#                     if wd in comment:
#                         count_d[wd] += 1
#                         if count_d[wd] <= N:
#                             sen_d[wd].append(comment)
#                         elif (count_d[wd]>N) and (random.random() < N/float(count_d[wd]+1)):
#                             replace = random.randint(0,len(sen_d[wd])-1)
#                             sen_d[wd][replace] = comment
#             if idx == 5:
#                 break

# now = datetime.datetime.now()
# print(now.strftime("%Y-%m-%d %H:%M:%S"))
# print("pickle dump")

# pickle.dump(sen_d,open('sen_dic.pickle','wb'))
# pickle.dump(count_d,open('count_dic.pickle','wb'))

# with open('count.csv', 'w') as f:
#     for key in count_d.keys():
#         f.write("%s,%s\n"%(key,count_d[key]))

# with open('count_sample.csv', 'w') as f:
#     for key in sen_d.keys():
#         f.write("%s,%s\n"%(key,len(sen_d[key])))