from dataclasses import dataclass


@dataclass
class Config:
    _tx_: tuple = (56, 0, 255)
    _bx_: tuple = (128, 128, 0)
    _cr_: tuple = (52, 0, 199)
    _ln_: tuple = (144, 157, 42)
    field_clr: tuple = (0, 97, 242)
    field_opacity: float = 0.19
    delay: int = 15
    camera_index: int = 0
    thres_y: int = 400
    thres_x: int = 500
    logging = False
    gen_box: bool = True
    log_format: str = '%(asctime)s ~ %(levelname)s:%(message)s'
    log_mode: str = 'w+'

def fetch_default_config():
    return Config()