# Investigating Text Simplification Evaluation
Source code for the paper "Investigating Text Simplification Evaluation" by [@lmvasquezr](https://twitter.com/lmvasquezr), [@MattShardlow](https://twitter.com/MattShardlow), [Piotr Przybyła](https://home.ipipan.waw.pl/p.przybyla/) and [@SAnaniadou](https://twitter.com/SAnaniadou). Accepted in Findings at [ACL-IJCNLP 2021](https://2021.aclweb.org/program/accept/).

If you have any questions, please don't hesitate to [contact us](mailto:lvasquezcr@gmail.com?subject=[GitHub]%20Investigating%20TS%20Eval%20Question). Feel free to submit any issue/enhancement in [GitHub](https://github.com/lmvasque/ts-explore/issues) as well. 
## Features


1. Analysis of Text Simplification corpora based on simplification operations, using the edit distance measure.
1. Creation of better distributed datasets (random and with our heuristic for reduction of incorrect alignments)
1. Technical details and modifications done for performance evaluation using [EditNTS model](https://github.com/yuedongP/EditNTS). 


## Dependencies

### 1. Datasets Analysis & 2. Better-distributed datasets

You will need **Python 3.7+** and **Java** (tested on 15.0.1)

```bash
git clone https://github.com/lmvasque/ts-explore.git
cd ts-explore
pip install -r requirements.txt
```

### 3. Model Evaluation

We have adapted [EditNTS model](https://github.com/yuedongP/EditNTS) code to run in our setting. You can use this adaptation from the following fork [repo](https://github.com/lmvasque/EditNTS-eval) from original repo.
- Code migration to Python 3  
- Scripts for data preprocessing
- Other minor fixes

## Usage

### 1. Datasets Analysis 


#### Configure your datasets

Create a json file with the location of the dataset files:
```json
{
  "wikismall": {
    "test": "<data_dir>/wikismall/PWKP_108016.tag.80.aner.ori.test",
    "dev": "<data_dir>/wikismall/PWKP_108016.tag.80.aner.ori.valid",
    "train": "<data_dir>/wikismall/PWKP_108016.tag.80.aner.ori.train",
    "tag": ["src", "dst"]
  }
}
```

This is an example for **wikismall.json**, which contains subsets that start with **PWKP_108016.tag.80.aner.ori** and end with **.src** and **.dst**, located in **<data_dir>/wikismall/**

#### Run the Java Server
Edit-distance calculations occur in Java. Open a new terminal and run the following command:
```bash
cd ts-explore/java
/bin/bash run.sh
```

#### Run the analysis

In a new terminal, run from the downloaded git repo:
```bash
python ts_eval.py --analysis --datasets examples/wikismall.json --output_dir output
```

### 2. Better-distributed datasets

For creating random distributed datasets:
```bash
python ts_eval.py --create random --datasets examples/wikismall.json --seed 324 --output_dir output
```

For creating datasets reduced in poor-alignments (sentences that are aligned incorrectly):
```bash
python ts_eval.py --create unaligned --datasets examples/wikismall.json --sample 0.95 --seed 324 --output_dir output
```


### 3. Model Evaluation

We adapted the original [EditNTS model](https://github.com/yuedongP/EditNTS) and documented our changes [here](https://github.com/lmvasque/EditNTS-eval). Then, we trained our model as follows:
```bash
python main.py --vocab_path vocab_data/ --device 0 --data_path datasets/<dataset_dir>/<dataset_train_dev> --store_dir <output_dir> --batch_size 64 --lr 0.001 --vocab_size 30000 --run_training
```
To run model evaluation:
```bash
python main.py --vocab_path vocab_data/ --device 0 --data_path datasets/<dataset_dir>/<dataset_test> --store_dir output/ --load_model output/<model>/checkpoints/<checkpoints_dir> --batch_size 64 --lr 0.001 --vocab_size 30000 --run_eval
```

## Reproducibility Details

### Data
To replicate our results, please download or request the following resources:
- **WikiLarge & WikiSmall**: from [(Zhang and Lapata, 2017)](https://xingxingzhang.github.io/dress/) splits.
- **Turk Corpus**: from [(Xu, 2016)](https://github.com/cocoxu/simplification/tree/master/data/turkcorpus) splits.
- **ASSET**: from [(Alva-Manchego, 2020)](https://github.com/facebookresearch/asset) splits. In this dataset, we performed minor transformations to be consistent with other datasets, in which there are spaces between punctuation marks. This is the list of replacements applied:
  ```python
  regex = [(",", " ,"), (".", " . "), ("(", " ( "), (")", " ) ")]
  ```
- **WikiManual**: from [(Jiang, 2020)](https://github.com/chaojiang06/wiki-auto) splits. We limited our analysis to sentences labeled as "aligned", we filtered [them](https://github.com/chaojiang06/wiki-auto/tree/master/wiki-manual) as follows:
  ```bash
  grep -E  "^aligned" <file> 
  ```
- **MSD**: from [(Cao, 2020)](https://srhthu.github.io/expertise-style-transfer/#disclaimer) splits. The original dataset comes in JSON format, we filtered "text" field from each sentence. We kept every *even* line as the complex sentence and its corresponding *odd* line as its simple sentence.

### Analysis
We have created a [sample configuration file](https://github.com/lmvasque/ts-explore/examples/ts_datasets.json) to replicate our TS datasets analysis. Please use this file and update with the location of the data files. You can run the datasets analysis as follows:
```bash
python ts_eval.py --analysis --datasets examples/ts_datasets.json --output_dir output
```

You will see the following outputs:

- **Edit-distance plots** under *<output_dir>/imgs* 
- **KL divergences** between each dataset subsets, this are reported in console

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

> :memo: **Note:** For ASSET and TurkCorpus, the KL-divergences were calculated in a different way since these datasets have multiple references. In our experiments, we merged all the references into a single file for each subset (test, dev and train) and then calculated the divergences. 
- **Datasets files** (complex and simple sentences in separate files) under *<output_dir>/txt*
- Text files with **edit-distance calculations** under *<output_dir>/txt*
```text
# Edit distance calculations: Score, Complex, Simple (tab-separated)
4.3478260869565215	She performed for President Reagan in 1988's Great Performances at the White House series , which aired on the Public Broadcasting Service .	She performed for Reagan in 1988's Great Performances at the White House series , which aired on the Public Broadcasting Service .
4.545454545454546	This was demonstrated in the Miller-Urey experiment by Stanley L .  Miller and Harold C .  Urey in 1953 .	This was shown in the Miller-Urey experiment by Stanley L .  Miller and Harold C .  Urey in 1953 .
4.545454545454546	This was substantially complete when Messiaen died , and Yvonne Loriod undertook the final movement's orchestration with advice from George Benjamin .	This was mostly complete when Messiaen died , and Yvonne Loriod undertook the final movement's orchestration with advice from George Benjamin .
```

### Better-distributed datasets (Wiki Random, 98% and 95%)

Use the following command lines to reproduce our datasets.

```python
# Wikilarge Random
python ts_eval.py --create random --seed 324 --datasets examples/datasets.wikilarge.json --output_dir output

# Wikilarge 98%
python ts_eval.py --create unaligned --datasets examples/datasets.wikilarge.json --sample 0.98 --seed 324 --output_dir output

# Wikilarge 95%
python ts_eval.py --create unaligned --datasets examples/datasets.wikilarge.json --sample 0.95 --seed 324 --output_dir output

```

And *datasets.wikilarge.json* will look like this:
```json
{
  "wikilarge": {
    "test": "<data_dir>/wikilarge/wiki.full.aner.ori.test",
    "dev": "<data_dir>/wikilarge/wiki.full.aner.ori.dev",
    "train": "<data_dir>/wikilarge/wiki.full.aner.ori.train",
    "tag": ["src", "dst"]
  }
}
```
The same steps apply for WikiSmall dataset, just update the .json file.
> :memo: **Note:** The scripts above will recreate the datasets from scratch. We recommend you use this method since they fix minor limitations found in data after publication. If you still want to use the original datasets, you can download from [here](https://drive.google.com/file/d/1rT6U_bZ28NzCjzKaA-Ml4pKx39p33BVT/view?usp=sharing).

### Hardware & Runtimes
For the datasets analysis and creation, we ran under the following setting:
-  Processor Name:	2 GHz Quad-Core Intel Core i5
-  Memory:	16 GB

*Analysis duration*: for all datasets presented in this paper it should take ~5 minutes.

For the model training, we used a different setting, using 1 GPU with the following specs:
- Tesla V100-SXM2-16GB
- CUDA Driver Version = 11.2

*Model training duration:* ~3-4 hours for WikiSmall and from ~17-22 hours for WikiLarge experiments.

## Citation

If you use our results and scripts in your research, please cite our work: [Investigating Text Simplification Evaluation](https://2021.aclweb.org/program/accept/) :)
