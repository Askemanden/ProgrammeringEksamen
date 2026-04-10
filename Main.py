import WindowPartitioner
import pygame as PYMfkas

PYMfkas.surface

if __name__ == "__main__":
    screen = PYMfkas.display.set_mode((800, 500), PYMfkas.RESIZABLE)
    PYMfkas.display.set_caption("Tingeling")
    running = True
    while running:
        for event in PYMfkas.event.get():
            if event.type == PYMfkas.QUIT:
                running = False

            elif event.type == PYMfkas.VIDEORESIZE:
                # Update screen size when resized
                screen = PYMfkas.display.set_mode((event.w, event.h), PYMfkas.RESIZABLE)
            
            #elif spiller-klasse

    PYMfkas.quit()