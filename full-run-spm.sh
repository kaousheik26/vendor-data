#!/usr/bin/env bash
# 1. Train SentencePiece (using cls input data)
cat raw_data/train.cls raw_data/train.ns > raw_data/combined.txt

spm_train \
    --input raw_data/combined.txt \
    --model_prefix processed_data/spm \
    --vocab_size 10000 \
    --character_coverage 0.9995 \
    --model_type unigram \
    --input_sentence_size 1000000 \
    --shuffle_input_sentence true

# 2. Apply tokenization (notice the changed extensions)
spm_encode --model=processed_data/spm.model < raw_data/train.cls > processed_data/train.cls-ns.cls
spm_encode --model=processed_data/spm.model < raw_data/train.ns > processed_data/train.cls-ns.ns

spm_encode --model=processed_data/spm.model < raw_data/valid.cls > processed_data/valid.cls-ns.cls
spm_encode --model=processed_data/spm.model < raw_data/valid.ns > processed_data/valid.cls-ns.ns

spm_encode --model=processed_data/spm.model < raw_data/test.cls > processed_data/test.cls-ns.cls
spm_encode --model=processed_data/spm.model < raw_data/test.ns > processed_data/test.cls-ns.ns

# 3. Preprocess (changed source-lang and target-lang)
fairseq-preprocess \
    --source-lang cls --target-lang ns \
    --trainpref processed_data/train.cls-ns \
    --validpref processed_data/valid.cls-ns \
    --testpref processed_data/test.cls-ns \
    --destdir data-bin \
    --workers 20 \
    --joined-dictionary

# 4. Train (similar command but with cls-ns instead of hi-en)
fairseq-train \
    data-bin \
    --arch transformer \
    --share-decoder-input-output-embed \
    --optimizer adam \
    --adam-betas '(0.9, 0.98)' \
    --clip-norm 0.0 \
    --lr 5e-4 \
    --lr-scheduler inverse_sqrt \
    --warmup-updates 4000 \
    --dropout 0.3 \
    --weight-decay 0.0001 \
    --criterion label_smoothed_cross_entropy \
    --label-smoothing 0.1 \
    --max-tokens 4096 \
    --eval-bleu \
    --eval-bleu-args '{"beam": 5, "max_len_a": 1.2, "max_len_b": 10}' \
    --eval-bleu-detok moses \
    --eval-bleu-remove-bpe sentencepiece \
    --eval-bleu-print-samples \
    --best-checkpoint-metric bleu \
    --maximize-best-checkpoint-metric \
    --save-dir checkpoints \
    --max-epoch 40 \
    --save-interval 10 \
    --validate-interval 1