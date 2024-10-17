# Learn By Hearing - learn a new language by hearing it with text-to-speech

Learning a new language is much easier if you hear the same sentence in the new language and also a language you are familiar with.

That's what this package aims to help you do.  You input a text file in the language you're familiar with (which contains **a list of sentences in separate lines**), and you get an audio file that has the audio in the first language and also the second language.  Currently the languages supported are only those present in both `argostranslate` and `piper`.

This is essentially a wrapper running on top of three packages:
    * `argostranslate` for translation
    * `piper` for converting text to speech (TTS)
    * `ffmpeg` for combining the audio files

# Documentation

Only tested for Ubuntu 22.04 environment, but this should work on all Linux systems.

To install using pip, first download the `requirements.txt` file, and then: 
```
pip install -r requirements.txt
pip install learnbyhear
```

It separately requires **ffmpeg** to be already installed in the system!

## Considerations

- Argos Translate is a bit heavy because of torch, so keep enough free space (~5 GB)
- Installation may take some time since dependencies must be downloaded
- First usage of any particular model will download that model

## Supported languages

- Argos Translate: https://github.com/argosopentech/argos-translate#supported-languages
- Piper: https://github.com/rhasspy/piper#voices

## Voice models

Piper languages may have multiple models and also multiple speaking styles; check https://rhasspy.github.io/piper-samples/

Some models present in the above link are **NOT** available when installed through pip.  So if you run into "RuntimeError: Number of .wav files in each dir is unequal", it is most likely a voice not found error, so just keep trying a different voice.  In the meanwhile I will investigate further and raise a issue on piper GitHub if necessary.

Currently in learnByHear you can use multiple models as you wish but speakers are not yet supported (coming soon!)

## Example usage

English to German (this is the default, outputs stored in tts/):
```
learnbyhear text_EN.txt
```

English to German with multiple output models, 1 extra repetition (for each sentence you hear EN+DE+DE), 1 second silence padding, and a specific output directory
```
learnbyhear text_EN.txt \
    --from_code en \
    --to_code de \
    --out_models de_DE-thorsten-high de_DE-thorsten_emotional-medium \
    --in_model en_GB-alan-medium \
    --repeats 1 \
    --padding 1.0 \
    --out_dir OUT_DIR/
```

List of models available on piper: https://rhasspy.github.io/piper-samples/ Please check this important note: https://gitlab.com/drohi/learnbyhear#voice-models

