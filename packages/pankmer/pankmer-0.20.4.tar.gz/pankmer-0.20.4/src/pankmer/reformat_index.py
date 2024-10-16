import time
import pandas as pd
from Bio.bgzf import BgzfWriter

def get_scores(pkr, output):
    start_time = time.time()

    with BgzfWriter(output, "wb") as f:
        for _, score_b in pkr:
            score = pkr.decode_score(score_b)
            f.write(''.join(str(int(value)) for value in score) + '\n')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Executed in {elapsed_time:.2f} seconds")


def get_kmers(pkr, output):
    start_time = time.time()

    with BgzfWriter(output, "wb") as f:
        for kmer_b, _ in pkr:
            kmer = pkr.decode_kmer_str(kmer_b)
            f.write(kmer + '\n')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Executed in {elapsed_time:.2f} seconds")


def get_unique_kmers(pkr, output):
    start_time = time.time()

    genome_names = pkr.genomes
    genome_kmers = {}

    for kmer_b, score_b in pkr:
        kmer, score = pkr.decode_kmer_str(kmer_b), pkr.decode_score(score_b)
        if score.count(True) == 1:
            for genome_index, is_present in enumerate(score):
                if is_present:
                    genome_name = genome_names[genome_index]
                    if genome_name not in genome_kmers:
                        genome_kmers[genome_name] = []
                    genome_kmers[genome_name].append(kmer)
    
    df = pd.DataFrame.from_dict(genome_kmers, orient='index').T
    df.to_csv(output, sep="\t", index=False)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Executed in {elapsed_time:.2f} seconds")