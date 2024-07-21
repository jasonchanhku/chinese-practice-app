
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
import json
import pandas as pd

class ExampleUsage(BaseModel):
    chinese: str
    pinyin: str
    english: str
    audio_bytes: str

class WordEntry(BaseModel):
    word: str
    pinyin:str
    translation: str
    pronounciation_audio_bytes: str
    definitions: List[str]
    example_usages: List[ExampleUsage]

# Declaring the full list type that holds multiple word entries.
class DictionaryEntries(BaseModel):
    entries: List[WordEntry]
    
with open("./data/output_compiled/keywords/keywords.json") as json_file:
        loaded_keywords = json.load(json_file)

# Deserializing the JSON data into Pydantic models
chinese_keywords = DictionaryEntries(entries=[WordEntry(**entry) for entry in loaded_keywords]).entries


chinese_keywords_df = pd.DataFrame([chinese_keyword.model_dump(exclude={"example_usages": {"__all__": {"audio_bytes"}}, "pronounciation_audio_bytes":True}) for chinese_keyword in chinese_keywords])
