import pygame_menu

def harry():

    myimage = pygame_menu.baseimage.BaseImage(
        image_path = './imagenes/caliz.jpg',
        drawing_mode = pygame_menu.baseimage.IMAGE_MODE_FILL,
    )

    Theme = pygame_menu.themes.Theme
    harry = Theme(background_color = myimage,
                    title_background_color = (102, 0, 0),
                    title_font = pygame_menu.font.FONT_NEVIS,
                    title_font_color = (255, 255, 255),
                    title_font_size = 67,
                    cursor_selection_color = (224, 156, 9),
                    selection_color = (224, 156, 9),
                    widget_font = pygame_menu.font.FONT_NEVIS,
                    widget_alignment = pygame_menu.locals.ALIGN_CENTER,
                    widget_font_color=(255, 255, 255),
                    widget_background_color=(102, 0, 0),
                    widget_padding = (10,20),
                    widget_margin = (0,20))

    return harry
