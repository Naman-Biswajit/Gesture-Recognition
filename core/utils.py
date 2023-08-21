from dataclasses import dataclass, asdict


@dataclass
class Model:
    static_image_mode: bool = False,
    max_num_hands: int = 1
    min_detection_confidence: float = 0.8
    min_tracking_confidence: float = 0.5


@dataclass
class Config:
    # Requirements
    _tx_: tuple = (56, 0, 255)
    _bx_: tuple = (128, 128, 0)
    _cr_: tuple = (52, 0, 199)
    _ln_: tuple = (144, 157, 42)
    field_clr: tuple = (244, 168, 57)
    rect_clr: tuple = (66, 245, 72)
    thickness: int = 3
    radii: int = 13
    circle_clr: tuple = (105, 78, 72)
    mid_clr: tuple = (0, 127, 247)

    width: int = 640
    height: int = 480
    field_opacity: float = 0.19
    delay: int = 1
    camera_index: int = 0
    ty: int = round(0.5*height)
    tx: int = round(0.7*width)
    sensitivity: float = 7
    click_rate = 0.5 # (SECONDS)
    click_thresthold: int = 30

    # Offsets
    tof: int = 20
    dof: int = 200
    lof: int = 100
    rof: int = 100

    # Optionals
    logging = False
    G_field: bool = True
    log_format: str = '%(asctime)s ~ %(levelname)s:%(message)s'
    log_mode: str = 'w+'
    field_toggle: bool = False


fetch_asdict_model = lambda **kwargs: asdict(Model(**kwargs))
