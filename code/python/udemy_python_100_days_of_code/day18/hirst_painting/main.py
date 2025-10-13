#!/opt/homebrew/bin/python3
import colorgram
import turtle as t


def extract_colors(image, num_colors):
    # Extract 6 colors from an image.
    colors = colorgram.extract(image, num_colors)
    rgb_colors = [(_.rgb.r,_.rgb.g,_.rgb.b)  for _ in colors]
    return rgb_colors
    
    """
    usage example
    # colorgram.extract returns Color objects, which let you access
    # RGB, HSL, and what proportion of the image was that color.
    first_color = colors[0]
    rgb = first_color.rgb # e.g. (255, 151, 210)
    hsl = first_color.hsl # e.g. (230, 255, 203)
    proportion  = first_color.proportion # e.g. 0.34
    
    # RGB and HSL are named tuples, so values can be accessed as properties.
    # These all work just as well:
    red = rgb[0]
    red = rgb.r
    saturation = hsl[1]
    saturation = hsl.s
    """

def draw_circle(circle_size, circle_color, turtle_instance):
    print(f"Drawing a circle of color {circle_color}, at position {turtle_instance.pos()}")
    #turtle_instance.color((circle_color))
    turtle_instance.fillcolor(circle_color)
    turtle_instance.begin_fill()
    turtle_instance.circle(circle_size)
    turtle_instance.end_fill()

def get_next_color(colors):
    import random
    #i=0
    while True:
        yield random.choice(colors)
    #    color = colors[i%len(colors)]
    #    yield color 
    #    i+=1

def draw_hirst_image(image, rows=10, columns=10, space=50, dot_size=20  ):
    num_colors = 30
    colors = extract_colors(image, num_colors)[5:] #rgb tuples sorted by frequency in the original image. remove first three as they're likely to be background colors
    turt = t.Turtle()
    turt.speed("fastest")
    screen = t.Screen()
    screen.colormode(255) #required for color() to accept rgb range
    #turt.setworldcoordinates(-1, -1, 300, 300)

    startx, starty = -500, -500 #start at buttom left corner
    turt.penup()
    turt.goto(startx, starty)
    print(f"turtle position {turt.pos()}")
    #turt.pendown()
    color_generator= get_next_color(colors)

    for i in range(rows):
        for j in range(columns): 
            print(f"drawing row {i}, col {j}, position {turt.pos()}")
            draw_circle(dot_size, next(color_generator), turt)
            #turt.penup()
            turt.fd(space)
            #turt.pendown()
        #turt.penup()
        turt.goto(startx, starty+((i+1)*space))
        print(f"turtle went to {(startx+(i*space), starty)}  position {turt.pos()}")
        #turt.pendown()
    turt.ht()
    screen.exitonclick()
    

def main():
    image_path = 'https-hypebeast.com-image-2020-04-mschf-damien-hirst-severed-spots-project-000-e1588260357694-1200x720.jpg'
    #num_colors = 30
    #colors = extract_colors(image_path, num_colors)
    #print(colors)

    draw_hirst_image(image_path, 10, 10, 110, 20)

if __name__ == "__main__":
    main()
