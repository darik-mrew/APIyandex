import pygame
import requests
import sys
import os


class MapParams(object):
    def __init__(self):
        self.lt = 59.939820
        self.ln = 30.314383
        self.zoom = 17
        self.type = "map"

    def ll(self):
        return str(self.ln) + "," + str(self.lt)


def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("HTTP статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                mp.zoom -= 1
                if mp.zoom < 1:
                    mp.zoom = 1
            elif event.key == pygame.K_PAGEUP:
                mp.zoom += 1
                if mp.zoom > 19:
                    mp.zoom = 19
            elif event.key == pygame.K_UP:
                mp.lt += 0.001
                if mp.lt > 90:
                    mp.lt = 90
            elif event.key == pygame.K_DOWN:
                mp.lt -= 0.001
                if mp.lt < -90:
                    mp.lt = -90
            elif event.key == pygame.K_RIGHT:
                mp.ln += 0.001
                if mp.ln > 180:
                    mp.ln = 180
            elif event.key == pygame.K_LEFT:
                mp.ln -= 0.001
                if mp.ln < -180:
                    mp.ln = -180
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()