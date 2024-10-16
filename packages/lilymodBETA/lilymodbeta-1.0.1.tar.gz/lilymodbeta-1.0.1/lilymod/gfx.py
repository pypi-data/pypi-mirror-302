from .resource import Window, Camera, Sprite
from .__globs__ import pg, os, re, _sprite_count_

""" Classes """
# ------------------------------------------------------------ #
class Renderer:
    def __init__(self, window:Window, camera:Camera, canvasSize:list[int]) -> None:
        self.layers = {
            "background":   0,
            "midground":    1,
            "foreground":   2,
        }
        self.window:Window=window
        self.camera:Camera=camera
        self.canvas:pg.Surface=pg.Surface(canvasSize)
        self.layerGroups = [ pg.sprite.Group() for layer in self.layers ]

    def addSprite(self, s:Sprite, layer:str="background") -> None:
        try:
            self.layerGroups[self.layers[layer]].add(s)
        except (IndexError) as err: ...

    def remSprite(self, s:Sprite, layer:int=0) -> None:
        try:
            self.layerGroups[layer].remove(s)
        except (IndexError) as err: ...
    
    def renderPixels(self) -> None:
        self.canvas.fill(self.window.color)
        for layer in self.layers:
            group = self.layerGroups[ self.layers[layer] ]
            
            for s in group:
                drawLocation = [
                    s.location[0] - self.camera.offset[0] ,
                    s.location[1] - self.camera.offset[1] 
                ]
                self.canvas.blit( s.image, drawLocation)

        self.window.blit(
            dest=[0,0],
            src=pg.transform.scale(self.canvas, [
                self.window.size[0] / self.camera.zoom,
                self.window.size[1] / self.camera.zoom
            ])
        )
# ------------------------------------------------------------ #

""" Sigletons """
# ------------------------------------------------------------ #
def showMouse() -> None:
    pg.mouse.set_visible(True)

def hideMouse() -> None:
    pg.mouse.set_visible(False)

def createSurface(size:list[int], color:list[int]) -> pg.Surface :
    s:pg.Surface = pg.Surface(size)
    s.fill(color)
    return s

def createRect(location:list, size:list) -> pg.Rect :
    return pg.Rect(location, size)

def flipSurface(surface:pg.Surface, x:bool, y:bool) -> pg.Surface:
    return pg.transform.flip(surface, x, y)

def fillSurface(surface:pg.Surface, color:list[int]) -> None:
    surface.fill(color)

def naturalKey(string_) -> list[int] :
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

def drawLine(display:pg.Surface, color:list[int], start:list[int|float], end:list[int|float], width:int=1) -> None :
    pg.draw.line(display, color, start, end, width=width)
    
def drawRect(display:pg.Surface, size:list[int], location:list[int|float], color:list[int]=[255,0,0], width:int=1) -> None :
    pg.draw.rect(display, color, pg.Rect(location, size), width=width)

def drawCircle(surface, color, center, radius, width=0):
    pg.draw.circle(surface, color, (int(center[0]), int(center[1])), radius, width)

def rotateSurface(surface:pg.Surface, angle:float) -> None :
    return pg.transform.rotate(surface, angle)

def scaleSurface(surface:pg.Surface, scale:list) -> pg.Surface :
    return pg.transform.scale(surface, scale)

def loadImage(file_path:str) -> pg.Surface :
    image:pg.Surface = pg.image.load(file_path).convert_alpha()
    return image

def loadImageDir(dirPath:str) -> list[pg.Surface] :
    images:list = []
    for _, __, images in os.walk(dirPath):
        sorted_images = sorted(images, key=naturalKey)
        for image in sorted_images:
            full_path = dirPath + '/' + image
            image_surface = loadImage(full_path)
            images.append(image_surface)
            
def loadImageSheet(sheetPath:str, frameSize:list[int]) -> list[pg.Surface] :
    sheet = loadImage(sheetPath)
    frame_x = int(sheet.get_size()[0] / frameSize[0])
    frame_y = int(sheet.get_size()[1] / frameSize[1])
    
    frames = []
    for row in range(frame_y):
        for col in range(frame_x):
            x = col * frameSize[0]
            y = row * frameSize[1]
            frame = pg.Surface(frameSize, pg.SRCALPHA).convert_alpha()
            frame.blit(sheet, (0,0), pg.Rect((x, y), frameSize))   # blit the sheet at the desired coords (texture mapping)
            frames.append(frame)
    return frames
# ------------------------------------------------------------ 
