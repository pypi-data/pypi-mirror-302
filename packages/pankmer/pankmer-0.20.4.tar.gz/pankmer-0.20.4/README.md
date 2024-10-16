Please submit questions to the [Issues page on GitLab](https://gitlab.com/salk-tm/pankmer/-/issues)

Primary contact: Todd P. Michael, tmicha@salk.edu

# PanKmer

_k_-mer based and reference-free pangenome analysis. See the quickstart below, or read the [documentation](https://salk-tm.gitlab.io/pankmer/index.html).

## Repository structure

- `benchmark/` Shell scripts defining benchmarking runs
- `docs/` Source code and makefiles for Sphinx documentation
  - `source/` Documentation source code in ReStructuredText format
  - `Makefile` Sphinx infrastructure
  - `make.bat` Sphinx infrastructure
  - `pankmer-manual.pdf` User manual generated from `sphinx-build -b latexpdf`
- `example/` Files for use in README examples, can probably remove this
- `rust/` Cargo config and Rust source code
  - `src/` Rust code
  - `Cargo.toml` Cargo config
- `snakemake/` Snakemake workflows, some of these are currently outdated
- `src/pankmer/` Python source code
- `test/` Python unit tests (run with `pytest`)


## License

PanKmer is licensed under a [Salk Institute BSD license](LICENSE)

## Installation
### In a conda environment
First create an environment that includes all dependencies:
```
conda create -c conda-forge -c bioconda -n pankmer \
  python=3.10 cython gff2bed more-itertools pybedtools \
  python-newick pyfaidx rust seaborn upsetplot urllib3 \
  tabix dash-bootstrap-components
```
Then install PanKmer with `pip`:
```
conda activate pankmer
pip install pankmer
```

### With pip
PanKmer is built with [Rust](https://doc.rust-lang.org/stable/book/title-page.html),
so you will need to [install](https://doc.rust-lang.org/stable/book/ch01-01-installation.html)
it if you have not already done so. Then you can install PanKmer with `pip`:
```
pip install pankmer
```

### Check installation
Check that the installation was successful by running:
```
pankmer --version
```

## Tutorial
### Download example dataset

The `download-example` subcommand will download a small example dataset of
Chr19 sequences from _S. polyrhiza._
```
pankmer download-example -d .
```
After running this command the directory `PanKmer_example_Sp_Chr19/` will be present in the working directory. It contains FASTA files representing Chr19 from three genomes, and GFF files giving their gene annotations.
```
ls PanKmer_example_Sp_Chr19/*
```
```
PanKmer_example_Sp_Chr19/README.md

PanKmer_example_Sp_Chr19/Sp_Chr19_features:
Sp9509_oxford_v3_Chr19.gff3.gz Sp9512_a02_genes_Chr19.gff3.gz

PanKmer_example_Sp_Chr19/Sp_Chr19_genomes:
Sp7498_HiC_Chr19.fasta.gz Sp9509_oxford_v3_Chr19.fasta.gz Sp9512_a02_genome_Chr19.fasta.gz
```

To get started, navigate to the downloaded directory.
```
cd PanKmer_example_Sp_Chr19/
```

### Build a _k_-mer index

The _k_-mer index is a table tracking presence or absence of _k_-mers in the set of input genomes. To build an index, use the `index` subcommand and provide a directory containing the input genomes.

```
pankmer index -g Sp_Chr19_genomes/ -o Sp_Chr19_index.tar
```

After completion, the index will be present as a tar file `Sp_Chr19_index.tar`.
```
tar -tvf Sp_Chr19_index.tar
```
```
Sp_Chr19_index/
Sp_Chr19_index/kmers.bgz
Sp_Chr19_index/metadata.json
Sp_Chr19_index/scores.bgz
```

> #### Note
> The input genomes argument proided with the `-g` flag can be a directory, a tar archive, or a space-separated list of FASTA files.
>
> If the output argument provided with the `-o` flag ends with `.tar`, then the index will be written as a tar archive. Otherwise it will be written as a directory.


### Create an adjacency matrix

A useful application of the _k_-mer index is to generate an adjacency matrix. This is a table of _k_-mer similarity values for each pair of genomes in the index. We can generate one using the `adj-matrix` subcommand, which will produce a CSV or TSV file containing the matrix.

```
pankmer adj-matrix -i Sp_Chr19_index.tar -o Sp_Chr19_adj_matrix.csv
pankmer adj-matrix -i Sp_Chr19_index.tar -o Sp_Chr19_adj_matrix.tsv
```

> #### Note
> The input index argument proided with the `-i` flag can be tar archive or a directory.

### Plot a clustered heatmap

To visualize the adjacency matrix, we can plot a clustered heatmap of the adjacency values. In this case we use the Jaccard similarity metric for pairwise comparisons between genomes:

```
pankmer clustermap -i Sp_Chr19_adj_matrix.csv \
  -o Sp_Chr19_adj_matrix.svg \
  --metric jaccard \
  --width 6.5 \
  --height 6.5
```

![example heatmap](docs/source/_static/Sp_Chr19_adj_matrix.svg)

### Generate a gene variability heatmap

Generate a heatmap showing variability of genes across genomes. The following command uses the `--n-features` option to limit analysis to the first two genes from each input GFF3 file. The resulting image shows the level of variability observed across genes from each genome.

```
pankmer anchor-heatmap -i Sp_Chr19_index.tar \
  -a Sp_Chr19_genomes/Sp9509_oxford_v3_Chr19.fasta.gz Sp_Chr19_genomes/Sp9512_a02_genome_Chr19.fasta.gz \
  -f Sp_Chr19_features/Sp9509_oxford_v3_Chr19.gff3.gz Sp_Chr19_features/Sp9512_a02_genes_Chr19.gff3.gz \
  -o Sp_Chr19_gene_var.png \
  --n-features 2 \
  --height 3
```

![example heatmap](example/Sp_Chr19_gene_var.png)

### Pangenome datasets

The `pankmer download-example` subcommand can be used to download genomes from several publicly available pangenome datasets. See the help text:

```sh
pankmer download-example --help
```
```
usage: pankmer download-example [-h] [-d <dir/>] [-s {Spolyrhiza,Slycopersicum,Zmays,Hsapiens,Bsubtilis,Athaliana}] [-n <int>]

options:
  -h, --help            show this help message and exit
  -d <dir/>, --dir <dir/>
                        destination directory for example data
  -s {Spolyrhiza,Slycopersicum,Zmays,Hsapiens,Bsubtilis,Athaliana}, --species {Spolyrhiza,Slycopersicum,Zmays,Hsapiens,Bsubtilis,Athaliana}
                        download publicly available genomes. Species: max_samples. Spolyrhiza: 3, Slycopersicum: 46, Zmays: 54, Hsapiens: 94,    Bsubtilis: 164, Athaliana: 1135
  -n <int>, --n-samples <int>
                        number of samples to download, must be less than species max [1]
```

The `-s/--species` option selects the species, and the `-n/--n-samples` option selects the number of samples to download. The maximum number of samples for each species is:

| Species | Max samples |
| ------- | ----------- |
| _S. polyrhiza_ | 3    |
| _S. lycopersicum_ | 46 |
| _Z. mays_ | 54        |
| _H. sapiens_ | 94     |
| _B. subtilis_ | 164   |
| _A. thaliana_ | 1135  |

See below a description of each pangenome dataset

#### _S. lycopersicum_

46 *Solanum lycopersicum* genomes from the [SolOmics database](http://solomics.agis.org.cn/tomato/ftp). See also: [Nature article](https://www.nature.com/articles/s41586-022-04808-9) .

#### _Z. mays_

54 _Zea mays_ genomes from the [downloads page](https://download.maizegdb.org/) of [MaizeGDB](https://maizegdb.org/). 

#### _H. sapiens_

94 _Homo sapiens_ haplotypes from Year 1 of the [Human Pangenome Reference Consortium](https://humanpangenome.org/)/[Human Pangenome Project](https://humanpangenomeproject.org/). Download details found at the [HPRC/HPP github repository](https://github.com/human-pangenomics/HPP_Year1_Assemblies). [Nature article](https://www.nature.com/articles/s41586-022-04601-8)

#### _B. subtilis_

164 _B. subtilis_ genomes from NCBI.

#### _A. thaliana_

1135 _A. thaliana_ pseudo-genomes from the [data center](https://1001genomes.org/data/GMI-MPI/releases/v3.1/pseudogenomes/fasta/) of [1001 Genomes](https://1001genomes.org/index.html)

#### _S. polyrhiza_

A collection of 3 _Spirodela polyrhiza_ clones Sp7498, Sp9509, Sp9512, from the following sources: Sp7498 and Sp9509 sequences were sourced from the following references found at [http://spirodelagenome.org](http://spirodelagenome.org):

```
Sp9509_oxford_v3
NCBI: GCA_900492545.1
CoGe: id51364
This genome was generated with Oxford Nanopore and polished with Illumina, scaffolded against the previous Illumina-based genome Sp9509v3 and validated with BioNano optical maps and multi-color FISH (mcFISH).

Hoang PNT, Michael TP, Gilbert S, Chu P, Motley TS, Appenroth KJ, Schubert I, Lam E. Generating a high-confidence reference genome map of the Greater Duckweed by integration of cytogenomic, optical mapping and Oxford Nanopore technologies. Plant J. 2018 Jul 28.

Sp7498_HiC
CoGe: 55877
This assembly was generated using Oxford Nanopore long reads and Illumina-based HiC scaffolding.

Harkess A, McGlaughlin F, Bilkey N, Elliott K, Emenecker R, Mattoon E, Miller K, Vierstra R, Meyers BC, Michael TP. High contiguity Spirodela polyrhiza genomes reveal conserved chromosomal structure. Submitted.
```

Sp9512 sequence was sourced from research data for the following in-progress publication:

```
Pasaribu B, Acosta K, Aylward A, Abramson BW, Colt K, Hartwick NT, Liang Y, Shanklin J, Michael TP, Lam E Genomics of turions from the Greater Duckweed reveal pathways for tissue dormancy and reemergence strategy of an aquatic plant.
```

Sp9512 can be downloaded from [Michael lab AWS storage](https://salk-tm-pub.s3.us-west-2.amazonaws.com/duckweed/Sp9512.a02_final.tar).
