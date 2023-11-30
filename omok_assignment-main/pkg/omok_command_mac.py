from tkinter import *
from tkinter import messagebox
import random as rd

class temp_clic():
    """마우스가 클릭 이벤트를 관리하는 클래스"""
    def __init__(self, canvas, entry_x, entry_y):
        self.point_tf=False
        self.canvas=canvas
        self.entry_x=entry_x
        self.entry_y=entry_y

    def point(self, x, y):
        """xy 좌표를 받아와 해당 위치에 빨간색 점을 그려 어느 위치를 선택했는지 표시하는 메서드
        canvas 위에 하나의 포인트만 표시되도록 하기 위해 포인트 존재 여부를 판단한다."""
        if(self.point_tf):
            self.canvas.create_oval(x*50-8, y*50-8, x*50+8, y*50+8, fill="red", tags="point")
            self.point_tf=True
        else:
            self.canvas.delete("point")
            self.canvas.create_oval(x*50-8, y*50-8, x*50+8, y*50+8, fill="red", tags="point")

    def call(self, event):
        """마우스 클릭 이벤트가 일어난 self.canvas의 좌표를 받아와 그 값을 계산하여 엔트리에 삽입하는 메서드"""
        xc=event.x
        yc=event.y

        for i in range(1, 14):
            for j in range(1, 14):
                if((i)*50-10<=xc<=(i)*50+10 and (j)*50-10<=yc<=(j)*50+10):
                    self.entry_x.delete(0, END)
                    self.entry_y.delete(0, END)
                    self.entry_x.insert(0, i)
                    self.entry_y.insert(0, j)
        
        if(self.entry_x.get()!=""): # 엔트리에 공백이 없을 경우
            self.point(int(self.entry_x.get()), int(self.entry_y.get()))
    
    def delete_point(self):
        """self.canvas 위에 존재하는 포인트를 삭제하는 메서드"""
        self.canvas.delete("point")
        self.point_tf=False

# ----------------------------------------------------------------------------------------------------------------------------------

class random_item:
    """랜덤하게 생성되는 아이템을 관리하는 클래스"""
    def __init__(self, canvas):
        self.two_items={1: "erase_item", 2: "two_placement_item"}
        self.stone_list=command_class.all_list
        self.item_tf=False
        self.x=0
        self.y=0
        self.item_num=None
        self.item_list=[PhotoImage(file="pkg/지우기.png"), PhotoImage(file="pkg/두번놓기.png")]
        self.canvas=canvas

    def item_per(self, percentage):
        """아이템이 생성될 확률을 결정하는 메서드
        canvas 위에 이미 아이템이 있을 경우 새로운 아이템이 생성되지 않도록 한다."""
        if(self.item_tf):
            return False
        else:
            per=rd.random()
            return per<=percentage/100

    def make_item(self):
        """랜덤한 아이템을 랜덤한 위치에 생성하고 그 이미지를 canvas에 그리는 메서드
        중앙 근처에서 아이템이 생성되도록 하며, 중앙에 더이상 아이템을 생성할 공간이 없을 경우 가장자리에서도 아이템이 생성된다."""
        try:
            self.x=rd.choice([i for i in range(4, 11) if(i not in list(map(lambda x:x[0], self.stone_list)))])
            self.y=rd.choice([j for j in range(4, 11) if(j not in list(map(lambda x:x[1], self.stone_list)))])
            self.item_num=rd.randrange(1, 3)
            item_image=self.item_list[self.item_num-1]
            self.canvas.create_image(self.x*50, self.y*50, image=item_image, tags="item")
            self.item_tf=True
        except IndexError:
            self.x=rd.choice([i for i in [1, 2, 3, 11, 12 ,13] if(i not in list(map(lambda x:x[0], self.stone_list)))])
            self.y=rd.choice([j for j in [1, 2, 3, 11, 12, 13] if(j not in list(map(lambda x:x[1], self.stone_list)))])
            self.item_num=rd.randrange(1, 3)
            item_image=self.item_list[self.item_num-1]
            self.canvas.create_image(self.x*50, self.y*50, image=item_image, tags="item")
            self.item_tf=True

    def del_item(self):
        """self.canvas 위에 존재하는 아이템을 삭제하는 메서드"""
        self.canvas.delete("item")
        self.item_tf=False

