use std::io::{Read, BufReader, ErrorKind};
use std::path::PathBuf;
use pyo3::prelude::*;
use ndarray::s;
use niffler;
use crate::{Score, PKMeta, PKGenomes};
use crate::metadata::load_metadata;
use crate::helpers::decode_score;
use tar::Archive;
use crate::parse_kmers_scores::parse_scores;
use rustc_hash::FxHashMap as HashMap;


#[pyfunction]
pub fn get_adjacency_matrix(idx_dir: &str, tar_file: &str,
) -> PyResult<(Vec<Vec<usize>>, PKGenomes)> {
    let meta: PKMeta = load_metadata(idx_dir, tar_file)?;
    let n_genomes: usize = meta.genomes.len();
    let score_counts = match tar_file.len() > 0 {
        true => get_adj_tar(tar_file, n_genomes),
        false => get_adj_no_tar(idx_dir, n_genomes)
    };
    let mut genomes: PKGenomes = Vec::new();
    for i in 0..n_genomes {
        let genome = meta.genomes.get(&i).expect("could not get genome name");
        genomes.push(genome.to_string());
    }
    Ok((score_counts, genomes))
}


fn get_adj_no_tar(idx_dir: &str, n_genomes: usize) -> Vec<Vec<usize>> {
    let batch_size = 100_000_000;

    let mut score_counts = vec![vec![0_usize; n_genomes]; n_genomes];
    let score_bytes: usize = (n_genomes + 7) / 8;
    let score_bufsize: usize = 1000 * score_bytes;
    let mut score_buf = vec![0; score_bytes];
    let mut scores_in_path: PathBuf = PathBuf::from(&idx_dir);
    scores_in_path.push("scores.bgz");
    
    let (scores_reader, _format) = niffler::from_path(&scores_in_path).expect("File not found");
    let mut scores_in = BufReader::with_capacity(score_bufsize, scores_reader);

    loop {
        let mut batch_score_counts = HashMap::default();
        for _ in 0..batch_size {

            let scores = match scores_in.read_exact(&mut score_buf) {
                Ok(_) => parse_scores(&score_buf, score_bytes),
                Err(ref e) if e.kind() == ErrorKind::UnexpectedEof => break,
                // Err(ref e) if e.kind() == ErrorKind::Interrupted => continue,
                Err(e) => panic!("{:?}", e),
            };
            for score in scores.iter() {
                *batch_score_counts.entry(score.to_owned()).or_default() += 1;
            }
        }
        if batch_score_counts.is_empty() {
            break;
        }

        for (score, count) in &batch_score_counts {
            match decode_score(score, n_genomes) {
                Ok(decoded) => {
                    for i in 0..n_genomes {
                        for j in 0..n_genomes {
                            // If both i-th and j-th positions are `true`, update score_counts
                            if decoded[i] && decoded[j] {
                                score_counts[i][j] += count;
                            }
                        }
                    }
                },
                Err(e) => eprintln!("failed to decode score: {:?}", e),
            }
        }
    }
    score_counts
}


fn get_adj_tar(tar_file: &str, n_genomes: usize) -> Vec<Vec<usize>> {
    let batch_size = 100_000_000;

    let mut score_counts = vec![vec![0_usize; n_genomes]; n_genomes];
    let score_bytes: usize = (n_genomes + 7) / 8;
    let score_bufsize: usize = 1000 * score_bytes;
    let mut score_buf = vec![0; score_bytes];
    let (tar, _format) = niffler::from_path(tar_file).expect(&format!("File not found: {}", tar_file));

    for entry in Archive::new(tar).entries().expect("Can't read tar file") {
        let s = entry.expect("Error reading tar archive");
        let s_in_path = s.path().expect("Error reading tar archive");
        let s_in_str = s_in_path.to_str().unwrap().to_owned();

        if s_in_str.ends_with("scores.bgz") {
            let (scores_reader, _format) = niffler::get_reader(Box::new(s)).expect("Can't read from tar archive");
            let mut scores_in = BufReader::with_capacity(score_bufsize, scores_reader);

            loop {
                let mut batch_score_counts = HashMap::default();
                for _ in 0..batch_size {
        
                    let scores = match scores_in.read_exact(&mut score_buf) {
                        Ok(_) => parse_scores(&score_buf, score_bytes),
                        Err(ref e) if e.kind() == ErrorKind::UnexpectedEof => break,
                        // Err(ref e) if e.kind() == ErrorKind::Interrupted => continue,
                        Err(e) => panic!("{:?}", e),
                    };
                    for score in scores.iter() {
                        *batch_score_counts.entry(score.to_owned()).or_default() += 1;
                    }
                }
                if batch_score_counts.is_empty() {
                    break;
                }
        
                for (score, count) in &batch_score_counts {
                    match decode_score(score, n_genomes) {
                        Ok(decoded) => {
                            for i in 0..n_genomes {
                                for j in 0..n_genomes {
                                    // If both i-th and j-th positions are `true`, update score_counts
                                    if decoded[i] && decoded[j] {
                                        score_counts[i][j] += count;
                                    }
                                }
                            }
                        },
                        Err(e) => eprintln!("failed to decode score: {:?}", e),
                    }
                }
            }
        }
    }
    score_counts
}

