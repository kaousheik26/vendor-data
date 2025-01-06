#!/usr/bin/env bash

src=cls
tgt=cs

TEXT=iwslt14.tokenized.$src-$tgt
fairseq-preprocess --source-lang $src --target-lang $tgt \
    --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test \
    --destdir data-bin/iwslt14.tokenized.de-en \
    --workers 20