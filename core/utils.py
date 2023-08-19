from dataclasses import dataclass, asdict

@dataclass
class Model:
    static_image_mode: bool = False,
    max_num_hands: int = 1
    min_detection_confidence: float = 0.8
    min_tracking_confidence: float = 0.5


@dataclass
class Config:
    _tx_: tuple = (56, 0, 255)
    _bx_: tuple = (128, 128, 0)
    _cr_: tuple = (52, 0, 199)
    _ln_: tuple = (144, 157, 42)
    field_clr: tuple = (244, 168, 57)
    width: int = 1080
    height: int = 520
    field_opacity: float = 0.19
    delay: int = 15
    camera_index: int = 0
    thres_y: int = round(0.5*height)
    thres_x: int = round(0.7*width)
    logging = False
    G_field: bool = True
    log_format: str = '%(asctime)s ~ %(levelname)s:%(message)s'
    log_mode: str = 'w+'
    field_toggle: bool = False
    x_offset: int = 100
    x_offset: int = 100
    even: int = 6

fetch_asdict_model = lambda **kwargs: asdict(Model(**kwargs))