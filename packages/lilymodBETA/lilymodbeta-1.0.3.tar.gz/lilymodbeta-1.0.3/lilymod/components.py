from .__globs__ import pg
from .gfx import loadImage, loadImageSheet, flipSurface, scaleSurface, rotateSurface

# Base component class
# --------------------------- #
class Component:
    def __init__(self, sprite) -> None:
        self.sprite = sprite
    def update(self, *args, **kwargs): raise NotImplementedError
    def free(self, *args, **kwargs): raise NotImplementedError
# --------------------------- #

# --------------------------- #
class Texture(Component):
    def __init__(self, sprite, size:list[int]=[32, 32], color:list[int]=[25, 60, 80], path:str=None, renderLayer:str="background", offset:list[int]=[0,0]):
        super().__init__(sprite)
        self.flip_x:bool=False
        self.flip_y:bool=False
        self.size:list[int]=size
        self.color:list[int]=color
        self.offset:list[int]=offset
        self.render_layer:str=renderLayer
        if path: 
            self.load(path)
        else:
            self.image:pg.Surface=pg.Surface(self.size)
            self.image.fill(self.color)
    
    def set(self, texture:pg.Surface) -> None :
        self.image = texture
        self.sprite.image = self.image
    
    def load(self, path:str) -> None :
        self.set(loadImage(path))

    def flip(self, x:bool, y:bool):
        self.set(flipSurface(self.image, x, y))

    def scale(self, scale:list) -> None :
        self.size = scale
        self.set(scaleSurface(self.image, scale))

    def rotate(self, angle:float) -> None :
        self.set(rotateSurface(self.image, angle))
    
    def update(self, *args, **kwargs) -> None : return None
    
    def free(self):
        self.image = None
        self.size = None
        self.color = None
# --------------------------- #

# --------------------------- #
class Animation(Component):
    def __init__(self, sprite, flip_speed:float, dimensions:list[int], image_offset:list[int]=[0,0], loop:bool=False, loop_delay:bool=False, delay:int|float=4, scale:list[int]=[1,1], sheet_path:str=None, dir_path:str=None):
        super().__init__(sprite)
        self.nframe:int = 0
        """ number of current frame """
        self.nframes:int = 0
        """ number of total frames """
        self.texture:Texture = None
        """ current frame texture """
        self.image:pg.Surface = None
        """ current frame image """
        self.frames:list[pg.Surface] = []
        """ array of frame images """
        self.flip_speed:float = flip_speed
        """ the speed of iteration of frame images """
        self.dimensions:list[int] = dimensions
        """ dimensions of a frame """
        self.acc:float=0.0
        self.ldtime:float=delay
        """ amount of time a frame should be displayed """
        self.loop:bool = loop
        """ flag to control animation looping """
        self.loop_delay:bool=loop_delay

        self.src:str=None

        self.image_offset:list[int]=image_offset

        if self.loop == True:
            self.loop_delay = False
        
        if self.loop_delay == True:
            self.loop = False
        
        if dir_path != None:
            self.load_dir(dir_path, dimensions)
        if sheet_path != None:
            self.load_sheet(sheet_path, dimensions, scale) 
        
    def load_dir(self, dir_path:str, dimensions:list[int]): ...
    
    def load_sheet(self, sheet_path:str, dimensions:list[int], scale:list[int]=[1,1]):
        frame_images = loadImageSheet(sheet_path, dimensions)
        frame_textures = [Texture(self.sprite, dimensions, offset=self.image_offset) for _ in frame_images]
        [ frame_textures[t].set(tex) for t, tex in enumerate(frame_images) ]
        [ frame_textures[t].scale([self.dimensions[0]*scale[0], self.dimensions[1]*scale[1]]) for t, _ in enumerate(frame_images)]
        self.nframe = 0
        self.frames = frame_textures
        self.nframes = len(self.frames)
        self.image = self.frames[int(self.nframe)].image
        self.src = sheet_path
    
    def update(self, delta_time:float, *args, **kwargs) -> None :
        if self.nframes <= 0: return

        self.acc+=1*delta_time
        self.nframe += self.flip_speed * delta_time

        if self.loop:
            self.nframe %= self.nframes # loop: wrap around using modulo
        
        elif self.loop_delay: # delay the loop by the amount of frame time set
            if self.nframe >= self.nframes - 1:
                if int(self.acc) == self.ldtime:
                    self.nframe = 0 # loop: wrap around using modulo
                    self.acc = 0
                else: self.nframe = self.nframes - 1
        
        else: # no-loop: clamp to last frame
            if self.nframe >= self.nframes - 1:
                self.nframe = self.nframes - 1
            elif self.nframe < 0:   # bounds check
                self.nframe = 0
        
        self.texture = self.frames[int(self.nframe)]
        self.image = self.texture.image
    
    def free(self):
        self.frames = None
        self.image = None
        self.dimensions = None
# --------------------------- #

# --------------------------- #
class LifeRange(Component):
    def __init__(self, sprite, scalar:int|float=1.0, lifetime:int|float=None) -> None :
        super().__init__(sprite)
        self.scalar:int|float = scalar
        self.liferange = lifetime if lifetime is not None else 1.0
    
    def free(self) -> None :
        self.scalar = None
        self.liferange = None
    
    def update(self, delta_time:float, *args, **kwargs) -> None :
        self.liferange -= self.scalar * delta_time
        if self.liferange <= 0: 
            self.sprite.kill()
# --------------------------- #

# --------------------------- #
class ActionGraph(Component):
    def __init__(self, sprite) -> None:
        super().__init__(sprite=sprite)
        self.action:str=None
        self.nactions:int=0
        self.ncallbacks:int=0
        self.conditions:dict[str, bool]={}
        self.actions:dict[str, callable]={}

    def run_action(self, action:str) -> None:
        if self.action != action:
            self.action = action
            try:
                self.get_action(action=action)()
            except (AttributeError) as err: action=None; print(err) # action has no registered callback

    def get_action(self, action:str) -> None:
        callback:callable = None
        try:
            callback = self.actions.get(action, None)
        except (KeyError) as err: print(err)  # action not registered
        return callback

    def rem_action(self, action:str) -> None:
        try:
            self.actions.pop(key=action)
        except (KeyError) as err: print(err) # action not registered

    def add_action(self, action:str, callback:callable) -> None:
        if not self.get_action(action=action):
            self.actions[action] = callback
        else: ... # action already registered

    def set_action(self, action:str, callback:callable) -> None:
        if self.get_action(action=action):
            self.actions[action] = callback
        else: ... # action not registered

    def try_condition(self, con:str) -> bool:
        try:
            return self.get_condition(con=con)()
        except (AttributeError) as err: print(err); return False # action has no registered callback

    def get_condition(self, con:str) -> None:
        callback:callable = None
        try:
            callback = self.conditions.get(con, None)
        except (KeyError) as err: print(err)  # action not registered
        return callback

    def rem_condition(self, con:str) -> None:
        try:
            self.conditions.pop(key=con)
        except (KeyError) as err: print(err) # action not registered

    def add_condition(self, con:str, callback:callable) -> None:
        if not self.get_condition(con=con):
            self.conditions[con] = callback
        else: ... # action already registered

    def set_condition(self, con:str, callback:callable) -> None:
        if self.get_condition(con=con):
            self.conditions[con] = callback
        else: ... # action not registered

    def update(self, *args, **kwargs) -> None:
        for con in self.conditions.keys():
            if self.try_condition(con):
                self.run_action(con)
# --------------------------- #
