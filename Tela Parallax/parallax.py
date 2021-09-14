#32091982 - Jhonatan Felipe

import pygame

class _subsurface(object):
    #Classe de contêiner para subsuperfície

    def __init__(self, surface, factor):
        self.scroll = 0
        self.factor = factor
        self.surface = surface

class ParallaxSurface(object):
    #Classe de rolagem de paralaxe que suporta uma série de superficies
    def __init__(self, size, colorkey_flags=0):
        self.colorkey_flags = colorkey_flags
        self.scroller = 0
        self.levels = []
        self.levels_id = {}
        self.size = size
        self.orientation = 'horizontal'

    def chg_size(self, size):
        # Altera o tamanho da superfície paralaxe.
        self.size = size

    def update(self, image_path, scroll_factor, size=(0, 0)):
        #Atualiza o nível do paralaxe identificado pelo atributo image_path e
        #redefine o scroll_factor (atributo) da camada e o tamanho de toda a
        #superfície de paralaxe.

        self.rem(image_path)
        self.add(image_path, scroll_factor, size)

    def rem(self, image_path):

        #Remove o nível de paralaxe criado a partir de image_path.
        #Se nenhum nível correspondente for encontrado, nada será removido.

        if image_path in self.levels_id:
            elem_id = self.levels_id[image_path]
            del self.levels[elem_id]
            del self.levels_id[image_path]

    def add(self, image_path, scroll_factor, size=None):
        #Adiciona um nível de paralaxe, o primeiro nível adicionado é o
        #nível mais profundo, ou seja, o mais longe possível na "tela.

            
        #image_path é o caminho para a imagem a ser usada
        #scroll_factor é o fator de desaceleração para este nível de paralaxe.

        try:
            image = (pygame.image.load(image_path))
        except:
            message = "couldn't open image:" + image_path
            raise SystemExit(message)
        if ".png" in image_path:
            image = image.convert_alpha()
        else:
            image = image.convert()
        if len(self.levels) > 0:
            image.set_colorkey((0xff, 0x00, 0xea), self.colorkey_flags)
        if size is not None:
            image = pygame.transform.scale(image, size) # Alterar o tamanho da imagem

            self.chg_size(size) # Atualize o tamanho

        # Pegando a imagem atual por seu id

        self.levels_id[image_path] = len(self.levels)
        self.levels.append(_subsurface(image, scroll_factor))

    def add_colorkeyed_surface(self, surface, scroll_factor,
                               color_key=(0xff, 0x00, 0xea)):
        #Adiciona uma superfície colorida criada em ponto da aplicação.

        surface = surface.convert()
        if len(self.levels) > 0:
            surface.set_colorkey(color_key, self.colorkey_flags)
        self.levels.append(_subsurface(surface, scroll_factor))

    def add_surface(self, surface, scroll_factor):
        # Adiciona uma superfície criada em outro lugar.
        
        surface = surface.convert_alpha()
        if len(self.levels) > 0:
            surface.set_colorkey((0xff, 0x00, 0xea), self.colorkey_flags)
        self.levels.append(_subsurface(surface, scroll_factor))

    def draw(self, surface):
        #Isso atrai todos os níveis de paralaxe para a superfície
        #fornecido como argumento.

        s_width = self.size[0]
        s_height = self.size[1]
        for lvl in self.levels:
            if self.orientation == 'vertical':
                surface.blit(lvl.surface, (0, 0),
                             (0, -lvl.scroll, s_width, s_height))
                surface.blit(lvl.surface,
                             (0, lvl.scroll - lvl.surface.get_height()))
            else:
                surface.blit(lvl.surface, (0, 0),
                             (lvl.scroll, 0, s_width, s_height))
                surface.blit(lvl.surface,
                             (lvl.surface.get_width() - lvl.scroll, 0),
                             (0, 0, lvl.scroll, s_height))

    def scroll(self, offset, orientation=None):
        #scroll move cada superfície _offset_ pixels / fator atribuído
        if orientation is not None:
            self.orientation = orientation

        self.scroller = (self.scroller + offset)
        for lvl in self.levels:
            if self.orientation == 'vertical':
                lvl.scroll = (self.scroller / lvl.factor) \
                             % lvl.surface.get_height()
            else:
                lvl.scroll = (self.scroller / lvl.factor) \
                             % lvl.surface.get_width()

class VerticalParallaxSurface(ParallaxSurface):
    #Classe implementando superfície de paralaxe de rolagem vertical

    def __init__(self, size, colorkey_flags=0):
        ParallaxSurface.__init__(self, size, colorkey_flags)
        self.orientation = 'vertical'
