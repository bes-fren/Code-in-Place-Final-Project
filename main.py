"""This took SO LONG!  Check it out though, isn't it kinda sick? :) 

I can kinda hear my computer screaming when I try to change a bunch of cells at once, so maybe this
could be optimized a bit haha.  At least it works!  

There was a lot of complicated list and dictionary stuff in here, complicated to me at least.  Take a 
look in the draw_grid and draw_palette functions to see me creating the dictionaries, look in click, 
grid_coordinates, color_cell, and change_active_color to see me refer to and write back to the 
dictionaties."""

from graphics import Canvas
import time

CELL_SIZE = 30
CELLS_PER_TILE = 10
TILES_PER_CANVAS_ROW = 2

PALETTE_WIDTH = CELLS_PER_TILE/2*CELL_SIZE
CANVAS_WIDTH = CELL_SIZE*CELLS_PER_TILE*TILES_PER_CANVAS_ROW+PALETTE_WIDTH
CANVAS_HEIGHT = CELL_SIZE*CELLS_PER_TILE*TILES_PER_CANVAS_ROW
TILE_SIZE = CELL_SIZE * CELLS_PER_TILE
COLORS = ["black","white","gray","silver","red","lime","blue","yellow","cyan","magenta","maroon","olive","green","purple","teal","navy"]


def main():

    global cell_index
    global colors_dict
    global active_color
    active_color = "black"
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.create_rectangle(0,0,CANVAS_WIDTH,CANVAS_HEIGHT,"cyan")


    draw_grid(canvas)
    selected_color_box = draw_palette(canvas)

    while True:
        #Gets integer coordinates for where you just clicked
        click = get_click_coordinates(canvas)

        #Looks up which cell that click happened in, if you actually did click on a cell
        grid_coordinates = click_select(canvas,click)

        #Changes the color of the relevant cell to the active color
        color_cell(canvas,grid_coordinates,active_color)

        #Changes the active color + moves selection box when a palette color is clicked
        change_active_color(canvas,selected_color_box,click)






    



#Creates full grid with an idea of how large each tile is
def draw_grid(canvas): 

    """This is a little complicated, isn't it?  All these for loops with all these
    crazy inputs?  I'll do my best to explain.  This is calculating where each cell's 
    left, top, right and bottom dimensions are. To do that though, we need to know where
    it is relative to our little grid. Like, what tile column is it in, what cell column
    is it in?  We need to know BOTH of those things to figure out where this guy goes.
    So... we've got 4 different for loops that will do that for us!  
    
    The bottom two for loops will draw a rows and columns of cells equal to the amount we 
    specify in CELLS_PER_TILE at the top - makes sense.  That gets us one tile, but 
    we need more than that!  We want a grid of multiple tiles that we can go through!
    So...  We need to also draw rows and columns of tables!  Let's look at the math below
    and walk through it to get an idea of what's actually going on."""

    #makes the cell index that will store the tile x & y and the cell x & y of each tile.
    global cell_index
    global colors_dict
    cell_index = {}
    
    for tile_column_num in range(TILES_PER_CANVAS_ROW):
        for tile_row_num in range(TILES_PER_CANVAS_ROW):
            for cell_column_num in range(CELLS_PER_TILE):
                for cell_row_num in range(CELLS_PER_TILE):
                    cell_left = (tile_column_num*TILE_SIZE)+(cell_column_num*CELL_SIZE)
                    cell_top = (tile_row_num*TILE_SIZE)+(cell_row_num*CELL_SIZE)
                    cell_right = (tile_column_num*TILE_SIZE)+(cell_column_num*CELL_SIZE)+CELL_SIZE
                    cell_bottom = (tile_row_num*TILE_SIZE)+(cell_row_num*CELL_SIZE)+CELL_SIZE
                    
                    #The actual guy whose color we'll be changing later
                    cell_obj = canvas.create_rectangle(
                        cell_left,
                        cell_top,
                        cell_right,
                        cell_bottom,
                        "white",
                        "grey")
                    
                    #The bounds of this cell stored in a list
                    cell_bounds = [cell_left,
                    cell_top,
                    cell_right,
                    cell_bottom]
                    
                    #This is the object we're going to be editing AND the bounds of the cell in 1 list.
                    cell = [cell_bounds,cell_obj]

                    #Assigning the relative grid coordinates as key and "cell" as the value.
                    cell_index[(tile_column_num,tile_row_num,cell_column_num,cell_row_num)] = cell
                    """If this works the way I think it will, by looking up the key, we can
                    choose to either pull back the bounds of the cell OR edit the actual cell object
                    depending on how we write our little reference.  
                    
                    I think we pretty much HAVE to do this if we want to keep the happy grid structure
                    we've got right now.  I needed a way to lookup the objects based on given canvas
                    coordinates, and I think this will allow that!
                    
                    Example for changing the top left square's color:
                    canvas.set_color(cell_index[(0,0,0,0)][1],"blue")

                    Example for returning the bounds of the top left square:
                    bounds = cell_index[(0,0,0,0)][0]

                    Example for pulling back the right boundary of the top left square (it's the third
                    index (which is 2) in the cell_bounds list):
                    right_boundary = cell_index[(0,0,0,0)][0][2]
                    """
                        
                       
            #Makes a border around each tile for visibilityj
            border = canvas.create_rectangle(
                (tile_column_num*TILE_SIZE),
                (tile_row_num*TILE_SIZE),
                (tile_column_num*TILE_SIZE)+TILE_SIZE,
                (tile_row_num*TILE_SIZE)+TILE_SIZE,
                "transparent",
                "black")





