from modules.operations import Vector

class Build:
    def __init__(self, scene_dict) -> None:
        self.HEIGHT: int = scene_dict['v_res']
        self.WIDHT: int  = scene_dict['h_res']
        self.PIXEL_SIZE: float = scene_dict['square_side']
        self.DISTANCE: float = scene_dict['dist']
        self.CAM_EYE: list = Vector(*scene_dict['eye'])
        self.CAM_LOOT_AT: list = Vector(*scene_dict['look_at'])
        self.UP_VECTOR: list = Vector(*scene_dict['up'])
        self.BACKGROUND_COLOR: list = scene_dict['background_color']
        self.OBJECTS: list = scene_dict['objects']
        
    def rayBuild(self):
        # 1 construir a base ortonomal
        # 2 construir todos os rais
        # 3 setar os pixels
        ...

