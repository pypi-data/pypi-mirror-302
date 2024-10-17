# Learn By Hearing - learn a new language by hearing it with text-to-speech

Learning a new language is much easier if you hear the same sentence in the new language and also a language you are familiar with.

That's what this package aims to help you do.  You input a text file in the language you're familiar with (which contains **a list of sentences in separate lines**), and you get an audio file that has the audio in the first language and also the second language.  Currently the languages supported are only those present in both `argostranslate` and `piper`.

This is essentially a wrapper running on top of three packages:
    * `argostranslate` for translation
    * `piper` for converting text to speech (TTS)
    * `ffmpeg` for combining the audio files

# Documentation

Only tested for Ubuntu 22.04 environment, but this should work on all Linux systems.  Best to use it in a virtual environment, as you should do with any Python package!

To install using pip, first download the `requirements.txt` file, and then: 
```
pip install -r requirements.txt
pip install learnbyhear
```

### You need to separately have **ffmpeg** already installed in the system!

## Considerations

- Dependencies are a bit heavy, so keep enough free space (~5 GB)
- Installation may take some time since dependencies must be downloaded
- First usage of any particular model will download that model
- I designed it such that it is meant to be used once a large text file, and then never.  Yes, this is also my excuse for not optimizing it ;)

## Supported languages

Currently the languages supported are only those present in both `argostranslate` and `piper`.

- Argos Translate: https://github.com/argosopentech/argos-translate#supported-languages
- Piper: https://github.com/rhasspy/piper#voices

## Voice models

Piper languages may have multiple models and also multiple speaking styles; check https://rhasspy.github.io/piper-samples/

Multiple models and speakers are supported!

## Example usage

English to German (this is the default, outputs stored in `tts/`):
```
learnbyhear text_EN.txt
```

English to German with three different output models (two of them actually a different speaker from the same model), 1 extra repetition (for each sentence you hear EN + DE_model_1 + DE_model_2 + DE_model_3 + DE_model_1 + DE_model_2 + DE_model_3), 1 second silence padding, and a specific output directory
```
learnbyhear text_EN.txt \
    --from_code en \
    --to_code de \
    --out_models de_DE-thorsten-high de_DE-thorsten_emotional-medium:4 de_DE-thorsten_emotional-medium:5 \
    --in_model en_GB-alan-medium \
    --repeats 1 \
    --padding 1.0 \
    --out_dir OUT_DIR/
```

List of models available on piper: https://rhasspy.github.io/piper-samples/ 

