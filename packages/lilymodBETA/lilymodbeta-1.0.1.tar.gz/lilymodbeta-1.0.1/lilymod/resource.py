from .__globs__ import _logger, pg, time, CameraMode, _sprite_count_, _lily_dir_

class Clock:
    FPS:int=0
    maxFPS:int=144
    last:float=0.0
    delta:float=0.0
    current:float=0.0

    def tick(self) -> None:
        self.current = time.time()

        if self.last == 0.0:
            self.delta = 0.0
        else: self.delta = self.current - self.last

        self.last = self.current

        if self.delta > 0: self.FPS = 1 / self.delta

    def rest(self) -> None:
        time.sleep(max(1 / self.maxFPS - self.delta, 0))

class Window:
    def __init__(self, w:int=800, h:int=600, t:str="Lily: Game Window", color:list[int]=[140, 130, 160]) -> None:
        self.title:str=t
        self.color:list[int]=color
        self.size:list[int]=[w, h]
        self._internal:pg.Surface=pg.display.set_mode(self.size)
        pg.display.set_caption(self.title)
        pg.display.set_icon(pg.image.load(f"{_lily_dir_}assets\\logo.png"))

    def clear(self) -> None:
        self._internal.fill(self.color)

    def blit(self, src:pg.Surface, dest:list[float]) -> None:
        self._internal.blit(src, dest)

class Sprite(pg.sprite.Sprite):
    def __init__(self, size:list[int]=[32, 32], dest:list[float]=None, color:list[int]=[255, 0, 0], fixed:bool=False, *groups) -> None:
        super().__init__(*groups)
        self.fixed:bool=fixed
        self.id:int = next(_sprite_count_)
        self.size:list[int]=size
        self.color:list[int] = color
        self.rectCopy:pg.Rect = None
        self.location:list[float] = dest if dest is not None else [100.0, 100.0]
        self.rect:pg.Rect = pg.Rect(self.location, size)
        self.image = pg.Surface(size); self.image.fill(color)

        self.components:dict[object]={}

    def updateComponents(self, deltaTime:float, *args, **kwargs) -> None:
        for component in self.components:
            self.components[component].update(deltaTime, *args, **kwargs)

    def addComponent(self, component:object) -> None:
        try:
            self.components[type(component)]
        except (KeyError) as err:
            self.components[type(component)] = component
    
    def getComponent(self, component:object) -> object | None:
        try:
            return self.components[component]
        except (KeyError) as err: return None

    def swapRect(self, r:pg.Rect) -> None:
        if self.rectCopy == None:
            self.rectCopy = self.rect.copy()
            self.rect = r
        else:
            self.rect = self.rectCopy
            self.rectCopy = None
        
    def reColor(self, color:list[int]) -> None:
        self.color = color
        self.image.fill(color)

    def reLocate(self, delta:list[float], deltaTime:float) -> None:
        self.location[0] += delta[0] * deltaTime
        self.location[1] += delta[1] * deltaTime
        self.rect.topleft = self.location

    def update(self, deltaTime:float, *args, **kwargs) -> None:
        self.updateComponents(deltaTime, *args, **kwargs)

    def kill(self) -> None:
        [ g.remove(self) for g in self.groups() ]
        self.id = -1
        self.rect = None
        self.image = None
        self.rectCopy = None

class Camera:
    def __init__(self, window:Window, viewSize:list[int]=[400,300]) -> None:
        self.zoom:float=1.0
        self.speed:float=100.0
        self.dampening:float=0.05
        self.window:Window=window
        self.viewSize:list[int]=viewSize
        self.delta:list[float]=[0.0, 0.0]
        self.offset:list[float]=[0.0, 0.0]
        self.location:list[float]=[0.0, 0.0]
        self.mode:CameraMode=CameraMode.CenterTarget
        self.view:pg.Rect=pg.Rect(self.location, self.viewSize)
        self.center:list[float]=[
            self.location[0] + self.viewSize[0]/2,
            self.location[1] + self.viewSize[1]/2,
        ]

        self.target:Sprite = None

    def modZoom(self, delta:float) -> None:
        if self.zoom + delta < 0.4 or self.zoom + delta > 1.0: return
        self.zoom += delta

    def targetSprite(self, s:Sprite) -> None: self.target = s

    def centerTarget(self, bounds:list[int], deltaTime:float) -> None:
        self.center = [
            self.target.location[0] + self.target.size[0]/2,
            self.target.location[1] + self.target.size[1]/2,
        ]

        self.delta = [
            self.center[0] - (self.location[0] + self.viewSize[0]/2),
            self.center[1] - (self.location[1] + self.viewSize[1]/2)
        ]
        
        self.location[0] += ((self.delta[0] * self.speed) * self.dampening) * deltaTime
        self.location[1] += ((self.delta[1] * self.speed) * self.dampening) * deltaTime

        self.location[0] = max(0, min(self.location[0], bounds[0] - self.viewSize[0]))
        self.location[1] = max(0, min(self.location[1], bounds[1] - self.viewSize[1]))

        # produce an offset value that the Render() resource can use to properly center the target sprite
        self.offset = [
            self.location[0] - self.window.size[0] / 4 * self.zoom + (self.target.size[0]/self.zoom)  ,
            self.location[1] - self.window.size[1] / 4 * self.zoom + (self.target.size[1]/self.zoom)
        ]

    def process(self, bounds:list[int], deltaTime:float) -> None:
        match self.mode:
            case CameraMode.CenterTarget: self.centerTarget(bounds, deltaTime)
        self.view.topleft = self.location
