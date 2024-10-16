import re
import json
from collections import Counter, defaultdict
from multiprocessing import Pool
import numpy as np

class Tokenize2:
    def __init__(self, vocab_size, merge_strategy="bpe", encoding="utf-8", special_tokens=None, oov_strategy="split"):
        """
        Initialize the Tokenize2 tokenizer with advanced options.

        Args:
            vocab_size (int): The maximum vocabulary size.
            merge_strategy (str): The token merging strategy ('bpe', 'frequency', 'entropy', 'context').
            encoding (str): The character encoding scheme ('utf-8', 'utf-16', etc.).
            special_tokens (list, optional): List of special tokens like <PAD>, <UNK>, etc.
            oov_strategy (str): The strategy for handling out-of-vocabulary tokens ('split', 'approximation').
        """
        self.vocab_size = vocab_size
        self.vocab = {}
        self.merges = []
        self.byte_encoder = self.build_byte_encoder(encoding)
        self.byte_decoder = {v: k for k, v in self.byte_encoder.items()}
        self.special_tokens = special_tokens or ['<PAD>', '<UNK>']
        self.merge_strategy = merge_strategy
        self.oov_strategy = oov_strategy
        self.init_special_tokens()

    def init_special_tokens(self):
        """Initialize special tokens in the vocabulary."""
        for token in self.special_tokens:
            self.vocab[token] = len(self.vocab)

    def build_byte_encoder(self, encoding):
        """Creates byte to unicode mapping based on the chosen encoding scheme."""
        byte_encoder = {}
        if encoding == "utf-8":
            for i in range(256):
                byte_encoder[i] = chr(i)
        elif encoding == "utf-16":
            for i in range(65536):
                byte_encoder[i] = chr(i)
        return byte_encoder

    def bytes_to_unicode(self, text):
        """Encodes text into byte-level."""
        return ''.join(self.byte_encoder[byte] if byte in self.byte_encoder else chr(byte) for byte in text)

    def pre_tokenize(self, text):
        """Pre-tokenize text into byte-level representations."""
        text = re.sub(r'\s+', ' ', text.strip())  # Normalize spaces
        return [self.bytes_to_unicode(text.encode('utf-8'))]  # Byte-encode

    def train_tokenizer(self, corpus):
        """
        Train the tokenizer using a corpus of text.
        Args:
            corpus (list): A list of strings representing the training corpus.
        """
        # Pre-tokenize the corpus into byte-level tokens
        tokenized_corpus = [self.pre_tokenize(text) for text in corpus]

        # Build an initial vocabulary of byte-level tokens
        vocab = Counter()
        for tokens in tokenized_corpus:
            for token in tokens:
                token = ' '.join(token)
                vocab[token] += 1

        # Choose the merging strategy
        self.choose_merging_strategy(vocab)

    def choose_merging_strategy(self, vocab):
        """Choose the merging strategy based on user configuration."""
        if self.merge_strategy == "bpe":
            self.learn_bpe(vocab)
        elif self.merge_strategy == "frequency":
            self.learn_frequency_based_merging(vocab)
        elif self.merge_strategy == "entropy":
            self.learn_entropy_based_merging(vocab)
        elif self.merge_strategy == "context":
            self.learn_context_based_merging(vocab)
        else:
            raise ValueError(f"Unknown merge strategy: {self.merge_strategy}")

    def learn_bpe(self, vocab):
        """Learn Byte-Pair Encoding (BPE) merges."""
        while len(self.vocab) < self.vocab_size:
            pairs = self.get_stats(vocab)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            vocab = self.merge_vocab(best, vocab)
            self.merges.append(best)

    def learn_frequency_based_merging(self, vocab):
        """Learn token merging based on frequency."""
        while len(self.vocab) < self.vocab_size:
            pairs = self.get_stats(vocab)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            vocab = self.merge_vocab(best, vocab)
            self.merges.append(best)

    def learn_entropy_based_merging(self, vocab):
        """Learn token merging based on token entropy."""
        def entropy(freqs):
            total = sum(freqs)
            return -sum((f / total) * np.log2(f / total) for f in freqs if f > 0)
        
        while len(self.vocab) < self.vocab_size:
            pairs = self.get_stats(vocab)
            entropies = {pair: entropy([vocab[word] for word in vocab if pair[0] in word or pair[1] in word]) for pair in pairs}
            best = min(entropies, key=entropies.get)  # Minimize entropy
            vocab = self.merge_vocab(best, vocab)
            self.merges.append(best)

    def learn_context_based_merging(self, vocab):
        """Learn token merging based on context (advanced)."""
        # To implement, we would need a model that considers word context dynamically.
        pass

    def get_stats(self, vocab):
        """Get frequency of symbol pairs."""
        pairs = defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[(symbols[i], symbols[i + 1])] += freq
        return pairs

    def merge_vocab(self, pair, vocab):
        """Merge frequent symbol pairs."""
        new_vocab = {}
        bigram = ' '.join(pair)
        pattern = re.compile(r'(?<!\S)' + re.escape(bigram) + r'(?!\S)')
        for word in vocab:
            new_word = pattern.sub(''.join(pair), word)
            new_vocab[new_word] = vocab[word]
        return new_vocab

    def handle_oov(self, token):
        """Handle out-of-vocabulary tokens based on the chosen strategy."""
        if self.oov_strategy == "split":
            # Split into smaller subwords or bytes
            return [self.vocab.get(subtoken, self.vocab['<UNK>']) for subtoken in list(token)]
        elif self.oov_strategy == "approximation":
            # Approximate with pre-trained embeddings or a similar token
            return [self.vocab.get('<UNK>')]  # Placeholder for approximation logic
        else:
            raise ValueError(f"Unknown OOV strategy: {self.oov_strategy}")

    def tokenize(self, text):
        """
        Tokenize a given text.

        Args:
            text (str): The text to tokenize.
        
        Returns:
            list: A list of token IDs.
        """
        tokens = []
        text = self.pre_tokenize(text)[0]
        token = ' '.join(text)
        for merge in self.merges:
            token = token.replace(' '.join(merge), ''.join(merge))
        if token in self.vocab:
            tokens.append(self.vocab[token])
        else:
            tokens.extend(self.handle_oov(token))  # Handle OOV tokens
        return tokens

    def tokenize_batch(self, texts, num_processes=4):
        """
        Batch tokenize a list of texts in parallel.

        Args:
            texts (list): A list of texts to tokenize.
            num_processes (int): The number of parallel processes to use.
        
        Returns:
            list: A list of tokenized texts.
        """
        with Pool(processes=num_processes) as pool:
            tokenized_texts = pool.map(self.tokenize, texts)
        return tokenized_texts

    def save_vocab(self, filename):
        """Save the vocabulary and merges to a file."""
        with open(filename, 'w') as f:
            json.dump({
                "vocab": {str(k): v for k, v in self.vocab.items()},
                "merges": self.merges
            }, f)
