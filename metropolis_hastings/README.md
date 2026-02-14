# Metropolis-Hastings

This project implements a **Metropolis–Hastings algorithm** to decrypt a classic substitution cryptography in short sentence (around 30 to 50 words) when the frequence analyses cannot work.

- Builds a bigram probability matrix from `data.txt` (*Du côté de chez Swann*, Proust)
- Maximizes the plausibility of a sentence by maximizing its bigram probability
- Uses MCMC sampling to explore the search space and avoid local maxima

## Comments

- The algorithm does not always fully decrypt the sentence, but it often recovers enough structure to allow manual correction.
- The model is adapted to the French language, since the bigram probabilities are computed from a French text corpus.

## Code Example

Initial sentence:
```python
import random

key = list(range(26))
random.shuffle(key)

sentence = 'je suis le plus grand de ma classe et mon sac a dos est bleu'
crypted_sentence = 'xs ltil es petl yjmcf fs dm gemlls sh doc lmg m fol slh rest'

key = np.random.permutation(26)
decrypt_sentence = decrypt_sentence(crypt_array, key)
print(decrypt_sentence)
```

```
je surs le plus chand de ma ilasse et mon sai a dos est bleu
```

## Source 

This project is mostly based on the beautiful [video](https://www.youtube.com/watch?v=z4tkHuWZbRA&list=LLhm1YaU3029LFDPh7U3LTGg) from *ScienceEtonnante* (in french) and the method has been used in real context like in the investigation related to the *Zodiac* criminal case.