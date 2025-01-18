#!/usr/bin/env bash

src=cls
tgt=combine

TEXT=$tgt/iwslt14.tokenized.$src-$tgt
fairseq-preprocess --source-lang $src --target-lang $tgt \
    --trainpref $TEXT/train --validpref $TEXT/dev --testpref $TEXT/eval \
    --destdir $tgt/data-bin/iwslt14.tokenized.$tgt \
    --workers 20