"""This function draws the palette and the color boxes on the righthand side. I might need
to make them editable later?  Honestly not super sure. I'm going to hope just creating them
will be enough and move on for now."""
def draw_palette(canvas):
    global colors_dict
    
    #Left edge of the palette.  Useful for reference later
    palette_left = CANVAS_WIDTH-PALETTE_WIDTH

    #The main palette window.  All the colors will be placed on top of this
    palette = canvas.create_rectangle(
        palette_left,
        0,
        CANVAS_WIDTH,
        CANVAS_HEIGHT,
        "white",
        "black"
    )

    #Need this because you can't get the width of a text object, so it needs to be specified directly.
    text_width = 50

    #This isn't used to create the text, but is useful as a marker for drawing the colors
    text_height = 40
    palette_text = canvas.create_text(

        #All these variables are specified so the palette text will always be centered.
        palette_left + ((PALETTE_WIDTH - text_width)/2),

        #I eyeballed this to make the the text centered. Shouldn't break if we change the constants...?      
        15,
        text = "palette",
        font = "courier")
    
    width = canvas.get_object_width(palette_text)
    print(width)

    #Some variables to make helpful references to later
    color_box_height = CELL_SIZE    
    color_box_width = CELL_SIZE*2
    color_window_top = text_height
    color_window_bottom = CANVAS_HEIGHT

    """The below few variables were created to center the color boxes in the palette.  It's designed
    this way to (try to) let you change how many colors are given in the list up at the top and still
    keep things centered and pretty.  There's not a ton of white space left though, so making the canvas
    too small will probably make things run together haha."""

    #How tall the color boxes will be when stacked on top of one another
    combined_color_box_height = len(COLORS) * color_box_height

    #How much space is leftover in the color window after making color boxes
    color_window_combined_white_space = color_window_bottom-color_window_top-combined_color_box_height

    #How much space between color boxes.  +1 at the end for the fencepost problem
    white_space_divider = color_window_combined_white_space / (len(COLORS) +1 )

    #This creates the color selection box. We'll return this at the end; this needs to be dynamic.
    selected_color_box = canvas.create_rectangle(
        palette_left + ((PALETTE_WIDTH - color_box_width) / 2) - 5,
        color_window_top + white_space_divider -5,
        palette_left + ((PALETTE_WIDTH - color_box_width) / 2) + color_box_width + 5,
        color_window_top + white_space_divider + color_box_height + 5,
        "yellow",
        "black")

    #Ugh, needed to make a dict after all.
    colors_dict = {}

    #This creates the color boxes
    for i in range(len(COLORS)):
        color_box_left = palette_left + ((PALETTE_WIDTH - color_box_width) / 2)
        color_box_top = color_window_top + white_space_divider + ((i * white_space_divider) + (i * color_box_height))
        color_box_right = palette_left + ((PALETTE_WIDTH - color_box_width) / 2) + color_box_width
        color_box_bottom =  color_window_top + white_space_divider + ((i * white_space_divider) + (i * color_box_height)) + color_box_height
        canvas.create_rectangle(
            color_box_left,
            color_box_top,
            color_box_right,
            color_box_bottom,
            COLORS[i],
            "black")

        #This makes a list of the coordinates of each box; that's assigned as the value, color as key.
        colors_dict[COLORS[i]] = [color_box_left,
            color_box_top,
            color_box_right,
            color_box_bottom,]
    
    return selected_color_box
        

"""This function waits for a click, gets the coordinates for that click, then returns those
values as a list.  There's probably a simpler way to do this, but I did a bit of gymnastics
to convert the wait_for_click output into a list of integers."""
def get_click_coordinates(canvas):
    canvas.wait_for_click()
    click = str(canvas.get_new_mouse_clicks())
    click = click.split(",")
    for i in range(len(click)):
        click[i] = float(click[i])
        click[i] = int(click[i])
    return click

#Checks to see what cell the values stored in click correspond to, if any
def click_select(canvas,click):
    global cell_index
    for key, value in cell_index.items():

        #Value set to 0 because that's the index where the coordinate info is stored
        bounds = value[0]

        #Buncha booleans! Sees if click falls within the bounds of any cell.
        #Ton of iteration here.  This is almost surely what's killing performance.  Oh well, whatever!
        if bounds[0] <= click[0] and bounds[2] >= click[0] and bounds[1] <= click[1] and bounds[3] >= click[1]:
            grid_coordinates = key
            return grid_coordinates

#This tiny guy is what actually changes the color of a cell.  Looks kind of innocuous, doesn't it? 
def color_cell(canvas,grid_coordinates,active_color):
    global cell_index
    try:
        #Set to 1 here since that's where the actual object at the given coordinates is stored.
        canvas.set_color(cell_index[grid_coordinates][1],active_color)
    except:
        pass

#This changes the active color if the coordinates in click fall within a palette color.  It also 
#moves the color selection box to whatever the active color is.
def change_active_color(canvas,selected_color_box,click):
    global colors_dict
    global active_color

    #Checks to see if the latest click falls within the bounds of any color box and, if so, sets the
    #active color to be the color of the box the user just clicked.
    for key, value in colors_dict.items():
        if click[0] > value[0] and click[0] < value[2] and click[1] > value[1] and click[1] < value[3]:
            active_color = key

    #This moves the selection box by looking up the coordinates associated with the active color.
    canvas.moveto(selected_color_box,
    colors_dict.get(active_color)[0]-5,
    colors_dict.get(active_color)[1]-5)



if __name__ == '__main__':
    main()