from pkg.omok_command_mac import *
from pkg.omok_other import *

win=Tk() # 윈도우 인스턴스

win.title("오목") # 타이틀
win.geometry("1000x700") # 윈도우 크기
win.option_add("*Font", "맑은고딕 10") 

# 프레임 지정
frame_left=Frame(win, relief="solid") # 왼쪽 프레임
frame_left.config(width=700, height=700)
frame_left.pack(side="left", fill="both")

frame_right=Frame(win, relief="solid") # 오른쪽 프레임
frame_right.config(width=300, height=700)
image_wood=PhotoImage(file="pkg/wood.png") # 오른쪽 프레임 이미지
frame_right.pack(side="right", fill="both")
label_image=Label(frame_right, width=300, height=700, image=image_wood)
label_image.pack()

frame_list=Frame(frame_right, relief="solid") # 리스트박스 프레임
frame_list.place(x=25, y=25, width=250, height=350)

# 캔버스 지정
canvas=Canvas(frame_left, relief="solid", ) # 밑바탕
canvas.config(width=700, height=700) # 캔버스 크기
image_wood_pan=PhotoImage(file="pkg/wood_pan.png")
canvas.create_image(0, 0, image=image_wood_pan)
canvas.create_line(50, 50, 50, 650, 650, 650, 650, 50, 50, 50, width=3) # 아웃라인
a=100 # 가로선 초기값
b=100 # 세로선 초기값
c=50 # 가로숫자 초기값
d=50 # 세로숫자 초기값
for i in range(11): # 가로선
    canvas.create_line(a, 50, a, 650, width=1)
    a+=50
for i in range(11): # 세로선
    canvas.create_line(50, b, 650, b, width=1)
    b+=50
for j in range(13): # 가로숫자
    canvas.create_text(c, 15, text=j+1, fill="black",font=('Helvetica 10 bold'))
    c+=50
for j in range(13): # 세로숫자
    canvas.create_text(15, d, text=j+1, fill="black",font=('Helvetica 10 bold'))
    d+=50
canvas.create_oval(347, 347, 353, 353, fill="black") # 중앙 화점
canvas.create_oval(197, 197, 203, 203, fill="black") # 좌상귀 화점
canvas.create_oval(197, 497, 203, 503, fill="black") # 좌하귀 화점
canvas.create_oval(497, 197, 503, 203, fill="black") # 우상귀 화점
canvas.create_oval(497, 497, 503, 503, fill="black") # 우하귀 화점
canvas.pack()


scrollbar=Scrollbar(frame_list) # 리스트박스 스크롤바
scrollbar.pack(side="right", fill="both")

listbox=Listbox(frame_list, selectmode="extend") # 리스트박스
listbox.config(width=33, height=100, relief="flat", bg="#36393F", yscrollcommand=scrollbar.set)
listbox.config(fg="white", font="맑은고딕 15")
listbox.insert(0, "----->>Begin<<-----")
listbox.pack(side="left")

scrollbar.config(command=listbox.yview) 

# 엔트리
entry_x=Entry(frame_right, width=7, font="맑은고딕 17") #가로 엔트리
entry_x.place(x=85, y=465)
lb1=Label(frame_right, width=5, font="맑은고딕 16", text="가로")
lb1.place(x=25, y=465)
entry_y=Entry(frame_right, width=7, font="맑은고딕 17") #세로 엔트리
entry_y.place(x=85, y=500)
lb2=Label(frame_right, width=5, font="맑은고딕 16", text="세로")
lb2.place(x=25, y=500)

# -----------------------------------------------------------------------------------------------------

clic=temp_clic(canvas, entry_x, entry_y) # 클릭 인스턴스
canvas.bind("<Button-1>", clic.call) # 마우스 오른쪽 클릭 명령어 전달

item_instance=random_item(canvas) # 아이템 인스턴스

black=command_class("black", clic, item_instance, win, entry_x, entry_y, canvas, listbox) # 흑돌 인스턴스
white=command_class("white", clic, item_instance, win, entry_x, entry_y, canvas, listbox) # 백돌 인스턴스
# 상대방의 인스턴스 받아오기
black.get_other(white) 
white.get_other(black)

def take_turns(): # 착수 턴 관리 함수
    if(black.order):
        return black.placement()
    else:
        return white.placement()

def take_erase_turns(): # 지우기 턴 관리 함수
    if(black.order):
        return black.erase()
    else:
        return white.erase()
    
def return_close():
    return other_command.close(messagebox, win)

def return_restart(): # 다시하기 반환 함수
    return other_command.restart(black, white, messagebox, command_class, canvas, listbox, entry_x, entry_y)

# -----------------------------------------------------------------------------------------------------

button_back=Button(frame_right, width=10, height=1, font="맑은고딕 16")
button_back.config(text="지우기", command=take_erase_turns)
button_back.place(x=25, y=397)

button_start=Button(frame_right, width=7, height=2, font="맑은고딕 17")
button_start.config(text="착수", command=take_turns)
button_start.place(x=180, y=465)

button_close=Button(frame_right, width=9, height=1, font="맑은고딕 17")
button_close.config(text="종료", command=return_close)
button_close.place(x=25, y=645)

button_restart=Button(frame_right, width=9, height=1, font="맑은고딕 17")
button_restart.config(text="다시하기", command=return_restart)
button_restart.place(x=160, y=645)

# -----------------------------------------------------------------------------------------------------

win.mainloop()
