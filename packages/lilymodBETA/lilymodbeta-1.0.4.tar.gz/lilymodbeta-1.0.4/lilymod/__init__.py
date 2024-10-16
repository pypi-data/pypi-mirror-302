import lilymod.gfx as gfx
import lilymod.input as input
import lilymod.events as events
import lilymod.physics as physics
import lilymod.resource as resource
import lilymod.lilymath as blackMath
import lilymod.components as components

import os, platform, lilymod.version as ver
if "LILY_NO_PROMT" not in os.environ:
    print(
        f"Lily {ver.LILYMOD_MAJOR}.{ver.LILYMOD_MINOR}.{ver.LILYMOD_PATCH} | Random Quote..."
    )