from matplotlib.axes import Axes

player_pos_plot_options = {
    'ms': 14,
    'alpha': 0.8,
    'mec': '#000000',
    'mew': 1,
    'linewidth': 2,
    'fillstyle': 'full',
    'marker': 'o',
}

player_shirt_plot_options = {
    'ha': 'center',
    'va': 'center',
    'fontsize': 8,
}

ball_plot_options = {
    'alpha': 1.0,
    'ms': 5,
    'mec': '#000000',
    'linewidth': 2,
    'marker': 'o',
}


def plot_player(
    x: float,
    y: float,
    shirt: int | None = None,
    *,
    ax: Axes,
    color=('#333333', '#000000'),
    **kwargs,
):
    """Plots a player on the pitch.

    Parameters
    ----------
    x : float
        x-coordinate of the player
    y : float
        y-coordinate of the player
    shirt : int, optional
        Shirt number of the player
    ax : Axes
        Axes object to plot on
    color : tuple
        Tuple of colors for the player and the shirt number
    kwargs : dict
        Additional options to pass to the pitch.scatter method
    """
    options = {**player_pos_plot_options, **kwargs}
    ax.plot(x, y, mfc=color[0], **options)
    if shirt:
        ax.text(x, y, str(shirt), c=color[1], **player_shirt_plot_options)
    return ax


def plot_ball(x: float, y: float, *, ax: Axes, color='#000000', **kwargs):
    """Plots the ball on the pitch.

    Parameters
    ----------
    x : float
        x-coordinate of the ball
    y : float
        y-coordinate of the ball
    ax : Axes
        Axes object to plot on
    color : str
        Color of the ball
    kwargs : dict
        Additional options to pass to ax.plot
    """
    options = {**ball_plot_options, **kwargs}
    ax.plot(x, y, mfc=color, **options)
    return ax