# ----------------------------------------------------------------------------------------------------------------------------------

class command_class():
    """'착수' 버튼이 눌릴 때마다 실행되는 함수들을 관리하는 메서드
    한 번 '착수' 버튼이 눌리는 것을 한 턴으로 가정한다."""
    all_list=[]
    count=0

    def __init__(self, stone, clic, rd_item, win, entry_x, entry_y, canvas, listbox):
        if(stone=="black"):
            self.stone_image=PhotoImage(file="pkg/검은돌48.png")
            self.order=True
        else:
            self.stone_image=PhotoImage(file="pkg/흰돌48.png")
            self.order=False
        self.stone=stone # 돌 속성
        self.placement_list=[] # 놓여진 돌 좌표 리스트
        self.clic=clic # 클릭 인스턴스
        self.rd_item=rd_item # 랜덤 아이템 인스턴스
        self.erase_turn=False
        self.win=win
        self.entry_x=entry_x
        self.entry_y=entry_y
        self.canvas=canvas
        self.listbox=listbox

        self.board=[] # 돌이 높인 위치 보드
        for _ in range(13):
            self.board.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def get_other(self, other):
        """외부에서 상대방의 인스턴스를 받아오는 메서드"""
        self.other=other

    def error_message(self, comment):
        """에러창을 띄우고 엔트리에 입력된 값을 지우는 메서드"""
        messagebox.showerror("오류", comment)
        self.entry_x.delete(0, END)
        self.entry_y.delete(0, END)

    def win_judge(self, x, y):
        """버튼이 눌릴 때마다 우승 여부를 판단하는 메서드"""
        for x in range(13):
            for y in range(9):
                if sum(self.board[x][y:y+5]) == 5:
                    return 'win'

        # 세로
        for x in range(9):
            for y in range(13):
                if sum(self.board[x+i][y] for i in range (5)) == 5:
                    return 'win'

        # 대각선 (왼쪽 위에서 오른쪽 아래로)
        for x in range(9):
            for y in range(9):
                if sum(self.board[x+i][y+i] for i in range(5)) == 5:
                    return 'win'

        # 대각선 (오른쪽 위에서 왼쪽 아래로)
        for x in range(9):
            for y in range(4, 13):
                if sum(self.board[x+i][y-i] for i in range(5)) == 5:
                    return 'win'
                
    def win_judge_temp(self, x, y):
        wc=1
        sc=0
        for x in range(13):
            for y in range(13):
                if(self.board[x+1][y+1]==1):
                    for a in range(13-(x+1)): #가로 확인
                        if(self.board[x+1+(a+1)][y+1]==1):
                            wc+=1
                        else:
                            break
                    if(wc>=5):
                        return "win"
                    else:
                        wc=1
                    for a in range(13-(y+1)): #세로 확인
                        if(self.board[x+1][y+1+(a+1)]==1):
                            wc+=1
                        else:
                            break
                    if(wc>=5):
                        return "win"
                    else:
                        wc=1
                    for a in range(13): #대각선 아래 개수 확인
                        if(self.board[x+1+(a+1)][y+1+(a+1)]==0 or self.board[x+1+(a+1)][y+1+(a+1)]==1):
                            sc+=1
                        else:
                            break
                    for a in range(sc): #대각선 아래 확인
                        if(self.board[x+1+(a+1)][y+1+(a+1)]==1):
                            wc+=1
                        else:
                            break
                    if(wc>=5):
                        return "win"
                    else:
                        wc=1
                        sc=0
                    for a in range(13): #대각선 아래 개수 확인
                        if(self.board[x+1-(a+1)][y+1+(a+1)]==0 or self.board[x+1-(a+1)][y+1+(a+1)]==1):
                            sc+=1
                        else:
                            break
                    for a in range(sc): #대각선 아래 확인
                        if(self.board[x+1-(a+1)][y+1+(a+1)]==1):
                            wc+=1
                        else:
                            break
                    if(wc>=5):
                        return "win"
                    else:
                        wc=1
                        sc=0

    def placement(self):
        """엔트리의 좌표를 받아와 해당 위치에 돌 이미지를 생성하는 메서드"""
        x=self.entry_x.get()
        y=self.entry_y.get() 
        try:
            x=int(x)
            y=int(y)
            if(self.erase_turn):
                self.error_message("지울 돌의 위치를 선택하고 '지우기' 버튼을 누르세요")
                self.clic.delete_point()
            else:
                if((x>=1 and x<=13) and (y>=1 and y<=13)):
                    if(([x, y] in self.placement_list) or ([x, y] in self.other.placement_list)):
                        self.error_message("이미 다른 돌이 해당 위치에 있습니다.")
                    else:
                        command_class.count+=1 # 공유 카운트
                        self.canvas.create_image(x*50, y*50, image=self.stone_image, tags=f"check[{x},{y}]") 
                        self.board[x-1][y-1]=1 # 보드에 추가
                        self.entry_x.delete(0, END)
                        self.entry_y.delete(0, END)
                        self.placement_list.append([x, y]) # 리스트에 추가
                        self.all_list.append([x, y]) # 공유 리스트에 추가

                        # 리스트박스 추가
                        if(command_class.count<10):
                            seq="00"+str(command_class.count)
                        elif(10<=command_class.count and command_class.count<100):
                            seq="0"+str(command_class.count)
                        else:
                            seq=str(command_class.count)

                        if(self.stone=="black"):
                            self.listbox.insert(END, seq+f" ----({x},{y})---- ⚪")
                            self.listbox.see(END)
                        else:
                            self.listbox.insert(END, seq+f" ----({x},{y})---- ⚫")
                            self.listbox.see(END)

                        # 다음 순서 결정
                        self.order=False
                        self.other.order=True

                        # 포인터 지우기
                        self.clic.delete_point()

                        # 아이템 생성
                        if(self.rd_item.item_per(60)):
                            self.rd_item.make_item()

                        # 아이템을 획득했을 경우
                        if(x==self.rd_item.x and y==self.rd_item.y):
                            if(self.rd_item.item_num==1): # 지우기
                                self.order=True
                                self.other.order=False
                                self.erase_turn=True
                                self.rd_item.del_item()
                            else: # 두 번 놓기
                                self.order=True
                                self.other.order=False 
                                self.rd_item.del_item()

                        if(self.win_judge(x, y)=="win"): # 우승 판단
                            if(self.stone=="black"):
                                messagebox.showinfo("흑 승리", "흑이 우승했습니다!")
                                self.win.destroy()
                            else:
                                messagebox.showinfo("백 승리", "백이 우승했습니다!")
                                self.win.destroy()
                else:
                    self.error_message("1부터 13까지 숫자를 입력하세요")
        except ValueError:
            self.error_message("정수숫자를 입력하세요")

    def erase(self):
        """'지우기' 아이템을 획득할 경우 활성화되어 선택한 위치에 있는 상대방의 돌을 지우는 메서드"""
        if(self.erase_turn):
            try:
                x=int(self.entry_x.get())
                y=int(self.entry_y.get())
                if([x, y] in self.other.placement_list):
                    self.other.placement_list.remove([x, y])
                    self.all_list.remove([x, y])
                    self.canvas.delete(f"check[{x},{y}]")
                    self.board[x-1][y-1]=0
                    self.order=False
                    self.other.order=True
                    self.erase_turn=False
                    command_class.count+=1

                    # 리스트박스 
                    if(command_class.count<10):
                        seq="00"+str(command_class.count)
                    elif(10<=command_class.count and command_class.count<100):
                        seq="0"+str(command_class.count)
                    else:
                        seq=str(command_class.count)

                    if(self.stone=="black"):
                        self.listbox.insert(END, seq+f" ----({x},{y}) erased ⚫")
                        self.listbox.see(END)
                    else:
                        self.listbox.insert(END, seq+f" ----({x},{y}) erased ⚪")
                        self.listbox.see(END)

                    # 포인트 지우기
                    self.clic.delete_point()

                    # 엔트리 지우기
                    self.entry_x.delete(0, END)
                    self.entry_y.delete(0, END)
                else:
                    self.error_message("지우고싶은 상대방의 돌의 위치를 정하세요")
                    self.clic.delete_point()
            except ValueError:
                self.error_message("정수숫자를 입력하세요")
        else:
            self.error_message("'지우기' 아이템이 없습니다")