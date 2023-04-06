import pyautogui
import cv2
import numpy as np


# 匹配精确图像用
def match_exact_image(cvtarget, space, confidence=0.9):
    # 宽高
    w, h = cvtarget.shape[::-1]
    
    # 使用模板匹配方法寻找图像
    res = cv2.matchTemplate(space, cvtarget, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= confidence)
    
    # 返回所有可能的左上角坐标的列表，可能多个也可能为空
    # TODO: 只取一个就行
    return list(zip(*loc[::-1])), w, h

def get_screenshot():
    # 获取屏幕截图
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    return screenshot

def find_image_center_scaled(target, confidence=0.9, attempt_time=5, s_steps=0.1):
    # TODO: 检查 step 和 attempt会不会越过 0（非法）
    space = get_screenshot()
    
    coords = []
    w, h= 0, 0
    scale = 0
    resized_target = cv2.imread(target, cv2.IMREAD_GRAYSCALE)
    
    while attempt_time > 0:
        coords, w, h = match_exact_image(resized_target, space, confidence)
        if not coords:
            # 准备 scale
            old_scale = scale
            if scale < 0:
                scale -= 0.1
                attempt_time -= 1
            scale = -scale
            if scale == 0:
                scale += 0.1
            if attempt_time > 0:
                print(f"{target} 在{1+old_scale}x 下匹配失败, 尝试缩放后再次搜索：{1+scale}x")
            # 缩放target
            resized_target = cv2.resize(resized_target, None, fx=1+scale, fy=1+scale)
        else:
            break
    if not coords:
        print(f"{target} 在{1+old_scale}x 下匹配失败")
        print(f"{target}未找到")
        center_point = (-1,-1)
        return center_point
    x, y = coords[0]
    if scale == 0:
        print(f"{target} 已找到：({x}, {y}) ")
    else:
        print(f"{target} 已找到：({x}, {y}) （在 {1+scale}x 尺度下）")
            
    center_point = (x + w // 2, y + h // 2)
                
                
            
    return center_point

def act1(x, y):
    
    # 将鼠标移动到找到的图像位置
    pyautogui.moveTo(x, y)

    # 操作
    pyautogui.click()
    # pyautogui.typewrite('Hello, World!')
    

def main():
    image_path = 'target/button1.png'
    coord = find_image_center_scaled(image_path)
    if coord !=(-1,-1):
        act1(*coord)
    else:
        pass
    # coordinates = find_image_on_screen(image_path)

    # if coordinates:
    #     x, y = coordinates[0]
    #     print(coordinates)
    #     print(f"图像在屏幕上的坐标: {x}, {y}")
        
    #     # 将鼠标移动到找到的图像位置
    #     pyautogui.moveTo(x, y)

    #     # 执行操作
    #     perform_actions()
    # else:
    #     print("未找到匹配的图像")

if __name__ == '__main__':
    main()
