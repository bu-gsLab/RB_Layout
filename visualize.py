import pygame
import numpy as np

W, H = 1600, 900
RB_COL = (180, 210, 240)
PB_COL = (210, 240, 185)
BG = (255, 255, 255)

def show(rows, row_index):
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    font = pygame.font.SysFont("monospace", 12)
    clock = pygame.time.Clock()
    idx = 0

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT:
                    idx = (idx + 1) % len(rows)
                if ev.key == pygame.K_LEFT:
                    idx = (idx - 1) % len(rows)

        screen.fill(BG)
        row = rows[idx]
        mods = row.modules
        x_off = W / 12
        #scale = (W - x_off) / (sum(m.RB_long for m in mods))
        scale = W / (row.R * 1.2)

        total_rb_width = sum(m.RB.total_long for m in mods) * scale
        x = W - x_off - total_rb_width
        y = H / 2 + 100

        R = row.R * scale
        rb_keepout_x = x - (row.rb_distance * scale)
        pb_keepout_x = x + (mods[::-1][0].RB_long - mods[::-1][0].PB_long) * scale - (row.pb_distance * scale)

        if row_index <= 12:
            rb_keepout_y = y
            pb_keepout_y = y - (mods[::-1][0].RB_PB_short - mods[::-1][0].RB_short) * scale
        else:
            rb_keepout_y = y + mods[::-1][0].RB_short * scale
            pb_keepout_y = y


        p1 = np.array([rb_keepout_x, rb_keepout_y])
        p2 = np.array([pb_keepout_x, pb_keepout_y])
        d = np.linalg.norm(p2 - p1)

        mid = (p1 + p2) / 2
        h = np.sqrt(R**2 - (d/2)**2)

        perp = np.array([-(p2 - p1)[1], (p2 - p1)[0]]) / d
        center1 = mid + h * perp
        center2 = mid - h * perp
        if row_index <= 12:
            center = center1 if center1[1] > center2[1] else center2
        else:
            center = center1 if center1[1] < center2[1] else center2
        cx, cy = center


        for m in mods[::-1]:
            rw = m.RB.total_long * scale
            rh = m.RB.total_short * scale
            pw = m.PB.total_long * scale
            ph = m.PB.total_short * scale
            pygame.draw.rect(screen, RB_COL, (x, y, rw, rh))
            pygame.draw.rect(screen, PB_COL, (x + (rw - pw), y - ph, pw, ph))
            pygame.draw.rect(screen, (0,0,0), (x, y, rw, rh), 1)
            pygame.draw.rect(screen, (0,0,0), (x + (rw - pw), y - ph, pw, ph), 1)
            lbl = font.render(m.label, True, (30, 30, 30))
            screen.blit(lbl, lbl.get_rect(center=(x + rw/2, y + rh/2)))
            x += rw

        info = f"{idx+1}/{len(rows)}  {row}"
        screen.blit(font.render(info, True, (80, 80, 80)), (20, 10))
        pygame.draw.circle(screen, (255, 0, 0), (cx, cy), R, 2)
        pygame.display.flip()
        clock.tick(60)