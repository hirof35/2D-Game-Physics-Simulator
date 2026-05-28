import time

# ---
## Ball Class
# ---
class Ball:
    x = 0  # x座標
    y = 0  # y座標
    vx = 0 # x方向の速度
    vy = 0 # y方向の速度
    isActive = True # 弾が有効かどうかのフラグ（True:有効、False:無効）

    def __init__(self, x, y, vx, vy, isActive):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.isActive = isActive

# ---
## Player Class
# ---
class Player:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 弾を発射するメソッド
    def shoot_ball(self, ball_speed):
        # Create a new ball at the player's current position
        new_ball = Ball(self.x, self.y, ball_speed, 0, True)
        print("弾を発射しました！")
        return new_ball

    # 弾を更新する関数 (Ball itself could have this method, but Player managing it is also fine)
    def update_ball(self, ball):
        if ball.isActive:
            ball.x += ball.vx
            ball.y += ball.vy

            # 画面外に出た場合は非活動状態にする
            # 仮に画面範囲をX:0-800, Y:0-600と想定
            if ball.x < 0 or ball.x > 800 or ball.y < 0 or ball.y > 600:
                ball.isActive = False
                print("弾は画面外に出ました。")

# ---
## Jump_Player Class
# ---
class Jump_Player:
    x = 0  # x座標
    y = 0  # y座標
    isJumping = False  # ジャンプ中かどうかのフラグ（True:ジャンプ中、False:地上）
    jump_speed = 0     # ジャンプの初速度
    gravity = 0        # 重力の値（ジャンプ中に適用される）
    vy = 0             # y方向の速度（ジャンプ中の上昇・下降に使用）

    # プレイヤーの初期化メソッド (Using __init__ for standard Pythonic class initialization)
    def __init__(self, start_x, start_y, initial_jump_speed, initial_gravity):
        self.x = start_x
        self.y = start_y
        self.jump_speed = initial_jump_speed
        self.gravity = initial_gravity
        self.vy = 0
        self.isJumping = False # Ensure player starts on the ground

    # プレイヤーのジャンプメソッド
    def jump(self):
        if not self.isJumping: # 地上にいる場合のみジャンプ可能
            self.isJumping = True
            self.vy = self.jump_speed  # 上向きに初期速度を設定
            print("プレイヤーがジャンプしました！")
        else:
            print("プレイヤーは既にジャンプ中です。")

    # プレイヤーの更新メソッド
    def update_jump_state(self):
        if self.isJumping:
            self.y += self.vy  # Y座標を更新
            self.vy -= self.gravity # 重力を適用してY方向速度を減少させる

            # 地面に着地した場合の処理
            if self.y <= 10: # 地面のY座標を10と仮定
                self.y = 10     # 地面に着地
                self.isJumping = False # ジャンプ状態を解除
                self.vy = 0     # Y方向速度をリセット
                print("プレイヤーが地面に着地しました。")

    # プレイヤーの現在位置を表示するメソッド
    def display_jump_player_status(self):
        status = "ジャンプ中" if self.isJumping else "地上"
        print(f"プレイヤーの位置: (x = {self.x}, y = {self.y}) - {status}")

# ---
## Game Logic Functions
# ---

# Function for ball shooting simulation
def run_ball_simulation(player_obj):
    current_ball = None # No ball initially

    while True:
        print("\n----------------------------------------");
        print("弾を発射するには1を入力、終了するには0を入力してください: ");

        try:
            choice = int(input())
        except ValueError:
            print("無効な入力です。数字を入力してください。");
            continue

        if choice == 0:
            print("弾発射シミュレーションを終了します。");
            break

        elif choice == 1:
            if current_ball is not None and current_ball.isActive:
                print("弾はすでに発射されています。新しい弾を発射するには、現在の弾が非活動状態になるまで待ってください。");
                continue

            print("弾の速度を入力してください: ")
            try:
                speed = int(input())
            except ValueError:
                print("無効な速度です。数字を入力してください。")
                continue

            # 弾を発射
            current_ball = player_obj.shoot_ball(speed)

            # 弾が活動状態である限り、更新を繰り返す
            if current_ball.isActive:
                print("弾が移動中です...")
                update_count = 0
                while current_ball.isActive:
                    player_obj.update_ball(current_ball) # Player updates its associated ball
                    print(f"現在の弾の位置: x = {current_ball.x}, y = {current_ball.y}")
                    update_count += 1
                    time.sleep(0.05) # Wait for 50 milliseconds

                print(f"弾の移動が終了しました（{update_count}回更新）。")
            else:
                print("弾は発射されませんでした。"); # Should only happen if speed immediately puts it out of bounds
        else:
            print("無効な入力です。もう一度試してください。");

# Function for jump simulation
def run_jump_simulation(jump_player_obj):
    # Initialize the jump player for this simulation run
    # Set a reasonable jump speed and gravity
    jump_player_obj.__init__(50, 10, 15, 0.8) # x, y, jump_speed, gravity
    print("ジャンプシミュレーションを開始します。");
    jump_player_obj.display_jump_player_status() # 初期状態を表示

    while True:
        print("ジャンプするには1を入力、終了するには0を入力してください: ");
        try:
            user_input = int(input()) # Use a different variable name
        except ValueError:
            print("無効な入力です。数字を入力してください。");
            continue

        if user_input == 0:
            print("ジャンプシミュレーションを終了します。");
            break

        elif user_input == 1:
            if not jump_player_obj.isJumping: # Only allow jump if not already jumping
                jump_player_obj.jump() # Start the jump
                # Now, continuously update and display until the jump is over
                while jump_player_obj.isJumping:
                    jump_player_obj.update_jump_state()
                    jump_player_obj.display_jump_player_status()
                    time.sleep(0.1) # Shorter delay for smoother jump animation
            else:
                print("プレイヤーは既にジャンプ中です。");
        else:
            print("無効な入力です。もう一度試してください。");

# ---
## Main Program
# ---
def main():
    player_for_ball_sim = Player(50, 300) # Player object for ball simulation
    jump_player_obj = Jump_Player(0, 0, 0, 0) # Initialize Jump_Player, will be re-initialized in run_jump_simulation

    while True:
        print("\nどちらのシミュレーションを実行しますか？");
        print("1: 弾発射シミュレーション");
        print("2: ジャンプシミュレーション");
        print("0: プログラムを終了");
        print("選択してください: ");

        try:
            num = int(input())
        except ValueError:
            print("無効な入力です。数字を入力してください。");
            continue

        if num == 1:
            run_ball_simulation(player_for_ball_sim)
        elif num == 2:
            run_jump_simulation(jump_player_obj)
        elif num == 0:
            print("プログラムを終了します。");
            break
        else:
            print("無効な入力です。もう一度試してください。");

if __name__ == "__main__":
    main()
    
