import pygame as pg

pg.init()

# ink display is 250x122
win = pg.display.set_mode(size=(1280, 720), flags=pg.RESIZABLE)
pg.display.set_caption('Super Inky Sender')

# setup
canvasSize = 1, 1
font = pg.font.SysFont('Consolas', 24)
butText = font.render('SEND', True, (169, 169, 169))
winSize = win.get_size()
start = 0, 0
pixels = []
run = True

while run:
    leftClick = False
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.VIDEORESIZE:
            # resize all coordinate stuff
            win = pg.display.set_mode(size=(event.w if event.w > 300 else 300, event.h if event.h > 200 else 200), flags=pg.RESIZABLE)
            oldCanvasSize = canvasSize
            winSize = event.w, event.h
            if winSize[0] < winSize[1]*250/122:
                canvasSize = winSize[0]*3//4, winSize[0]*3*122//4//250
            else:
                canvasSize = winSize[1]*3*250//4//122, winSize[1]*3//4
            pixels = [(i*canvasSize[0]//oldCanvasSize[0], j*canvasSize[1]//oldCanvasSize[1]) for i,j in pixels]
        elif event.type == pg.MOUSEBUTTONDOWN:
            start = mousePos
        elif event.type == pg.MOUSEBUTTONUP and mousePos == start:
            leftClick = True

    win.fill((169, 169, 169))

    # grab key and mouse presses
    keys = pg.key.get_pressed()
    mouseButtons = pg.mouse.get_pressed()
    mousePos = pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]

    
    if winSize[0] < winSize[1]*250/122:
        canvasSize = winSize[0]*3//4, winSize[0]*3*122//4//250
    else:
        canvasSize = winSize[1]*3*250//4//122, winSize[1]*3//4
    canvas = pg.draw.rect(win, (255, 255, 255), (winSize[0]//2-winSize[0]*3//8, winSize[1]//2-winSize[1]*3//8,*canvasSize))

    if canvas.collidepoint(mousePos) and mouseButtons[0]:
        pixels.append((((mousePos[0]-canvas[0])*250//canvas[2])*canvas[2]//250+canvas[2]//500, ((mousePos[1]-canvas[1])*250//canvas[2])*canvas[2]//250+canvas[2]//500))
    
    if len(pixels) > 2:
        pg.draw.lines(win, (0, 0, 0), False, [(canvas[0]+i, canvas[1]+j) for i,j in pixels], canvas[2]//250)
    elif len(pixels) > 0:
        pg.draw.rect(win, (0, 0, 0), pixels[0] + (canvas[2]//250, canvas[2]//250))

    sendBut = pg.draw.rect(win, (30, 30, 30), (winSize[0] - 100, 50, 60, 30))
    win.blit(butText, (sendBut[0], sendBut[1]))
    if sendBut.collidepoint(mousePos) and leftClick:
        print('SENDING...')

    pg.display.update()

pg.quit()