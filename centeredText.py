import pygame.display as pygdisp

class selfcenteredText:

    def __init__(self,font, text:str, rect_top_left:list, rect_size:int):
        self.font = font
        self.text = text
        self.top_left = rect_top_left
        self.size = rect_size

    def draw(self, display,colour:list):
        x = (self.top_left[0] + (self.size - self.font.size(self.text)[0])//2)
        y = (self.top_left[1] + (self.size - self.font.size(self.text)[1]) // 2)
        display.blit(self.font.render(self.text,True,colour),(x,y))
