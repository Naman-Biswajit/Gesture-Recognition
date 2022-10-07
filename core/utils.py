from dataclasses import dataclass


@dataclass
class Config:
    _tx_: tuple = (56, 0, 255)
    _bx_: tuple = (128, 128, 0)
    _cr_: tuple = (52, 0, 199)
    _ln_: tuple = (144, 157, 42)
    delay: int = 15
    camera_index: int = 0
    thres_active: int = 300
    dominant_hand: str = 'right'
    gen_line: bool = True
    log_format: str = '%(asctime)s  %(levelname)s:%(message)s'
    log_mode: str = 'w+'
