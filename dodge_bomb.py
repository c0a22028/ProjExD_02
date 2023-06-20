import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1000, 600
#キーごとの移動量の辞書
delta = {  
    pg.K_UP:[0, -5],
    pg.K_DOWN:[0, 5],
    pg.K_LEFT:[-5, 0],
    pg.K_RIGHT:[5, 0]
}


def check_bound(rect: pg.Rect):
    """
    こうかとんRect、爆弾Rectが画面外か画面内かを判定する関数
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向、縦方向の判定結果タプル(True：画面内／False：画面内)
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  #横宝庫の判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  #縦方向の判定
        tate = False
    return (yoko, tate)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    bd_img = pg.Surface((20, 20))  #練習
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_img.set_colorkey((0, 0, 0))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    vx = +5
    vy = +5
    #爆弾Surface(bg_img)から爆弾Rect(bg_rct)を抽出する
    bd_rct = bd_img.get_rect()
    #爆弾rect(bg_rct)の中心座標を乱数で指定する
    bd_rct.center = x, y


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, mv in delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
                kk_rct.move_ip(sum_mv)

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        screen.blit(bd_img, bd_rct)
        bd_rct.move_ip(vx, vy)
        #こうかとんを更新前の位置に戻す
        if not check_bound(kk_rct)[0]:
            kk_rct.move_ip(-sum_mv[0], 0)
        if not check_bound(kk_rct)[1]:
            kk_rct.move_ip(0, -sum_mv[1])
        #爆弾が画面外の場合、速度の符号を反転させる
        if not check_bound(bd_rct)[0]:
            vx *= -1
        if not check_bound(bd_rct)[1]:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()