import sentencepiece as spm

# 1. Train the SentencePiece model
spm.SentencePieceTrainer.train(
    input='raw_data/combined.txt',
    model_prefix='processed_data/spm',
    vocab_size=10000,
    character_coverage=0.9995,
    model_type='unigram',
    input_sentence_size=1000000,
    shuffle_input_sentence=True
)

# 2. Apply tokenization using the trained model
def encode_file(input_file, output_file, model_file):
    # Load the SentencePiece model
    sp = spm.SentencePieceProcessor(model_file=model_file)
    
    # Read input file and encode sentences
    with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            # Encode the line and write to the output file
            encoded_line = sp.encode(line.strip(), out_type=str)  # `out_type=str` gives tokens as strings
            fout.write(' '.join(encoded_line) + '\n')

# File paths
model_file = 'processed_data/spm.model'

# Encode training data
encode_file('raw_data/train.cls', 'processed_data/train.cls-ns.cls', model_file)
encode_file('raw_data/train.ns', 'processed_data/train.cls-ns.ns', model_file)

# Encode validation data
encode_file('raw_data/valid.cls', 'processed_data/valid.cls-ns.cls', model_file)
encode_file('raw_data/valid.ns', 'processed_data/valid.cls-ns.ns', model_file)

# Encode test data
encode_file('raw_data/test.cls', 'processed_data/test.cls-ns.cls', model_file)
encode_file('raw_data/test.ns', 'processed_data/test.cls-ns.ns', model_file)
