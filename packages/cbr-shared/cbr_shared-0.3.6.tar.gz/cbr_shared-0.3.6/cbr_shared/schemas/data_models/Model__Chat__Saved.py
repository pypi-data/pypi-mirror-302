from dataclasses import dataclass, field
from typing import Optional

from osbot_utils.helpers.Random_Guid_Short import Random_Guid_Short
from osbot_utils.helpers.Timestamp_Now import Timestamp_Now

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid import Random_Guid


@dataclass
class Model__Chat__Saved(Type_Safe):
    chat_path: str               = None
    user_id  : str               = None
    chat_id  : Random_Guid_Short = None
    data     : dict              = field(default_factory=list)
    timestamp: Timestamp_Now     = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_id   = Random_Guid_Short()
        self.timestamp = Timestamp_Now()
