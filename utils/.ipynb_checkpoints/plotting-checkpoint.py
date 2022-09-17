import matplotlib.pyplot as plt
import numpy as np

class BlitManager:
    
    def __init__(self, canvas, animated_artists=()):
        """
        Parameters
        ----------
        canvas : FigureCanvasAgg
            The canvas to work with, this only works for sub-classes of the Agg
            canvas which have the `~FigureCanvasAgg.copy_from_bbox` and
            `~FigureCanvasAgg.restore_region` methods.

        animated_artists : Iterable[Artist]
            List of the artists to manage
        """
        self.canvas = canvas
        self._bg = None
        self._artists = []

        for a in animated_artists:
            self.add_artist(a)
        # grab the background on every draw
        self.cid = canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._bg = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()

    def add_artist(self, art):
        """
        Add an artist to be managed.

        Parameters
        ----------
        art : Artist

            The artist to be added.  Will be set to 'animated' (just
            to be safe).  *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def update(self):
        """Update the screen with animated artists."""
        cv = self.canvas
        fig = cv.figure
        # paranoia in case we missed the draw event,
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            cv.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            cv.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
        cv.flush_events()
        

def set_matplotlib_options():
    
    try:
        plt.style.use(["science", "notebook"])
        
    except:
        print("Couldn't import matplotlib style correctly.")
        if input("Do you want to install SciencePlots? [y/n]") == "y":
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "SciencePlots"])
            print("Succesfully installed SciencePlots")
            plt.style.use(["science", "notebook"])
        
        else:
            raise ModuleNotFoundError("Please install SciencePlots.")

    plt.rcParams["legend.fancybox"] = False
    plt.rcParams["legend.frameon"] = True
    plt.rcParams["legend.edgecolor"] = "black"
    plt.rcParams["legend.fontsize"] = 13
    plt.rcParams["legend.framealpha"] = 1

    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12

    plt.rcParams["axes.labelsize"] = 14
    plt.rcParams["axes.titlesize"] = 17
    plt.rcParams["axes.grid"] = True

    plt.rcParams["grid.color"] = "gray"
    plt.rcParams["grid.linestyle"] = (1, (4, 9))
    
def plot_measure(x: np.ndarray, y: np.ndarray, dt: np.ndarray, 
                 label_x: str = None, label_y: str = None) -> tuple:
    """Quick measurement plotting."""
    
    fig, ax = plt.subplots(1, 2, figsize = (8, 3), tight_layout=True)
    
    ax[0].plot(x, y)
    ax[1].plot(x, dt)

    ax[0].set_xlabel(label_x)
    ax[1].set_xlabel(label_x)

    ax[0].set_ylabel(label_y)
    ax[1].set_ylabel("dt [s]")
    
    return fig, ax