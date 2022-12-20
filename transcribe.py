import whisper
from pathlib import Path
from tqdm import tqdm

model = whisper.load_model("large-v2")
paths = Path("data/").glob("**/*.wav")

data = []
progress = tqdm(list(paths))
for wav in progress:
    progress.set_postfix({"video" : wav.parent})
    result = model.transcribe(str(wav))
    with open(wav.parent/ "transcript.srt", "w", encoding="utf-8") as srt:
        whisper.utils.write_srt(result["segments"], file=srt)
    with open(wav.parent/ "transcript.txt", "w", encoding="utf-8") as txt:
        whisper.utils.write_txt(result["segments"], file=txt)