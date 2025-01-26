#!/usr/bin/env bash
#
# Adapted from https://github.com/facebookresearch/MIXER/blob/master/prepareData.sh


SCRIPTS=mosesdecoder/scripts
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl
LC=$SCRIPTS/tokenizer/lowercase.perl
CLEAN=$SCRIPTS/training/clean-corpus-n.perl
BPEROOT=subword-nmt/subword_nmt
BPE_TOKENS=$1

if [ ! -d "$SCRIPTS" ]; then
    echo "Please set SCRIPTS variable correctly to point to Moses scripts."
    exit
fi


data_dir=$3
exp_dir=$BPE_TOKENS

mkdir -p $exp_dir

cp $data_dir/dev.cls $exp_dir
cp $data_dir/eval.cls $exp_dir
cp $data_dir/eval.ns $exp_dir/eval.$exp_dir
cp $data_dir/dev.ns $exp_dir/dev.$exp_dir
cp $data_dir/train.cls $exp_dir
cp $data_dir/train.ns $exp_dir/train.$exp_dir

src=cls
tgt=$exp_dir

prep=$exp_dir/iwslt14.tokenized.$src-$tgt
mkdir -p $prep
BPE_CODE=$prep/code

$TRAIN=$exp_dir/train
cat $exp_dir/train.cls $exp_dir/train.$exp_dir >> $exp_dir/train
python3 $BPEROOT/learn_bpe.py -s $BPE_TOKENS < $TRAIN > $BPE_CODE

for L in $src $tgt; do
    for f in train.$L dev.$L eval.$L; do
        echo "apply_bpe.py to ${f}..."
        python3 $BPEROOT/apply_bpe.py -c $BPE_CODE < $exp_dir/$f > $prep/$f
    done
done
rm -rf $tmp
echo "Binarizing"

TEXT=$prep
fairseq-preprocess --source-lang $src --target-lang $tgt \
    --trainpref $TEXT/train --validpref $TEXT/dev --testpref $TEXT/eval \
    --destdir $tgt/data-bin/iwslt14.tokenized.$tgt \
    --workers 20

CUDA_VISIBLE_DEVICES=$2 fairseq-train $tgt/data-bin/iwslt14.tokenized.$tgt  \
   --arch transformer_iwslt_de_en \
   --share-decoder-input-output-embed  \
   --optimizer adam --adam-betas '(0.9, 0.98)' \
   --clip-norm 0.0     \
   --lr 5e-4 --lr-scheduler inverse_sqrt \
   --warmup-updates 4000     \
   --dropout 0.3 \
   --weight-decay 0.0001     \
   --criterion label_smoothed_cross_entropy \
   --label-smoothing 0.1     \
   --max-tokens 4096     \
   --eval-bleu     \
   --eval-bleu-args '{"beam": 5, "max_len_a": 1.2, "max_len_b": 10}'     \
   --eval-bleu-detok moses     \
   --eval-bleu-remove-bpe     \
   --eval-bleu-print-samples     \
   --best-checkpoint-metric bleu \
   --maximize-best-checkpoint-metric \
   --save-dir $tgt/data-bin/checkpoints \
   --max-epoch 40 \
   --save-interval 10

echo "Generating"

fairseq-generate $tgt/data-bin/iwslt14.tokenized.$tgt \
    --path $tgt/data-bin/checkpoints/checkpoint_best.pt \
    --batch-size 128  \
    --remove-bpe \
    --results-path $tgt/data-bin/cls-results \
    --nbest 1 --beam 5

grep -E '^T' $tgt/data-bin/cls-results/generate-test.txt | cut -d$'\t' -f2 > $tgt/data-bin/cls-results/ref
grep -E '^H' $tgt/data-bin/cls-results/generate-test.txt | cut -d$'\t' -f3 > $tgt/data-bin/cls-results/hyp
python3 wer.py $tgt/data-bin/cls-results/