""" 
1.游戏流程图
 """

#  2.使用模块和游戏提示
import random


def game_info():
    print('欢迎来到井字棋游戏')
    print('输入数字1~9进行下棋')


# 3.棋盘显示
def display_board(checkerboard):
    """ 棋盘显示 """
    print(' '.join(checkerboard[:3]))
    print(' '.join(checkerboard[3:6]))
    print(' '.join(checkerboard[6:9]))


# 4.玩家下棋输入显示
def chess_limited(number, checkerboard):
    """
    玩家落子限制
    param  number 用户输入
    param  checkerboard 棋盘列表
    return 返回验证过的用户输入
    """
    while True:
        if not number.isdigit():
            print('请输入整数数字')
        elif number not in '1 2 3 4 5 6 7 8 9'.split(' '):
            print('请输入1~9之间的数字')
        elif checkerboard[int(number)-1] != '_':
            print('棋盘上已经有棋子了')
        else:
            break
        number = input()
    return int(number)


# 5 双选验证
def double_verify(a, b, hint):
    """
    双选择验证函数
    param a 第一个选项值
    param b 第二个选项值
    param hint 选项信息
    return 返回输入值
    """
    choice = ''
    while choice.lower() != a and choice.lower() != b:
        print(hint)
        choice = input()
    return choice
# 6 获胜验证


def referee(choice, checkerboard):
    """ 判断谁胜利或平局 """
    if checkerboard[0] == choice and checkerboard[1] == choice and checkerboard[2] == choice:
        return True  # 123
    if checkerboard[3] == choice and checkerboard[4] == choice and checkerboard[5] == choice:
        return True  # 456
    if checkerboard[6] == choice and checkerboard[7] == choice and checkerboard[8] == choice:
        return True  # 789
    if checkerboard[0] == choice and checkerboard[3] == choice and checkerboard[6] == choice:
        return True  #
    if checkerboard[1] == choice and checkerboard[4] == choice and checkerboard[7] == choice:
        return True  # 258
    if checkerboard[2] == choice and checkerboard[5] == choice and checkerboard[8] == choice:
        return True  # 369
    if checkerboard[0] == choice and checkerboard[4] == choice and checkerboard[8] == choice:
        return True  # 159
    if checkerboard[2] == choice and checkerboard[4] == choice and checkerboard[6] == choice:
        return True  # 357
    return False


# 6.用户落子处理
def user_play(user_choice, checkerboard):
    """
    用户选择落子点
    param user_choice 用户所选棋子
    param checjerboard 棋盘列表
    return 返回用户落子完成后的棋盘列表
    """
    print('请选择落子点')
    number = chess_limited(input(), checkerboard)
    checkerboard[number-1] = user_choice
    return checkerboard


# 7.电脑落子处理
def compute_play(compute_choice, checkerboard):
    """
    电脑选择落子点（电脑AI）
    param compute_choice 电脑所选棋子
    param checkerboard 棋盘
    return 电脑下过的棋盘
    """
    copy_win = compute_win(compute_choice, checkerboard)
    if copy_win:  # 电脑获胜
        checkerboard = copy_win
        return checkerboard
    user_win = prevent_user_win(compute_choice, checkerboard)
    if user_win:  # 阻止用户获胜
        checkerboard = user_win
        return checkerboard
    angle = choice_random(compute_choice, checkerboard, [0, 2, 6, 8])
    if angle:  # 角落点
        checkerboard = angle
        return checkerboard
    center = choice_random(compute_choice, checkerboard, [4])
    if center:  # 中心落点
        checkerboard = center
        return checkerboard
    side = choice_random(compute_choice, checkerboard, [1, 3, 5, 7])
    if side:  # 边落点
        checkerboard = side
        return checkerboard
    return checkerboard


# 8.电脑获胜
def compute_win(compute_choice, checkerboard):
    """ 
    获胜的方法（模拟算法）
    return 获胜的棋盘，False 没有可落子的地方
     """
    compute_choice = compute_choice.lower()
    for i in range(9):
        copy_board = checkerboard.copy()
        if copy_board[i] == '_':
            copy_board[i] = compute_choice
            if referee(compute_choice, copy_board):
                checkerboard[i] = compute_choice
                return checkerboard
    return False


# 9. 阻止玩家获胜
def prevent_user_win(compute_choice, checkerboard):
    """ 阻止玩家获胜（模拟玩家获胜下子）
    return 阻止用户获胜的棋盘 False 没有介意阻止的落子
    """
    user_choice = 'O' if compute_choice.lower() == 'x' else 'X'
    user_choice = user_choice.lower()
    for i in range(9):
        copy_board = checkerboard.copy()
        if copy_board[i] == '_':
            copy_board[i] = user_choice
            if referee(user_choice, copy_board):
                # 成功阻止玩家获胜...
                checkerboard[i] = compute_choice
                return checkerboard
    return False
# 10. 电脑随机落点


def choice_random(compute_choice, checkerboard, choice_list):
    """ 随机下棋点 """
    for i in choice_list:
        if checkerboard[i] == '_':
            checkerboard[i] = compute_choice
            return checkerboard
    return False


# 11 游戏主程序
def game_start(user_choice, sequence_flag):
    """ 游戏核心处理
    param user_choice 用户所选棋子
    param sequence_flag 决定先后手
    """
    checkerboard = ['_' for i in range(9)]  # 棋盘列表
    compute_choice = 'O' if user_choice.lower() == 'x' else 'X'
    if sequence_flag:  # 显示棋盘
        print('玩家先走')
    else:
        checkerboard = compute_play(compute_choice, checkerboard)  # 电脑先走棋
        print('电脑先走')
    while True:
        display_board(checkerboard)
        checkerboard = user_play(user_choice, checkerboard)
        if referee(user_choice, checkerboard):
            print('玩家赢')
            display_board(checkerboard)
            break
        checkerboard = compute_play(compute_choice, checkerboard)
        if referee(compute_choice, checkerboard):
            print('电脑赢')
            display_board(checkerboard)
            break
        if '_' not in checkerboard:
            print('平局')
            display_board(checkerboard)
            break


# 12. 游戏外壳
def game_shell():
    """ 外壳程序 """
    game_info()  # 游戏开始提示
    user_choice = double_verify('x', 'o', hint='请选择你的棋子 X or O')
    sequence_flag = random.randint(0, 1)
    game_start(user_choice, sequence_flag)
    while True:
        message = '你想再玩一次吗（Y or N）'
        again_flag = double_verify('y', 'n', message)
        if again_flag == 'n':
            break
        if sequence_flag:
            sequence_flag = 0
        else:
            sequence_flag = 1
            game_start(user_choice, sequence_flag)


# 13. 运行游戏
game_shell()
