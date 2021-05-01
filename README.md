# Contextualized Word Embeddings Contain Emergent Intersectional Biases in a Contextualized Distribution of Human-like Bias Scores

This repository is the official implementation of [Contextualized Word Embeddings Contain Emergent Intersectional Biases in a Contextualized Distribution of Human-like Bias Scores](https://arxiv.org/abs/2006.03955). 

## Requirements

To set up an environment for the project

```
conda create --name ceat
conda activate ceat
```

To install requirements:

```setup
pip install -r requirements.txt
```

## Supplemental material

We listed the details of Word Embedding Association Test and the words we used in validation of CEAT, IBD and UIBD as `supp.pdf` in this codebase.


## Dataset
[Reddit Comment Dataset 2014](https://files.pushshift.io/reddit/comments/) is used. Here's the link of raw json comment files.

Since the raw dataset is too huge for storage, we provide a pickle file that contains the sentences for our experiment from this huge raw dataset. The link of this data file is in `data.md` file. The pickle file contains a big dictionary file. The dictionary contains all the sentences we need for CEAT.

After downloading all comment json file, you can use the python file we provide.

```
import pickle

dataset = pickle.load(open('file','rb'))

```


If you prefer to download the raw data yourself, we also provide a code file to process the raw data.

```
python generate_txt.py
```

It extract the comment, clean the raw text and save it as a pickle file.

Besides the raw json files provided by the link.

Another way is to test with a small sample set. For this task, we can use [Google BigQuery](https://cloud.google.com/bigquery) to inquiry the needed comments. Here's a sample big query script to select 10 comments in 2014.

```{sql}
select * from `fh-bigquery.reddit_comments.20014` limit 10
```

After you download the comments, the comments files should be stored as pickle file in dictionary. The keys are the target and attribute words. The values are lists. Each list contains comments that contain the key word.





## Generate Contextualized Word Embeddings

Please set the file path as you needed before running the scripts.

In this step we generate contextualized word embeddings and store it in pickle files. 

Each pickle file is a dictionary whose keys are the words in tests and values are a list whose items are 300-d contextualized word embeddings.

The generated contextualized word embeddings files should be named as weat{test_number}_{model_name}.pickle

```
python generate_ebd_{model_name}.py
```

There're four models we used: Bert, GPT, GPT2 and elmo. You will find four files in code folder.

## Contextualized Embedding Association Test (CEAT)

Run the script to generate effect size, p value for N=10000 (by default) time of sampling.

For CEAT(C1~C10):

```
python ceat.py
```


Effect sizes, p values of each test are stored as list in seperate pickle files. 
The pickle file is named as: {model_name}_weat{test_number}_pvalue.pickle, {model_name}_weat{test_number}_effectsize.pickle

The returned values are Combined Effect Size (CES), P value of each test. 

Users can use matplotlib library to draw the distribution based on sampling effect sizes and p values.

## Intersectional Bias Detection (IBD)

To detect intersectional biases of African American females (AF) and Latino American females (LF)

```
python ibd.py
```



