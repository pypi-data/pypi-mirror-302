import lily.gfx as gfx
import lily.input as input
import lily.events as events
import lily.physics as physics
import lily.resource as resource
import lily.lilymath as blackMath
import lily.components as components

import os, platform, lily.version as ver
if "LILY_NO_PROMT" not in os.environ:
    print(
        f"Lily {ver.LILY_MAJOR}.{ver.LILY_MINOR}.{ver.LILY_PATCH} | Random Quote..."
    )