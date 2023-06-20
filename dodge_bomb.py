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
    #左向きのこうかとん
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_left = pg.transform.rotozoom(kk_img, 0, 1.0)
    #右
    kk_img_right = pg.transform.flip(kk_img_left, 1, 0)  
    #左上
    kk_img_upper_left = pg.transform.rotozoom(kk_img_left, 315, 1.0)
    #上  
    kk_img_upper = pg.transform.rotozoom(kk_img_right, 90, 1.0)  
    #右上
    kk_img_upper_right = pg.transform.rotozoom(kk_img_right, 45, 1.0)  
    #右下
    kk_img_lower_right = pg.transform.rotozoom(kk_img_right, 315, 1.0) 
     #下 
    kk_img_lower = pg.transform.rotozoom(kk_img_right, 270, 1.0)
     #左下 
    kk_img_lower_left = pg.transform.rotozoom(kk_img_left, 45, 1.0) 
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_imgs = []  
    #いろいろな大きさの爆弾をリストに格納
    for r in range(1, 11):
        bd_img = pg.Surface((20*r, 20*r))  
        pg.draw.circle(bd_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bd_img.set_colorkey((0, 0, 0))
        bd_imgs.append(bd_img)
    bd_img = bd_imgs[0]
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    vx = +5
    vy = +5
    #爆弾Surface(bg_img)から爆弾Rect(bg_rct)を抽出する
    bd_rct = bd_img.get_rect()
    #爆弾rect(bg_rct)の中心座標を乱数で指定する
    bd_rct.center = x, y

    kk_zisyo = {(-5, 0): kk_img_left, (-5, -5): kk_img_upper_left, 
                (0, -5): kk_img_upper, (5, -5): kk_img_upper_right, 
                (5, 0): kk_img_right, (5, 5): kk_img_lower_right,
                (0, 5): kk_img_lower, (-5, 5): kk_img_lower_left} 


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  #合計移動量
        for k, mv in delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)

        screen.blit(bg_img, [0, 0])
        #移動方向に応じてこうかとんの向きも変える
        for tup in kk_zisyo.keys():
            if list(tup) == sum_mv:
                screen.blit(kk_zisyo[tup], kk_rct)
            elif sum_mv == [0, 0]:
                screen.blit(kk_img, kk_rct)
        #こうかとんを更新前の位置に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        #時間に合わせて爆弾の大きさを変える
        for i, img in enumerate(bd_imgs):
            tm = 100  #爆弾の大きさが変わる時間の単位
            bd_img = img
            if i < 1:
                if tmr <= tm*(i+1):
                    screen.blit(bd_img, bd_rct)
            elif i == len(bd_imgs)-1:
                if tm*(i-1) <= tmr:
                    screen.blit(bd_img, bd_rct)
            else:
                if tm*(i-1) < tmr and tmr <= tm*(i+1):
                    screen.blit(bd_img, bd_rct)
        #爆弾が画面外の場合、速度の符号を反転させる
        bd_rct.move_ip(vx,vy)
        if not check_bound(bd_rct)[0]:
            vx *= -1
        if not check_bound(bd_rct)[1]:
            vy *= -1

        if kk_rct.colliderect(bd_rct):
            print("ゲームオーバー")
            return

        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()