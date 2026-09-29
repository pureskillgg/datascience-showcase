"""
Animations to MP4.

ffmpeg comes with the imageio-ffmpeg package, so nothing extra is installed.
Videos don't go in git: publish them on YouTube or similar, and keep a still
frame (made with save()) and the link in the gallery.
"""

from pathlib import Path

import imageio_ffmpeg
import matplotlib as mpl
from matplotlib.animation import FFMpegWriter

from .figure import _meta, add_footer


def save_animation(animation, path, *, fps=30, official=None, crf=20):
    """
    Render a matplotlib animation to an H.264 MP4 at the preset's resolution.

    The attribution line (and the logo, if official) is added to the figure
    first. crf sets the quality: lower is better and bigger; 18 to 23 is sane.
    """
    fig = animation._fig  # pylint: disable=protected-access
    add_footer(fig, official=bool(official))
    info = _meta[fig]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    mpl.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
    writer = FFMpegWriter(
        fps=fps,
        codec="libx264",
        extra_args=["-pix_fmt", "yuv420p", "-crf", str(crf), "-movflags", "+faststart"],
    )
    animation.save(
        str(path),
        writer=writer,
        dpi=info["preset"].dpi,
        savefig_kwargs={"facecolor": info["theme"].surface},
    )
    return path
