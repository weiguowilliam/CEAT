# Contextualized Word Embeddings Contain Emergent Intersectional Biases in a Contextualized Distribution of Human-like Bias Scores

This repository is the official implementation of [Contextualized Word Embeddings Contain Emergent Intersectional Biases in a Contextualized Distribution of Human-like Bias Scores](https://arxiv.org/). 

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

We listed the details of Word Embedding Association Test and the words we used in validation of CEAT, IBD and UIBD in supp.pdf.


## Dataset
[Reddit Comment Dataset 2014](https://files.pushshift.io/reddit/comments/) is used. Here's the link of raw json comment files.

After downloading all comment json file, you can use the python file we provide.

```
python generate_txt.py
```

It extract the comment, clean the raw text and save it as a pickle file.

Besides the raw json files provided by the link, we can also use [Google BigQuery](https://cloud.google.com/bigquery) to inquiry the needed comments. Here's a sample big query script to select 10 comments in 2014.

```{sql}
select * from `fh-bigquery.reddit_comments.20014` limit 10
```

After you download the comments, the comments files should be stored as pickle file in dictionary. The keys are the target and attribute words. The values are lists. Each list contains comments that contain the key word.





## Generate Contextualized Word Embeddings

Please set the file path as you needed before running the scripts.

In this step we generate contextualized word embeddings and store it in pickle files. 

Each pickle file is a dictionary whose keys are the words in tests and values are a list whose items are 300-d contextualized word embeddings.

The generated contextualized word embeddings files is named as weat{test_number}_{model_name}.pickle

```
python generate_ebd_{model_name}.py
```

There're four models we used: Bert, GPT, GPT2 and elmo. You will find four files in code folder.

## Contextualized Embedding Association Test (CEAT)

Run the script to generate effect size, p value for N=10000 (by default) time of sampling.

For CEAT(C11~C10):

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



