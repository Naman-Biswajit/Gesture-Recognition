from dataclasses import dataclass

@dataclass
class Config:
    _tx_: tuple
    _bx_: tuple
    _cr_: tuple
    _ln_: tuple
    delay: int
    camera_index: int
    thres_active: int
    dominant_hand: str
    gen_line: bool

def parse_config():
    instance = Config(
        _tx_ = 0,
        _bx_ = (128, 128, 0),
        _cr_ = (52, 0, 199),
        _ln_ = (144, 157, 42),
        delay = 15,
        camera_index = 0,
        thres_active = 300,
        dominant_hand = 'right',
        gen_line=True
    )
    
    return instance