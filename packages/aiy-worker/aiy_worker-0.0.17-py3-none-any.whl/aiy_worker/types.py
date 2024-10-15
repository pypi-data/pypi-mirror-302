
from enum import Enum
from typing import List

class PayloadErrorLocation:
    line: int
    column: int
    def __init__(self, location: dict):
        self.line = location['line']
        self.column = location['column']

class PayloadError:
    message: str
    locations: List[PayloadErrorLocation]
    path: List[str]

    def __init__(self, error: dict):
        self.message = error['message']
        self.locations = [PayloadErrorLocation(i) for i in error['locations']]
        self.path = error.get('path')

class Lora:
    def __init__(self, props: dict) -> None:
        self.name = props.get('name')
        self.weight = props.get('weight')

    def __str__(self) -> str:
        return f'[{self.name}:{self.weight}]'

class Text2ImageProps:
    def __init__(self, props: dict) -> None:
        self.prompt = props.get('prompt')
        self.negative_prompt = props.get('negativePrompt')
        self.seed = props.get('seed')
        self.width = props.get('width')
        self.height = props.get('height')
        self.n_steps = props.get('nSteps')
        self.ip_adapter_image_url = props.get('ipAdapterImageUrl')
        self.ip_adapter_face_image_url = props.get('ipAdapterFaceImageUrl')
        self.canny_reference_url = props.get('cannyReferenceUrl')
        self.depth_reference_url = props.get('depthReferenceUrl')
        self.openpose_reference_url = props.get('openposeReferenceUrl')
        self.cfg = props.get('cfg')
        self.init_image = props.get('initImage')
        self.mask_image = props.get('maskImage')
        loras = props.get('loras')
        self.loras = None
        if loras and isinstance(loras, list):
            self.loras = [Lora(obj) for obj in loras]

class CannyProps:
    def __init__(self, props: dict) -> None:
        self.image_url = props.get('imageUrl')

class DepthProps:
    def __init__(self, props: dict) -> None:
        self.image_url = props.get('imageUrl')

class OpenposeProps:
    def __init__(self, props: dict) -> None:
        self.image_url = props.get('imageUrl')

class SadtalkerProps:
    def __init__(self, props: dict) -> None:
        self.image_url = props.get('imageUrl')
        self.audio_url = props.get('audioUrl')

class TTSProps:
    def __init__(self, props: dict) -> None:
        self.text = props.get('text')
        self.actor = props.get('actor')
        self.seed = props.get('seed')

class MusicProps:
    def __init__(self, props: dict) -> None:
        self.prompt = props.get('prompt')
        self.duration = props.get('duration')

class TaskKind(Enum):
    TEXT_TO_IMAGE = 1
    CANNY = 2
    DEPTH = 3
    OPENPOSE = 4
    INPAINT = 5
    SADTALKER = 6
    TTS = 7
    MUSIC = 8

class Task:
    def __init__(self, data: dict):
        self.id = None
        self.name = None
        if data is None:
            return
        subscribe_task: dict = data.get('subscribeTasks')
        if subscribe_task:
            self.id = subscribe_task.get('id')
            self.name = subscribe_task.get('name')
            self.text2Image = None
            if subscribe_task.get('text2Image'):
                self.text2Image = Text2ImageProps(subscribe_task.get('text2Image'))
            self.inpaint = None
            if subscribe_task.get('inpaint'):
                self.inpaint = Text2ImageProps(subscribe_task.get('inpaint'))
            self.canny = None
            if subscribe_task.get('canny'):
                self.canny = CannyProps(subscribe_task.get('canny'))
            self.depth = None
            if subscribe_task.get('depth'):
                self.depth = DepthProps(subscribe_task.get('depth'))
            self.openpose = None
            if subscribe_task.get('openpose'):
                self.openpose = OpenposeProps(subscribe_task.get('openpose'))
            self.sadtalker = None
            if subscribe_task.get('sadtalker'):
                self.sadtalker = SadtalkerProps(subscribe_task.get('sadtalker'))
            self.tts = None
            if subscribe_task.get('tts'):
                self.tts = TTSProps(subscribe_task.get('tts'))
            self.music = None
            if subscribe_task.get('music'):
                self.music = MusicProps(subscribe_task.get('music'))

    @property
    def kind(self):
        if self.name == 'inpaint':
            return TaskKind.INPAINT
        if self.text2Image is not None:
            return TaskKind.TEXT_TO_IMAGE
        if self.canny is not None:
            return TaskKind.CANNY
        if self.depth is not None:
            return TaskKind.DEPTH
        if self.openpose is not None:
            return TaskKind.OPENPOSE
        if self.sadtalker is not None:
            return TaskKind.SADTALKER
        if self.music is not None:
            return TaskKind.MUSIC
        if self.tts is not None:
            return TaskKind.TTS
        return None

class Payload:
    def __init__(self, payload: dict) -> None:
        self.errors = None
        self.task = None
        if payload.get('errors') is not None:
            errors = payload.get('errors')
            self.errors = [PayloadError(i) for i in errors]
        if isinstance(payload, list):
            self.errors = [PayloadError(i) for i in payload]
        else:
            self.task = Task(payload.get('data', {}))


class WsData:
    type: str
    id: str
    def __init__(self, data: dict) -> None:
        self.type = data.get('type')
        self.id = data.get('id')
        self.payload = Payload(data.get('payload'))

class TaskKindCapability(Enum):
    Text2Image = 'TEXT2_IMAGE'
    Inpaint = 'INPAINT'
    CannyModel = 'CANNY_MODEL'
    PoseModel = 'POSE_MODEL'
    DepthModel = 'DEPTH_MODEL'
    CannyPreprocess = 'CANNY_PREPROCESS'
    DepthPreprocess = 'DEPTH_PREPROCESS'
    PosePreprocess = 'POSE_PREPROCESS'
    Style = 'STYLE'
    StyleFace = 'STYLE_FACE'
    Sadtalker = 'SADTALKER'
    TTS = 'TTS'
    Music = 'MUSIC'
