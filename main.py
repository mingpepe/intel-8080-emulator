import pygame

from i8080 import I8080Chip

FILE_PATH = 'rom//invaders'
RAM_SIZE = 0x10000

CYCLE_PER_SEC = 2 * 1000 * 1000  # 2M
FPS = 60
CYCLE_PER_FRAME = CYCLE_PER_SEC // FPS
CYCLE_PER_HALF_FRAME = CYCLE_PER_FRAME // 2
DRAW_PER_N_FRMAE = 5

BLACK = (0, 0, 0)
WHITE = (0xff, 0xff, 0xff)


def key_event_handler(chip):
    mapping = {
        pygame.K_LEFT: I8080Chip.LEFT_KEY,
        pygame.K_RIGHT: I8080Chip.RIGHT_KEY,
        pygame.K_c: I8080Chip.COIN_KEY,
        pygame.K_SPACE: I8080Chip.SHOOT_KEY,
        pygame.K_1: I8080Chip.D1_KEY,
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key in mapping:
                chip.key_down(mapping[event.key])
        if event.type == pygame.KEYUP:
            if event.key in mapping:
                chip.key_up(mapping[event.key])


def run_cycle(chip, cycle_count):
    cycle = 0
    while cycle < cycle_count:
        cycle += chip.step_run()


def main():
    with open(FILE_PATH, 'rb') as f:
        rom = f.read()

    memory = bytearray(RAM_SIZE)
    memory[:len(rom)] = rom

    chip = I8080Chip(memory)

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(
        (I8080Chip.SCREEN_WIDTH, I8080Chip.SCREEN_HEIGHT))

    frame_count = 0

    while True:
        key_event_handler(chip)

        run_cycle(chip, CYCLE_PER_HALF_FRAME)
        chip.trigger_interrupt(1)
        run_cycle(chip, CYCLE_PER_HALF_FRAME)
        chip.trigger_interrupt(2)

        frame_count += 1
        if frame_count == DRAW_PER_N_FRMAE:
            chip.convert()
            screen.fill(BLACK)
            for i in range(I8080Chip.SCREEN_HEIGHT):
                for j in range(I8080Chip.SCREEN_WIDTH):
                    if chip.screen(i * I8080Chip.SCREEN_WIDTH + j):
                        screen.set_at((j, i), WHITE)
            pygame.display.flip()
            clock.tick(60)
            frame_count = 0


if __name__ == '__main__':
    main()
