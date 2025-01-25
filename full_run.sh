#!/usr/bin/env bash
#
# Adapted from https://github.com/facebookresearch/MIXER/blob/master/prepareData.sh


SCRIPTS=mosesdecoder/scripts
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl
LC=$SCRIPTS/tokenizer/lowercase.perl
CLEAN=$SCRIPTS/training/clean-corpus-n.perl
BPEROOT=subword-nmt/subword_nmt
BPE_TOKENS=10000
ENGLISH_WEIGHT=$1
HINDI_WEIGHT=$(($BPE_TOKENS - $ENGLISH_WEIGHT))

if [ ! -d "$SCRIPTS" ]; then
    echo "Please set SCRIPTS variable correctly to point to Moses scripts."
    exit
fi


data_dir=data
exp_dir=hi_en_$ENGLISH_WEIGHT

mkdir -p $exp_dir

cp data/dev.cls $exp_dir
cp data/eval.cls $exp_dir
cp data/eval.ns $exp_dir/eval.$exp_dir
cp data/dev.ns $exp_dir/dev.$exp_dir
cp data/train.cls $exp_dir
cp data/train.ns $exp_dir/train.$exp_dir

src=cls
tgt=$exp_dir

prep=$exp_dir/iwslt14.tokenized.$src-$tgt
mkdir -p $prep
BPE_CODE=$prep/code
BPE_CODE_HIN=$prep/code_hi
BPE_CODE_ENG=$prep/code_en
TRAIN_HI=$data_dir/train.hi
TRAIN_ENG=$data_dir/train.eng

echo "learn_bpe.py ${HINDI_WEIGHT} on ${TRAIN_HI}..."
python3 $BPEROOT/learn_bpe.py -s $HINDI_WEIGHT < $TRAIN_HI > $BPE_CODE_HIN
echo "learn_bpe.py ${ENGLISH_WEIGHT} on ${TRAIN_ENG}..."
python3 $BPEROOT/learn_bpe.py -s $ENGLISH_WEIGHT < $TRAIN_ENG > $BPE_CODE_ENG

cat $BPE_CODE_ENG <(tail -n +2 $BPE_CODE_HIN) > $BPE_CODE


for L in $src $tgt; do
    for f in train.$L dev.$L eval.$L; do
        echo "apply_bpe.py to ${f}..."
        python3 $BPEROOT/apply_bpe.py -c $BPE_CODE < $exp_dir/$f > $prep/$f
    done
done

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