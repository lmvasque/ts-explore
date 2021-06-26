# Investigating Text Simplification Evaluation
Source code for the paper "Investigating Text Simplification Evaluation" by [@lmvasquezr](https://twitter.com/lmvasquezr), [@MattShardlow](https://twitter.com/MattShardlow), [Piotr Przybyła](https://home.ipipan.waw.pl/p.przybyla/) and [@SAnaniadou](https://twitter.com/SAnaniadou). Accepted in Findings at ACL-IJCNLP 2021.

If you have any question, please don't hesitate to [contact us](mailto:lvasquezcr@gmail.com). Also, feel free to submit any issue/enhancement at [GitHub](https://github.com/lmvasque/ts-explore/issues), if needed. 
## Features


1. Analysis of Text Simplification corpora based on simplification operations, using the edit distance measure.
1. Creation of better distributed datasets (random and with our heuristic for reduction of incorrect alignments)
1. Technical details and modifications done for performance evaluation using [EditNTS model](https://github.com/yuedongP/EditNTS). 


## Dependencies

### 1. Datasets Analysis & 2. Better-distributed datasets

We use Python 3 and Java (we are using java 15.0.1)

```bash
pip install -r requirements.txt
```

### 3. Model Evaluation

We have adapted [EditNTS model](https://github.com/yuedongP/EditNTS) code to run in our setting. You can use this adaptation from the following fork [repo](https://github.com/lmvasque/EditNTS-eval) of the original repo. These modifications include:
- Code migration to Python 3  
- Scripts for data preprocessing
- Other minor fixes

## Usage

### 1. Datasets Analysis 


#### Configure your datasets

Create a json file with the location of the dataset files (with prefixes for test, dev and train subsets) and its suffixes:
```json
{
   "turkcorpus": {
    "test": "data/turkcorpus/turkcorpus.test",
    "dev": "data/turkcorpus/turkcorpus.tune",
    "tag": ["orig.all", "simp.all"]
  },
   "asset": {
    "test": "data/asset/asset.test",
    "dev": "data/asset/asset.valid",
    "tag": ["orig.all", "simp.all"]
  }
}
```

This is an example for **data.json**, which contains subsets called: **asset.test.orig.all** located in **data/turkcorpus/**

#### Run the Java Server
Edit-distance calculations occur in Java. Open a new terminal and run the following command:
```bash
cd ts-explore/java
./run.sh
```

#### Run the analysis 
```bash
./ts_eval --analysis --datasets ../examples/datasets.json --output_dir "../output"
```

### 2. Better-distributed datasets

For creating random distributed datasets:
```bash
./ts_eval --create random --sample 0.05 --output_dir "../output"
```

For creating datasets reduced in poor-alignments (sentences that are aligned incorrectly):
```bash
./ts_eval --create unaligned --sample 0.05 --output_dir "../output"
```


### 3. Model Evaluation

We created the following adaptation of EditNTS model: https://github.com/lmvasque/EditNTS-eval. We trained our model using the following command:
```bash
python main.py --vocab_path vocab_data/ --device 0 --data_path datasets/<dataset_dir>/<dataset_train_dev> --store_dir <output_dir> --batch_size 64 --lr 0.001 --vocab_size 30000 --run_training
```
And.. to run model evaluation:
```bash
python main.py --vocab_path vocab_data/ --device 0 --data_path datasets/<dataset_dir>/<dataset_test> --store_dir output/ --load_model output/<model>/checkpoints/<checkpoints_dir> --batch_size 64 --lr 0.001 --vocab_size 30000 --run_eval
```

## Reproducibility 

### Data
To replicate our results, please get the following resources:
- **WikiLarge & WikiSmall**: from [(Zhang and Lapata, 2017)](https://xingxingzhang.github.io/dress/) splits.
- **Turk Corpus**: from [(Xu, 2016)](https://github.com/cocoxu/simplification/tree/master/data/turkcorpus) splits.
- **ASSET**: from [(Alva-Manchego, 2020)](https://github.com/facebookresearch/asset) splits. In this dataset, we performed minor transformations to be consistent with other datasets, in which there are spaces between punctuation marks. This is the list of replacements applied:
  ```python
  regex = [(",", " ,"), (".", " . "), ("(", " ( "), (")", " ) ")]
  ```
- **WikiManual**: from [(Jiang, 2020)](https://github.com/chaojiang06/wiki-auto) splits. We limited our analysis to sentences labeled as "aligned", we filtered them as follows:
  ```bash
  grep -E  "^aligned" <file> 
  ```
- **MSD**: from [(Cao, 2020)](https://srhthu.github.io/expertise-style-transfer/#disclaimer) splits. The original dataset comes in JSON format, we filtered "text" field from each sentence. We kept every *even* line as the complex sentence and its corresponding *odd* line as its simple sentence.

### Analysis
We have created a sample configuration file to replicate the datasets analysis. Please refer to this file and update with the location of the data files. Then, run the datasets analysis:
```bash
./ts_eval --analysis --datasets ../examples/datasets.json --output_dir "../output"
```

You will the following output:

- **Edit-distance plots** under <your_output_dir>/imgs 
- **KL divergences** reported in the log

```bash
Distribution divergences between Test/Dev subsets
   Dataset    Value
wikimanual 0.102053
 wikilarge 0.462257
 wikismall 0.069603

Distribution divergences between Test/Train subsets
   Dataset    Value
wikimanual 0.017596
 wikilarge 0.463852
 wikismall 0.057977

```
**Note:** For ASSET and TurkCorpus, the KL-divergences were calculated with a different procedure since these datasets have multiple references.
- Datasets files (complex and simple sentences in separate files) under <your_output_dir>/txt
- Text files with edit-distance calculations under <your_output_dir>/txt
```text
# Edit distance calculations: Score, Complex, Simple (tab-separated)
4.3478260869565215	She performed for President Reagan in 1988's Great Performances at the White House series , which aired on the Public Broadcasting Service .	She performed for Reagan in 1988's Great Performances at the White House series , which aired on the Public Broadcasting Service .
4.545454545454546	This was demonstrated in the Miller-Urey experiment by Stanley L .  Miller and Harold C .  Urey in 1953 .	This was shown in the Miller-Urey experiment by Stanley L .  Miller and Harold C .  Urey in 1953 .
4.545454545454546	This was substantially complete when Messiaen died , and Yvonne Loriod undertook the final movement's orchestration with advice from George Benjamin .	This was mostly complete when Messiaen died , and Yvonne Loriod undertook the final movement's orchestration with advice from George Benjamin .
```

### Hardware & Runtimes
For the datasets analysis and creation, we ran under the following setting:
-  Processor Name:	2 GHz Quad-Core Intel Core i5
-  Memory:	16 GB

*Analysis duration*: for all datasets should take ~5 minutes.

For the model training, we used a different setting, using 1 GPU with the following specs:
- Tesla V100-SXM2-16GB
- CUDA Driver Version = 11.2

*Model training duration:* ~3-4 hours for WikiSmall and from ~17-22 hours for WikiLarge experiments.

## Citation

If you use our results and scripts in your research, please cite our work: Investigating Text Simplification Evaluation :)

```
@inproceedings{vasquez-rodriguez-etal-2021,
    title = "{Investigating Text Simplification Evaluation",
    author = "",
    booktitle = "",
    month = ,
    year = "",
    address = "",
    publisher = "",
    url = "",
    pages = ""
}
```
