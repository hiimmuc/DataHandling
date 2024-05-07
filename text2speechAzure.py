# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

# <code>
import os
import azure.cognitiveservices.speech as speechsdk
import pandas as pd
import soundfile as sf


def text2speech(text, voice_name, speech_config, save_path):
    audio_config = speechsdk.audio.AudioOutputConfig(
        use_default_speaker=True, filename=f"{save_path}.mp3")

    speech_config.speech_synthesis_voice_name = voice_name

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)

    speech_synthesis_result = speech_synthesizer.speak_text_async(
        text).get()
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(
                    cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


if __name__ == '__main__':
    # configurations
    save_dir = r"./mp3_files"
    # with open('D:\HuRoLab\workspace\DataHandling\data\sentences.csv') as rf:/home/phgnam/Workspace/workspace/Big5GenerationResponse/results/script
    #     sentences = [line.replace('\n', '') for line in rf.readlines()]\
    df = pd.read_csv(r"./data/sentences.csv")
    # sentences.remove('')
    # print(sentences, len(sentences))

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_key = "7aae4a6c4cf841ea9f0e689646ad4acc"
    service_region = "japaneast"

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region)

    # Female Voice
    character = 'ThomasNeural'
    voice_name = f'en-GB-{character}'

    save_nv_path = os.path.join(save_dir + f'/{character}')
    os.makedirs(save_nv_path, exist_ok=True)

    sent_idxes = {0: 'hollow',
                  1: 'yield',
                  2: 'thanks'}

    for idx, (personality, sentences) in enumerate(df.to_dict('list').items()):
        for sent_idx, sentence in enumerate(sentences):
            os.makedirs(
                f"{save_nv_path}/0{idx}.eHMI_{personality}/", exist_ok=True)
            text2speech(str(sentence), voice_name=voice_name,
                        speech_config=speech_config, save_path=f"{save_nv_path}/0{idx}.eHMI_{personality}/{sent_idxes[sent_idx]}")
    # </code>
    # pitch shift for affective voice
    # 12 semitones shift up 15% = 1.8 semitones = 1.8 half steps
    # y, sr = sf.read(f"{save_nv_path}/{idx}.mp3")
    # y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=1.8)
    # save_av_path = save_nv_path.replace('NV', 'AV')
    # os.makedirs(save_av_path, exist_ok=True)
    # sf.write(f"{save_av_path}/{idx}.mp3", y_shifted, sr, format='mp3')

# Male voice
# character = 'en-US-BrianNeural'

# for column in sentences:
#     save_nv_path = os.path.join(save_dir + f'/NV-MaleVoice-{column}')
#     os.makedirs(save_nv_path, exist_ok=True)
#     for idx, text in enumerate(sentences[column]):
#         audio_config = speechsdk.audio.AudioOutputConfig(
#             use_default_speaker=True, filename=f"{save_nv_path}/{idx}.mp3")
#         speech_config.speech_synthesis_voice_name = character

#         speech_synthesizer = speechsdk.SpeechSynthesizer(
#             speech_config=speech_config, audio_config=audio_config)

#         speech_synthesis_result = speech_synthesizer.speak_text_async(
#             text).get()
#         if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#             print("Speech synthesized for text [{}]".format(text))
#         elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
#             cancellation_details = speech_synthesis_result.cancellation_details
#             print("Speech synthesis canceled: {}".format(
#                 cancellation_details.reason))
#             if cancellation_details.reason == speechsdk.CancellationReason.Error:
#                 if cancellation_details.error_details:
#                     print("Error details: {}".format(
#                         cancellation_details.error_details))
#                     print("Did you set the speech resource key and region values?")
    # </code>
    # pitch shift for affective voice
    # 12 semitones shift up 15% = 1.8 semitones = 1.8 half steps
    # y, sr = sf.read(f"{save_nv_path}/{idx}.mp3")
    # y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=1.8)
    # save_av_path = save_nv_path.replace('NV', 'AV')
    # os.makedirs(save_av_path, exist_ok=True)
    # sf.write(f"{save_av_path}/{idx}.mp3", y_shifted, sr, format='mp3')
