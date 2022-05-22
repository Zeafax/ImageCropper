import pygame as py
from PIL import Image
import os

py.init()

background_colour = (15,16,18)
(width, height) = (1000, 1000)
screen = py.display.set_mode((width, height))
py.display.set_caption('Image Cropper')
screen.fill(background_colour)
#py.display.flip()

imageArray = os.listdir("img")
imageIndex = 0
aspectX = 1
aspectY = 1

cropStartPoint = [0,0]
moveStartPoint = [0,0]
cropWidth = 0
cropHeight = 0
selectingCrop = False
movingCrop = False
game_font = py.font.Font("Roboto-Regular.ttf",60)


def setCurrentImage():
  global current_image_rect, current_image_surface, imageIndex
  try:
    path = os.path.join("img",imageArray[imageIndex])
    current_image_surface = py.image.load(path)
    
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

    current_image_surface = py.transform.scale(py.image.load(path).convert_alpha(), (imgWidth, imgHeight))

    current_image_rect = current_image_surface.get_rect(center = (500,500))


  except:
    print("No more Images")


def CropImage():
  global imageIndex
  imageCropStart = [cropStartPoint[0]-current_image_rect.left,cropStartPoint[1]-current_image_rect.top]
  imageCropEnd = [imageCropStart[0]+cropWidth, imageCropStart[1]+cropHeight]
  imageCropStart[0] = (imageCropStart[0]/current_image_surface.get_width())
  imageCropStart[1] = (imageCropStart[1]/current_image_surface.get_height())

  imageCropEnd[0] = (imageCropEnd[0]/current_image_surface.get_width())
  imageCropEnd[1] = (imageCropEnd[1]/current_image_surface.get_height())
  path = os.path.join("img",imageArray[imageIndex])
  img = Image.open(path)
  width,height = img.size

  left = round(width * imageCropStart[0])
  top = round (height *imageCropStart[1])
  right = round(width * imageCropEnd[0])
  bottom = round (width *imageCropEnd[1])
  if (aspectX == aspectY):
    bottom = top+(right-left)

  img1 = img.crop((left,top,right,bottom))
  savePath = ["out", f"{imageIndex}.jpg"]
  img1 = img1.save(os.path.join(*savePath))

  imageIndex +=1
  setCurrentImage()
  


def cropOutline():
  global cropHeight, cropWidth
  if selectingCrop:
    (posX,posY) = py.mouse.get_pos()
    cropWidth = posX-cropStartPoint[0]
    cropHeight =  posY-cropStartPoint[1]
    # take aspect ratio into account
    if cropWidth > cropHeight:
      aspect = aspectX/aspectY
      cropHeight = cropWidth*aspect
    else: 
      aspect = aspectY/aspectX
      cropWidth = cropHeight*aspect

    #py.mouse.set_pos([width+cropStartPoint[0],height+cropStartPoint[1]])



  if movingCrop:
    (posX,posY) = py.mouse.get_pos()
    cropStartPoint[0] += posX-moveStartPoint[0]
    cropStartPoint[1] += posY-moveStartPoint[1]
    #left
    if cropStartPoint[0] < current_image_rect.left:
      cropStartPoint[0] = current_image_rect.left
    #right  
    if cropStartPoint[0]> current_image_rect.right-cropWidth:
      cropStartPoint[0] = current_image_rect.right-cropWidth
    #top
    if cropStartPoint[1] < current_image_rect.top:
      cropStartPoint[1] = current_image_rect.top
    #bottom
    if cropStartPoint[1] > current_image_rect.bottom-cropHeight:
      cropStartPoint[1] = current_image_rect.bottom-cropHeight

    moveStartPoint[0] = posX
    moveStartPoint[1] = posY
  
  if cropStartPoint and cropWidth and cropHeight:
    # Change width and height if larger than imaqge
    if (cropStartPoint[0] + cropWidth > current_image_rect.right):
      cropWidth = current_image_rect.right -cropStartPoint[0]
      aspect = aspectX/aspectY
      cropHeight = cropWidth*aspect
    if (cropStartPoint[1] + cropHeight > current_image_rect.bottom):
      cropHeight = current_image_rect.bottom-cropStartPoint[1]
      aspect = aspectY/aspectX
      cropWidth = cropHeight*aspect

    
    py.draw.rect(screen, (255,0,0), py.Rect(cropStartPoint[0], cropStartPoint[1], cropWidth, cropHeight), 2)

w, h = py.display.get_surface().get_size()
running = True
lastType = 0;
setCurrentImage()
while running:
  screen.fill(background_colour)
  for event in py.event.get():  
    if event.type == py.QUIT:
      running = False
    if event.type == py.MOUSEBUTTONDOWN: 
      if (Crop_rect.collidepoint(event.pos)):
        CropImage()
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
      if (current_image_rect.collidepoint(event.pos)):
        if event.button == 1:
          cropStartPoint = [event.pos[0], event.pos[1]]
          selectingCrop = True
        if event.button == 3:
          moveStartPoint = [event.pos[0], event.pos[1]]
          movingCrop = True
        if event.button == 4:
          if cropWidth > cropHeight:
            cropWidth += 4
            aspect = aspectX/aspectY
            cropHeight = cropWidth*aspect
          else: 
            cropHeight += 4
            aspect = aspectY/aspectX
            cropWidth = cropHeight*aspect
        if event.button == 5:
          if cropWidth > cropHeight:
            cropWidth -= 4
            aspect = aspectX/aspectY
            cropHeight = cropWidth*aspect
          else: 
            cropHeight -= 4
            aspect = aspectY/aspectX
            cropWidth = cropHeight*aspect
        
        #current_image_rect.topleft
    if event.type == py.MOUSEBUTTONUP:
      if  selectingCrop and event.button == 1:
        selectingCrop = False
      if event.button == 3:
        movingCrop = False







  aspectX_surface = game_font.render(f"{int(aspectX)}x",True,(0,255,220))
  aspectX_rect = aspectX_surface.get_rect(center = ((w-aspectX_surface.get_width())/2,100))

  aspectY_surface = game_font.render(f"{int(aspectY)}",True,(0,255,220))
  aspectY_rect = aspectY_surface.get_rect(center = ((w+aspectY_surface.get_width())/2,100))

  Crop_surface = game_font.render("Crop Image",True,(0,255,220))
  Crop_rect = Crop_surface.get_rect(center = ((w+aspectY_surface.get_width())/2,h*0.9))

  screen.blit(aspectX_surface,aspectX_rect)
  screen.blit(aspectY_surface,aspectY_rect)
  screen.blit(Crop_surface,Crop_rect)
  screen.blit(current_image_surface,current_image_rect)
  cropOutline()

  py.display.update()
