import pygame

class Slider:
    def __init__(self,x,y,w,h,min_val, max_val, start_val, label) -> None:
        self.rect = pygame.Rect(x,y,w,h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.label = label
        self.knob = pygame.Rect(x + (start_val - min_val) / (max_val - min_val) * w, y, 10, h)
        self.active = False
    
    def is_over(self, pos):
        return self.knob.collidepoint(pos) or self.rect.collidepoint(pos)

    def draw(self, screen):
        # draw slider
        pygame.draw.rect(screen, (255,255,255), self.rect, 1)
        pygame.draw.rect(screen, (0,255,0), self.knob)
        font = pygame.font.SysFont('Arial', 16)
        text_surf = font.render(f'{self.label}: {self.val:.3f}', True, (255,255,255))
        screen.blit(text_surf, (self.rect.x + self.rect.width +10, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_over(event.pos):
            self.active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active = False
        elif event.type == pygame.MOUSEMOTION and self.active:
            self.knob.x = min(max(event.pos[0], self.rect.x), self.rect.x + self.rect.width) #min of the length of slider and either mouse position or slider min
            self.val = self.min_val + (self.knob.x - self.rect.x) / (self.rect.width) * (self.max_val - self.min_val)
            return True
        return False
