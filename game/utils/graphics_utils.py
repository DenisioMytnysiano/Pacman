import time
import tkinter
import os.path


class GraphicsUtils:

    root_window = None
    canvas = None
    root_window_width = None
    root_window_height = None
    background_color = None
    got_release = None
    keys_down = {}
    keys_wait = {}

    @staticmethod
    def format_color(r, g, b):
        return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

    @staticmethod
    def color_to_vector(color):
        return list(map(lambda x: int(x, 16) / 256.0, [color[1:3], color[3:5], color[5:7]]))

    @staticmethod
    def sleep(secs):
        if GraphicsUtils.root_window is None:
            time.sleep(secs)
        else:
            GraphicsUtils.root_window.update_idletasks()
            GraphicsUtils.root_window.after(int(1000 * secs), GraphicsUtils.root_window.quit)
            GraphicsUtils.root_window.mainloop()

    @staticmethod
    def begin_graphics(width, height, color, title=None):
        if GraphicsUtils.root_window is not None:
            GraphicsUtils.root_window.destroy()

        GraphicsUtils.root_window_width, GraphicsUtils.root_window_height = width - 1, height - 1
        GraphicsUtils.background_color = color

        root_window = tkinter.Tk()
        root_window.title(title)
        root_window.resizable(0, 0)
        GraphicsUtils.root_window = root_window
        try:
            GraphicsUtils.canvas = tkinter.Canvas(root_window, width=width, height=height)
            GraphicsUtils.canvas.pack()
            GraphicsUtils.draw_background()
            GraphicsUtils.canvas.update()
        except Exception:
            GraphicsUtils.root_window = None
            raise

        GraphicsUtils.root_window.bind("<KeyPress>", GraphicsUtils.__keypress)
        GraphicsUtils.root_window.bind("<KeyRelease>", GraphicsUtils.__keyrelease)
        GraphicsUtils.root_window.protocol("WM_DELETE_WINDOW", exit)
        GraphicsUtils.__clear_keys()

    @staticmethod
    def end_graphics() -> None:
        GraphicsUtils.root_window.destroy()
        GraphicsUtils.root_window = None
        GraphicsUtils.canvas = None
        GraphicsUtils.mouse_enabled = 0
        GraphicsUtils.__clear_keys()

    @staticmethod
    def draw_background():
        corners = [
            (0, 0),
            (0, GraphicsUtils.root_window_height),
            (GraphicsUtils.root_window_width, GraphicsUtils.root_window_height),
            (GraphicsUtils.root_window_width, 0)
        ]
        GraphicsUtils.polygon(
            corners, GraphicsUtils.background_color,
            fill_color=GraphicsUtils.background_color,
            filled=True, smoothed=False
        )

    @staticmethod
    def polygon(coords, outline_color, fill_color=None, filled=1, smoothed=1, behind=0, width=1):
        if fill_color is None:
            fill_color = outline_color
        if filled == 0:
            fill_color = ""
        poly = GraphicsUtils.canvas.create_polygon(coords, outline=outline_color, fill=fill_color, smooth=smoothed,
                                                   width=width)
        if behind > 0:
            GraphicsUtils.canvas.tag_lower(poly, behind)
        return poly

    @staticmethod
    def square(pos, r, color, filled=1, behind=0):
        x, y = pos
        coords = [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]
        return GraphicsUtils.polygon(coords, color, color, filled, 0, behind=behind)

    @staticmethod
    def circle(pos, r, outline_color, fill_color=None, endpoints=None, style='pieslice', width=2):
        x, y = pos
        x0, x1 = x - r - 1, x + r
        y0, y1 = y - r - 1, y + r
        if endpoints is None:
            e = [0, 359]
        else:
            e = list(endpoints)
        while e[0] > e[1]:
            e[1] += 360

        return GraphicsUtils.canvas.create_arc(x0, y0, x1, y1, outline=outline_color, fill=fill_color or outline_color,
                                               extent=e[1] - e[0], start=e[0], style=style, width=width)

    @staticmethod
    def refresh():
        GraphicsUtils.canvas.update_idletasks()

    @staticmethod
    def keys_pressed():
        if GraphicsUtils.got_release:
            GraphicsUtils.root_window.dooneevent(tkinter._tkinter.DONT_WAIT)
        return GraphicsUtils.keys_down.keys()

    @staticmethod
    def keys_waiting() -> dict:
        keys = GraphicsUtils.keys_wait.keys()
        GraphicsUtils.keys_wait = {}
        return keys

    @staticmethod
    def wait_for_keys():
        keys = []
        while not keys:
            keys = GraphicsUtils.keys_pressed()
            GraphicsUtils.sleep(0.05)
        return keys

    @staticmethod
    def remove_from_screen(x):
        GraphicsUtils.canvas.delete(x)
        GraphicsUtils.root_window.dooneevent(tkinter._tkinter.DONT_WAIT)

    @staticmethod
    def move_to(object, x, y=None):
        if y is None:
            try:
                x, y = x
            except Exception:
                print('Incomprehensible coordinates')

        horiz = True
        new_coords = []
        current_x, current_y = GraphicsUtils.canvas.coords(object)[0:2]
        for coord in GraphicsUtils.canvas.coords(object):
            if horiz:
                inc = x - current_x
            else:
                inc = y - current_y
            horiz = not horiz
            new_coords.append(coord + inc)
        GraphicsUtils.canvas.coords(object, *new_coords)
        GraphicsUtils.root_window.dooneevent(tkinter._tkinter.DONT_WAIT)

    @staticmethod
    def move_by(object, x, y=None, lift=False):
        if y is None:
            try:
                x, y = x
            except Exception:
                print('Incomprehensible coordinates')

        horiz = True
        new_coords = []
        for coord in GraphicsUtils.canvas.coords(object):
            if horiz:
                inc = x
            else:
                inc = y
            horiz = not horiz

            new_coords.append(coord + inc)

        GraphicsUtils.canvas.coords(object, *new_coords)
        GraphicsUtils.root_window.dooneevent(tkinter._tkinter.DONT_WAIT)
        if lift:
            GraphicsUtils.canvas.tag_raise(object)

    @staticmethod
    def move_circle(id, pos, r, endpoints=None):
        x, y = pos
        x0, x1 = x - r - 1, x + r
        y0, y1 = y - r - 1, y + r
        if endpoints is None:
            e = [0, 359]
        else:
            e = list(endpoints)
        while e[0] > e[1]:
            e[1] = e[1] + 360

        if os.path.isfile('flag'):
            GraphicsUtils.edit(id, ('extent', e[1] - e[0]))
        else:
            GraphicsUtils.edit(id, ('start', e[0]), ('extent', e[1] - e[0]))
        GraphicsUtils.move_to(id, x0, y0)

    @staticmethod
    def edit(id, *args):
        GraphicsUtils.canvas.itemconfigure(id, **dict(args))

    @staticmethod
    def text(pos, color, contents, font='Helvetica', size=12, style='normal', anchor="nw") -> object:
        x, y = pos
        font = (font, str(size), style)
        return GraphicsUtils.canvas.create_text(x, y, fill=color, text=contents, font=font, anchor=anchor)

    @staticmethod
    def change_text(id, newText, font=None, size=12, style='normal'):
        GraphicsUtils.canvas.itemconfigure(id, text=newText)
        if font is not None:
            GraphicsUtils.canvas.itemconfigure(id, font=(font, '-%d' % size, style))

    @staticmethod
    def change_color(id, new_color):
        GraphicsUtils.canvas.itemconfigure(id, fill=new_color)

    @staticmethod
    def line(here, there, color, width=2):
        x0, y0, x1, y1 = here[0], here[1], there[0], there[1]
        return GraphicsUtils.canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    @staticmethod
    def __keypress(event):
        GraphicsUtils.keys_down[event.keysym] = 1
        GraphicsUtils.keys_wait[event.keysym] = 1
        GraphicsUtils.got_release = None

    @staticmethod
    def __keyrelease(event):
        try:
            del GraphicsUtils.keys_down[event.keysym]
        except Exception:
            pass
        GraphicsUtils.got_release = 1

    @staticmethod
    def __clear_keys():
        GraphicsUtils.keys_down = {}
        GraphicsUtils.keys_wait = {}
        GraphicsUtils.got_release = None
