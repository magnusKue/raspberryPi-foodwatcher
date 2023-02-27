import pygame 

def roundSurface(inSurf, roundness):
	size = inSurf.get_size()
	mask = pygame.Surface(size, pygame.SRCALPHA)
	pygame.draw.rect(mask, (255, 255, 255), (0, 0, *size), border_radius=roundness)
	image = inSurf.copy().convert_alpha()
	image.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MIN)
	return image