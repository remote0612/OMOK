from tkinter import END

class other_command():
    @staticmethod
    def close(messagebox, win): # 종료하기 메서드
        message_close=messagebox.askyesno("종료하기", "종료하시겠습니까?")
        if(message_close==1):
            win.destroy()

    @staticmethod
    def restart(black, white, messagebox, command_class, canvas, listbox, entry_x, entry_y): # 다시하기 메서드
        message_restart=messagebox.askyesno("다시하기", "판을 엎으시겠습니까?")
        if(message_restart):
            for i in command_class.all_list:
                canvas.delete(f"check[{i[0]},{i[1]}]") # 돌 지우기
            for _ in range(command_class.count):
                listbox.delete(END) # 리스트박스 초기화
            black.placement_list=[]
            black.order=True
            white.placement_list=[]
            white.order=False
            command_class.all_list=[]
            command_class.count=0
            black.rd_item.del_item()
            white.clic.delete_point()

            black.board=[]
            for _ in range(13):
                black.board.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            white.board=[]
            for _ in range(13):
                white.board.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

            # 엔트리 지우기
            entry_x.delete(0, END)
            entry_y.delete(0, END)