import os
import time
import string
from typing import List, Dict

# Méthode 1: Dictionnaire (référence)
def count_words_dict(files: List[str]) -> Dict[str, Dict[str, int]]:
    results = {}
    for filename in files:
        word_counts = {}
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.strip().lower().split()
                for word in words:
                    word = word.strip(string.punctuation)
                    if word:
                        word_counts[word] = word_counts.get(word, 0) + 1
        results[filename] = word_counts
    return results
# Méthode 2: Set + List
def count_words_set_list(files: List[str]) -> Dict[str, Dict[str, int]]:
    results = {}
    for filename in files:
        unique_words = set()
        word_counts_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.strip().lower().split()
                for word in words:
                    word = word.strip(string.punctuation)
                    if word:
                        if word not in unique_words:
                            unique_words.add(word)
                            word_counts_list.append([word, 1])
                        else:
                            for item in word_counts_list:
                                if item[0] == word:
                                    item[1] += 1
                                    break
        results[filename] = {item[0]: item[1] for item in word_counts_list}
    return results

# Méthode 3: Naïve brute force
def count_words_brute_force(files: List[str]) -> Dict[str, Dict[str, int]]:
    results = {}
    for filename in files:
        word_counts_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                words = line.strip().lower().split()
                for word in words:
                    word = word.strip(string.punctuation)
                    if not word:
                        continue
                    found = False
                    for i in range(len(word_counts_list)):
                        if word_counts_list[i][0] == word:
                            word_counts_list[i][1] += 1
                            found = True
                            break
                    if not found:
                        word_counts_list.append([word, 1])
        results[filename] = {item[0]: item[1] for item in word_counts_list}
    return results
# Génération de fichiers factices
def create_dummy_files(base_name: str, num_files: int, size_in_words: int) -> List[str]:
    filenames = [f"{base_name}{i + 1}.txt" for i in range(num_files)]
    dummy_words = ["python", "performance", "test", "data", "count", "word", "file", "analysis", "compare", "benchmark"]
    for filename in filenames:
        with open(filename, 'w') as f:
            for _ in range(size_in_words):
                f.write(f"{dummy_words[int(time.time() * 1000) % len(dummy_words)]} ")
    return filenames

# Exécution des tests
def run_detailed_tests():
    implementations = {
        "dict": count_words_dict,
        "set+list": count_words_set_list,
        "brute_force": count_words_brute_force
    }
    NUM_FILES = 3
    FILE_SIZE_WORDS = 10000
    filenames = create_dummy_files("testfile", NUM_FILES, FILE_SIZE_WORDS)

    try:
        for name, func in implementations.items():
            print(f"\nMéthode: {name}")
            for filename in filenames:
                start_time = time.time()
                result = func([filename])[filename]
                duration = time.time() - start_time
                print(f"  Fichier: {filename} | Temps: {duration:.4f}s | Mots uniques: {len(result)}")
    finally:
        for filename in filenames:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == "__main__":
    run_detailed_tests()
