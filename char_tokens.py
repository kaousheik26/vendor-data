import sentencepiece as spm
from pathlib import Path
import pandas as pd

def train_spm_tokenizer(data_path, model_prefix, vocab_size=10000):
    """
    Train a SentencePiece tokenizer on bilingual data
    
    Parameters:
    data_path: Path to text file with one sentence per line
    model_prefix: Prefix for saving tokenizer model files
    vocab_size: Size of subword vocabulary
    """
    # Training parameters
    train_args = {
        'input': data_path,
        'model_prefix': model_prefix,
        'vocab_size': vocab_size,
        'character_coverage': 0.9995,  # High coverage for Hindi characters
        'model_type': 'unigram',  # Unigram model works well for mixed scripts
        'input_sentence_size': 1000000,
        'shuffle_input_sentence': True,
        'normalization_rule_name': 'identity'  # Preserve original text
    }
    
    spm.SentencePieceTrainer.train(**train_args)
    
def prepare_training_data(hindi_path, english_path, output_path):
    """
    Combine Hindi and English data into single file for tokenizer training
    """
    with open(hindi_path, 'r', encoding='utf-8') as f_hi, \
         open(english_path, 'r', encoding='utf-8') as f_en, \
         open(output_path, 'w', encoding='utf-8') as f_out:
        
        # Write both Hindi and English sentences
        for hi_line, en_line in zip(f_hi, f_en):
            f_out.write(hi_line.strip() + '\n')
            f_out.write(en_line.strip() + '\n')

def tokenize_text(sp, text):
    """
    Tokenize text using trained SentencePiece model
    """
    return ' '.join(sp.encode_as_pieces(text))

def process_parallel_data(hindi_file, english_file, tokenizer_model):
    """
    Process parallel data with subword tokenization
    """
    # Load trained tokenizer
    sp = spm.SentencePieceProcessor()
    sp.load(tokenizer_model)
    
    tokenized_data = []
    
    with open(hindi_file, 'r', encoding='utf-8') as f_hi, \
         open(english_file, 'r', encoding='utf-8') as f_en:
        
        for hi_line, en_line in zip(f_hi, f_en):
            tokenized_hi = tokenize_text(sp, hi_line.strip())
            tokenized_en = tokenize_text(sp, en_line.strip())
            tokenized_data.append({
                'hi_en': tokenized_hi,
                'cls': tokenized_en
            })
    
    return pd.DataFrame(tokenized_data)

# Example usage
if __name__ == "__main__":
    # Prepare paths
    data_dir = Path("data")
    model_prefix = data_dir / "tokenizer"
    
    # Combine data and train tokenizer
    prepare_training_data(
        data_dir / "train.hi_en",
        data_dir / "train.cls",
        data_dir / "combined.txt"
    )
    
    train_spm_tokenizer(
        str(data_dir / "combined.txt"),
        str(model_prefix)
    )
    
    # Process training data
    processed_data = process_parallel_data(
        data_dir / "train.hi_en",
        data_dir / "train.cls",
        str(model_prefix) + ".model"
    )