from typing import overload

from matplotlib.axes import Axes

from gandula.config import PITCH_LENGTH, PITCH_WIDTH

from ..providers.pff.schema.event import PFF_Event, PFF_PossessionEvent
from ..providers.pff.schema.tracking import PFF_Frame
from ..schemas.atomic_spadl.types import SpadlAction
from ..viz.frame import plot_ball, plot_player
from ..viz.pitch import get_pitch

pydantic_dump_options = {
    'exclude_none': True,
    'exclude_defaults': True,
    'exclude_unset': True,
}


@overload
def _view_pff_event(events: PFF_Event | PFF_PossessionEvent, **kwargs) -> dict: ...


@overload
def _view_pff_event(
    events: list[PFF_Event | PFF_PossessionEvent], **kwargs
) -> list[dict]: ...


def _view_pff_event(
    events: PFF_Event | PFF_PossessionEvent | list[PFF_Event | PFF_PossessionEvent],
    **kwargs,
) -> dict | list[dict]:
    options = {**pydantic_dump_options, **kwargs}

    if isinstance(events, list):
        return [evt.model_dump(**options) for evt in events]

    return events.model_dump(**options)


@overload
def _view_pff_frame(frames: PFF_Frame, **kwargs) -> Axes: ...


@overload
def _view_pff_frame(frames: list[PFF_Frame], **kwargs) -> list[Axes]: ...


def _view_pff_frame(
    frames: PFF_Frame | list[PFF_Frame],
    *,
    pitch_length=PITCH_LENGTH,
    pitch_width=PITCH_WIDTH,
    home_colors=('#FFFFFF', '#000000'),
    away_colors=('#000000', '#FFFFFF'),
    ball_color='#000000',
    **kwargs,
) -> Axes | list[Axes]:
    pitch, _, ax = get_pitch(**kwargs)

    if isinstance(frames, PFF_Frame):
        frames = [frames]

    for frame in frames:
        for player in frame.home_players:
            plot_player(
                player.x + (pitch_length / 2),
                player.y + (pitch_width / 2),
                color=home_colors,
                ax=ax,
                shirt=player.jersey,
                **kwargs,
            )

        for player in frame.away_players:
            plot_player(
                player.x + (pitch_length / 2),
                player.y + (pitch_width / 2),
                color=away_colors,
                ax=ax,
                shirt=player.jersey,
                **kwargs,
            )

        if frame.ball:
            ball = frame.ball[0]
            if ball.x is not None and ball.y is not None:
                plot_ball(
                    ball.x + (pitch_length / 2),
                    ball.y + (pitch_width / 2),
                    color=ball_color,
                    ax=ax,
                    **kwargs,
                )

    return ax


def _view_spadl_action(action: SpadlAction | list[SpadlAction], **kwargs) -> dict: ...


def view(objs, **kwargs):
    """Single entry point for visualizing gandula objects.

    Parameters
    ----------
    objs : PFF_Event | PFF_PossessionEvent | PFF_Frame | SpadlAction
        The object to be visualized.
    kwargs : dict
        Options to be passed to the view function.
    """
    obj = objs[0] if isinstance(objs, list) else objs

    if isinstance(obj, PFF_Event) or isinstance(obj, PFF_PossessionEvent):
        return _view_pff_event(objs, **kwargs)
    if isinstance(obj, PFF_Frame):
        return _view_pff_frame(objs, **kwargs)
    if isinstance(obj, SpadlAction):
        return _view_spadl_action(objs, **kwargs)

    if hasattr(obj, 'model_dump'):
        options = {**pydantic_dump_options, **kwargs}
        return obj.model_dump(**options)

    raise ValueError(f'Cannot view object of type {type(obj)}')
