from __future__ import annotations

import asyncio


class AnnotatedFrameBuffer:
    """Holds the latest JPEG-encoded annotated frame for MJPEG streaming."""

    def __init__(self) -> None:
        self._jpeg_bytes: bytes = b""
        self._frame_index: int = 0
        self._width: int = 0
        self._height: int = 0
        self._new_frame: asyncio.Event = asyncio.Event()

    def store(
        self,
        jpeg_bytes: bytes,
        frame_index: int,
        width: int,
        height: int,
    ) -> None:
        self._jpeg_bytes = jpeg_bytes
        self._frame_index = frame_index
        self._width = width
        self._height = height
        self._new_frame.set()

    async def wait_for_frame(self, timeout_s: float = 1.0) -> bytes | None:
        try:
            await asyncio.wait_for(self._new_frame.wait(), timeout=timeout_s)
        except asyncio.TimeoutError:
            return None
        self._new_frame.clear()
        return self._jpeg_bytes

    @property
    def latest(self) -> bytes:
        return self._jpeg_bytes

    @property
    def frame_index(self) -> int:
        return self._frame_index
