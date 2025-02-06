#!/bin/bash

# Input files
file1="eval-org.cls"
file2="eval-org.large"
test2="temp"
# Check if files exist
# if [[ ! -f "$file1" || ! -f "$file2" ]]; then
#     echo "Error: One or both files do not exist."
#     exit 1
# fi

src=cls
tgt=large
data_dir=large
# Read the files line by line
chmod +x prepare-test.sh
chmod +x binarize-preprocess-test.sh

python3 convert_each_lines.py $data_dir/$file1 $data_dir/$file2
./prepare-test.sh $src $tgt $data_dir $test2
./binarize-preprocess.sh $src $tgt $test2
fairseq-generate $data_dir/data-bin/iwslt14.tokenized.$test2-$data_dir/ --path $data_dir/data-bin/checkpoints/best.pt --batch-size 128 --remove-bpe --results-path $data_dir/data-bin/cls-results-$test2 --nbest 1 --beam 5


grep ^S $data_dir/data-bin/cls-results-$test2/generate-test.txt | LC_ALL=C sort -V | cut -f2- > $data_dir/data-bin/cls-results-$test2/src.txt
grep ^T $data_dir/data-bin/cls-results-$test2/generate-test.txt | LC_ALL=C sort -V | cut -f2- > $data_dir/data-bin/cls-results-$test2/ref.txt
grep ^H $data_dir/data-bin/cls-results-$test2/generate-test.txt | LC_ALL=C sort -V | cut -f3- > $data_dir/data-bin/cls-results-$test2/hyp.txt
# paste "$file1" "$file2" | while IFS=$'\t' read -r line1 line2
# do
#     # Pass each line to the Python script
#     rm -rf $data_dir/data-bin/iwslt14.tokenized.$test2-$data_dir/
#     rm -rf $data_dir/data-bin/cls-results-$test2
#     python3 convert_each_lines.py "$line1" "$line2"
#     test2=tmp
#     ./prepare-test.sh $src $tgt $data_dir $test2
#     ./binarize-preprocess-test.sh $src $tgt $test2
#     fairseq-generate $data_dir/data-bin/iwslt14.tokenized.$test2-$data_dir/ --path $data_dir/data-bin/checkpoints/best.pt --batch-size 128 --remove-bpe --results-path $data_dir/data-bin/cls-results-$test2 --nbest 1 --beam 5
#     grep -E '^T' $data_dir/data-bin/cls-results-$test2/generate-test.txt | cut -d$'\t' -f2 > $data_dir/data-bin/cls-results-$test2/ref
#     grep -E '^H' $data_dir/data-bin/cls-results-$test2/generate-test.txt | cut -d$'\t' -f3 > $data_dir/data-bin/cls-results-$test2/hyp
#     paste -s -d ' ' $data_dir/data-bin/cls-results-$test2/ref > $data_dir/data-bin/tmp_ref
#     paste -s -d ' ' $data_dir/data-bin/cls-results-$test2/hyp > $data_dir/data-bin/tmp_hyp
#     cat $data_dir/data-bin/tmp_ref >> $data_dir/data-bin/ref_final
#     cat $data_dir/data-bin/tmp_hyp >> $data_dir/data-bin/hyp_final
# done