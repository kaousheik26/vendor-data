#!/bin/bash
src=$1
tgt=$2
data_dir=$3
test2=$4
chmod +x prepare-test.sh
chmod +x binarize-preprocess-test.sh
./prepare-test.sh $src $tgt $data_dir $test2
./binarize-preprocess-test.sh $src $tgt $test2


fairseq-generate $data_dir/data-bin/iwslt14.tokenized.$test2-$data_dir/ --path $data_dir/data-bin/checkpoints/checkpoint_best.pt --batch-size 128 --remove-bpe --results-path $data_dir/data-bin/cls-results-$test2 --nbest 1 --beam 5

grep -E '^T' $data_dir/data-bin/cls-results-$test2/generate-test.txt | cut -d$'\t' -f2 > $data_dir/data-bin/cls-results-$test2/ref
grep -E '^H' $data_dir/data-bin/cls-results-$test2/generate-test.txt | cut -d$'\t' -f3 > $data_dir/data-bin/cls-results-$test2/hyp
python3 wer.py $data_dir/data-bin/cls-results-$test2/
