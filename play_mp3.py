import pygame


def play_mp3(mp3_file):
    # Khởi tạo pygame
    pygame.init()

    try:
        # Load file mp3
        pygame.mixer.music.load(mp3_file)

        # Phát âm thanh
        pygame.mixer.music.play()

        # Đợi cho đến khi âm thanh phát xong
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # kiểm tra mỗi 10 milliseconds
    except Exception as e:
        print("Có lỗi khi phát âm thanh:", e)
    finally:
        # Dừng pygame khi kết thúc
        pygame.quit()


# Gọi hàm để phát tệp âm thanh .mp3
mp3_file = "video/ghiam.mp3"  # Thay đổi đường dẫn tới tệp .mp3 của bạn
play_mp3(mp3_file)
