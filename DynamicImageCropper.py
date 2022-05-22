import pygame as py

py.init()

background_colour = (15,16,18)
#background_colour = (255,255,255)
(width, height) = (1000, 1000)
screen = py.display.set_mode((width, height))
py.display.set_caption('Image Cropper')
screen.fill(background_colour)
py.display.flip()

number = 10 
aspectX = 1
aspectY = 1
game_font = py.font.Font("Roboto-Regular.ttf",60)

current_image_surface = py.image.load("img/2.jpg")

(imgWidth,imgHeight) = current_image_surface.get_size()

if (imgWidth < imgHeight):
  #imgHeight = max with
  ratio = imgWidth/imgHeight
  imgHeight = 800;
  imgWidth = imgHeight*ratio
else: 
  ratio = imgHeight/imgWidth
  imgWidth = 800;
  imgHeight = imgWidth*ratio

current_image_surface = py.transform.scale(py.image.load("img/2.jpg").convert_alpha(), (imgWidth, imgHeight))

current_image_rect = current_image_surface.get_rect(center = (500,500))


w, h = py.display.get_surface().get_size()
running = True
while running:
  screen.fill(background_colour)
  for event in py.event.get():
    if event.type == py.QUIT:
      running = False
    if event.type == py.MOUSEBUTTONDOWN: 
      if  (aspectX_rect.collidepoint(event.pos)):
        if (event.button == 1):
          aspectX+=1
        if (event.button == 3 and aspectX > 1):
          aspectX-=1
      if  (aspectY_rect.collidepoint(event.pos)):
        if (event.button == 1):
          aspectY+=1
        if (event.button == 3 and aspectY > 1):
          aspectY-=1




  aspectX_surface = game_font.render(f"{int(aspectX)},",True,(0,255,220))
  aspectX_rect = aspectX_surface.get_rect(center = ((w-aspectX_surface.get_width())/2,100))

  aspectY_surface = game_font.render(f"{int(aspectY)}",True,(0,255,220))
  aspectY_rect = aspectY_surface.get_rect(center = ((w+aspectY_surface.get_width())/2,100))

 
  screen.blit(aspectX_surface,aspectX_rect)
  screen.blit(aspectY_surface,aspectY_rect)
  screen.blit(current_image_surface,current_image_rect)

  py.display.update()
