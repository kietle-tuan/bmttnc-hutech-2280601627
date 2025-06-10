import tornado.ioloop
import tornado.websocket

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None  # Khởi tạo self.connection
        self.io_loop = io_loop
        
    def start(self):
        # Khi khởi động, cố gắng kết nối và đọc tin nhắn
        self.connect_and_read()
        
    def stop(self):
        # Dừng io_loop khi muốn dừng client
        self.io_loop.stop()
        
    def connect_and_read(self): # Đã sửa tên từ connect_add_read thành connect_and_read
        print("Đang cố gắng kết nối và đọc tin nhắn...")
        tornado.websocket.websocket_connect( # Đảm bảo gọi từ tornado.websocket
            url=f"ws://localhost:8888/websocket/",
            callback=self.maybe_retry_connection,
            on_message_callback=self.on_message,
            ping_interval=10,
            ping_timeout=30,
        )
        
    def maybe_retry_connection(self, future) -> None: # Đã sửa none thành None
        try:
            self.connection = future.result()
            print("Đã kết nối thành công tới server!")
            # Bắt đầu đọc tin nhắn ngay sau khi kết nối thành công
            self.connection.read_message(callback=self.on_message)
        except Exception as e: # Bắt lỗi cụ thể hơn
            print(f"Không thể kết nối lại, thử lại sau 3 giây... Lỗi: {e}")
            self.io_loop.call_later(3, self.connect_and_read) # Lên lịch kết nối lại

    def _disconnect(self): # Thêm phương thức ngắt kết nối
        if self.connection:
            print("Ngắt kết nối khỏi server.")
            self.connection.close()
            self.connection = None # Đặt lại kết nối về None
            
    def on_message(self, message):
        if message is None: # Nếu nhận được None, nghĩa là server đã đóng kết nối
            print("Server đã đóng kết nối. Đang cố gắng kết nối lại...")
            self._disconnect() # Gọi ngắt kết nối
            self.io_loop.call_later(1, self.connect_and_read) # Lên lịch kết nối lại sau 1 giây
            return

        print(f"Nhận được từ server: {message}")
        # Sau khi xử lý tin nhắn, tiếp tục đọc tin nhắn tiếp theo
        if self.connection: # Đảm bảo kết nối vẫn còn trước khi đọc tiếp
            self.connection.read_message(callback=self.on_message)

def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    io_loop.add_callback(client.start) # Thêm callback để bắt đầu client
    io_loop.start()

if __name__ == "__main__":
    main()