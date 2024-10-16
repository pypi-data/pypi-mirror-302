from .gfx import Sprite
from .__globs__ import _sprite_max_

class Transformer:
    def __init__(self) -> None:
        self.gravity:float=90.8
        self.friction:float=1.0
        
        self.massArr:list[float]=[ None for _ in range(_sprite_max_)]
        self.velocityArr:list[list[float]]=[ [] for _ in range(_sprite_max_)]

        self.state:dict[str, bool]={
            "gravity": True,
            "friction": True,
        }

    def toggleState(self, state:str) -> bool:
        try:
            self.state[state] = not self.state[state]
            return self.state[state]
        except (KeyError) as err: return False

    def getMass(self, s:Sprite) -> list|None:
        try:
            return self.massArr[s.id]
        except (IndexError) as err: return None

    def getVelocity(self, s:Sprite) -> list|None:
        try:
            return self.velocityArr[s.id]
        except (IndexError) as err: return None

    def addSprite(self, s:Sprite) -> None:
        self.massArr.insert(s.id, 10.0)
        self.velocityArr.insert(s.id, [0.0, 0.0])

    def modMass(self, s:Sprite, mass:float) -> None:
        try:
            self.massArr[s.id] = mass if mass else self.massArr[s.id]
        except (IndexError) as err: ...
    
    def modVelocity(self, s:Sprite, vel:list[float]) -> None:
        try:
            self.velocityArr[s.id][0] = vel[0] if vel[0] else self.velocityArr[s.id][0]
            self.velocityArr[s.id][1] = vel[1] if vel[1] else self.velocityArr[s.id][1]
        except (IndexError) as err: ...

    def applyGravity(self, s:Sprite, deltaTime:float) -> None:
        try:
            self.velocityArr[s.id][1] += (self.massArr[s.id] * self.gravity) * deltaTime
        except (IndexError) as err: ...

    def applyFriction(self, s:Sprite, deltaTime:float) -> None:
        try:
            if self.velocityArr[s.id][0] > 0:
                self.velocityArr[s.id][0] -= self.friction
                if self.velocityArr[s.id][0] <= 0:
                        self.velocityArr[s.id][0] = 0.0
            elif self.velocityArr[s.id][0] < 0:
                self.velocityArr[s.id][0] += self.friction
                if self.velocityArr[s.id][0] >= 0:
                        self.velocityArr[s.id][0] = 0.0
        except (IndexError) as err: ...

    def transformSprite(self, s:Sprite, deltaTime:float) -> None:
        if s.id < 0: return
        if not s.fixed:
            if self.state["gravity"]: self.applyGravity(s, deltaTime)
            if self.state["friction"]: self.applyFriction(s, deltaTime)
        s.reLocate(self.velocityArr[s.id], deltaTime)

