import os
import tkinter as tk
from tkinter import messagebox
import cv2
import mediapipe as mp
import numpy as np
import pickle
from PIL import Image, ImageTk
from PIL import Image, ImageFont, ImageDraw
import time
from tkinter import font
import datetime
import asyncio
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

def number_to_letter(number):
    if 1 <= number <= 26:
        return chr(64 + number) 
    else:
        return None 
    
labels = [chr(ord('A') + i) for i in range(26)]
image_paths = [f'imgs/{label}.png' for label in labels]
model_dict = pickle.load(open('model/model.p', 'rb'))
model = model_dict['model']
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
labels_dict = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'J',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
    25: 'Z'
}
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

class SignLanguageApp:
    def __init__(self, root):
        self.camera_flag = False
        self.root = root
        self.double = 0
        self.root.title("Sign Language App")
        self.root.attributes("-fullscreen", True)  
        self.root.configure(bg="#ff9e9e") 
        custom_font = font.Font(family="Bebas Neue", size=14)
        custom_font1 = font.Font(family="Bebas Neue", size=60)
        custom_font2 = font.Font(family="Bebas Neue", size=20)
        custom_font3 = font.Font(family="Bebas Neue", size=40)
        custom_font5 = font.Font(family="Bebas Neue", size=100)
        title_label = tk.Label(root, text="Learn Sign Language!", font=custom_font1, bg="#ff9e9e")
        title_label.pack(pady=20)

        self.re_label = tk.Label(root, text="Replicate the Hand Gesture shown.", font=custom_font3, bg="#ff9e9e")
        self.be_label = tk.Label(root, text="Make the Hand Gesture for the letter shown.", font=custom_font3, bg="#ff9e9e")
        

        self.canvas = tk.Canvas(root, width=400, height=400,  highlightthickness=7, highlightbackground='#db044c', bg="#ffffff",)
        self.canvas.pack()
        self.good_job_label = tk.Label(root, text="Good Job!", font=custom_font5, fg="green", bg="#ff9e9e",anchor="center")
        self.practice_button = tk.Button(
            root, text="Practice", command=self.start_practice, font=custom_font2,fg="white", bg="#de0046", padx=20, pady=10
        )
        self.practice_button.pack(pady=20)

        self.hinted = tk.Button(
            root, text="HINT", command=self.hint, font=custom_font2,fg="white", bg="#ff003c", padx=20, pady=10
        )     

        self.learn_button = tk.Button(
            root, text="Learn", command=self.start_learning, font=custom_font2, fg="white", bg="#de0046", padx=20, pady=10
        )
        self.learn_button.pack(pady=0)
        self.camera_frame_label = tk.Label(root)
        
        self.quit_button = tk.Button(
            root, text="Quit", command=self.root.destroy, font=custom_font, bg="#f97171", padx=10, pady=5
        )

        self.go_back_button = tk.Button(
            root, text="Go Back", command=self.go_back, font=custom_font, bg="#99cc99", padx=10, pady=5
        )

        self.quit_button.pack(side="top", anchor="ne", padx=20, pady=10)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

        self.image_index = 0
    
        self.img_tk = None
        self.display_image()

    def display_image(self):
        img = Image.open('imgs/hands.png')
        img = img.resize((400, 400)) 
        self.img_tk = ImageTk.PhotoImage(img) 
        self.canvas.create_image(207, 207, image=self.img_tk)

    def hide_good_job(self):
        self.good_job_label.pack_forget()
    
    def hint(self):
        self.canvas.delete("all") 
        ind = self.image_index -1
        image_path = image_paths[ind]
        img = Image.open(image_path)
        img = img.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.image = img_tk
        self.canvas.create_image(207, 207, image=img_tk)

        self.root.after(3000, self.showimage)
        
    
    def showimage(self):
        self.canvas.delete("all") 
        letter = number_to_letter(self.image_index)
        letter = letter.upper()
        img = Image.open('imgs/base.png')
        img = img.resize((400, 400))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/BebasNeue-Regular.ttf", 400)
        draw.text((200,215), letter, font = font,fill=(0, 0, 0), anchor='mm')                      
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.image = img_tk
        self.canvas.create_image(207, 207, image=img_tk)


    def go_back(self):
        self.canvas.delete("all") 
        
        self.go_back_button.pack_forget()  
        self.practice_button.pack(pady=20) 
        self.learn_button.pack(pady=20) 
        self.quit_button.pack(side="top", anchor="ne", padx=20, pady=10)
        self.hinted.pack_forget()
        self.camera_flag = False
        self.image_index = 0
        self.be_label.pack_forget()  
        self.re_label.pack_forget()  
        self.display_image()
        if self.camera_frame_label is not None:
            self.camera_frame_label.pack_forget()
            
    def start_practice(self):
        self.quit_button.pack_forget()
        self.practice_button.pack_forget()  
        self.be_label.pack(pady=0)
        self.learn_button.pack_forget()  
        self.canvas.delete("all") 
        self.hinted.pack(side="top", anchor="center", padx=10)
        self.go_back_button.pack(side="top", anchor="nw", padx=20)
        
        self.random_next_image()


    def start_learning(self):
        self.quit_button.pack_forget()
        self.practice_button.pack_forget()  
        self.learn_button.pack_forget()  
        self.canvas.delete("all") 
        self.go_back_button.pack(side="top", anchor="nw", padx=20, pady=10)
        self.re_label.pack(pady=0)
        self.display_next_image()

        
    def display_next_image(self):
        if self.image_index < len(image_paths):
            image_path = image_paths[self.image_index]
            img = Image.open(f'{image_path}')
            img = img.resize((400, 400))
            img_tk = ImageTk.PhotoImage(img)
            self.canvas.create_image(207, 207, image=img_tk)
            self.image_index += 1
            self.camera_flag = True
            self.root.after(1, self.start_camera(image_path))
            if self.camera_flag:
                pass
            else:
                return
        else:
            messagebox.showinfo("Learning Completed", "Good job! You've completed learning.")

    def random_next_image(self):
        if self.image_index < len(image_paths):
            self.image_index = random.randint(1,26)
            letter = number_to_letter(self.image_index)
            letter = letter.upper()
            img = Image.open('imgs/base.png')
            img = img.resize((400, 400))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("fonts/BebasNeue-Regular.ttf", 400)
            image_path = letter
            draw.text((200,215), letter, font = font,fill=(0, 0, 0), anchor='mm')                      
            img_tk = ImageTk.PhotoImage(img)
            self.canvas.create_image(207, 207, image=img_tk)
            self.camera_flag = True
            self.root.after(1, self.start_camera(image_path))
            if self.camera_flag:
                pass
            else:
                return
        else:
            messagebox.showinfo("Learning Completed", "Good job! You've completed learning.")


    def start_camera(self,image_path):
        cap = cv2.VideoCapture(0)
        self.camera_frame_label.pack(side="right", padx=0, pady=0)

        
        def update_camera_feed():
            if self.camera_flag:
                pass
            else:
                cap.release()
                cv2.destroyAllWindows()
                return 
            ret, frame = cap.read()

            if ret:
                check = False
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                data_aux = []
                x_ = []
                y_ = []
                H, W, _ = frame.shape
                results = self.hands.process(frame_rgb)
                timenow = None
                if results.multi_hand_landmarks:
                    if len(results.multi_hand_landmarks) == 1:  
                        hand_landmarks = results.multi_hand_landmarks[0] 

                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y

                            x_.append(x)
                            y_.append(y)

                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            data_aux.append(x - min(x_))
                            data_aux.append(y - min(y_))

                        x1 = int(min(x_) * W) - 10
                        y1 = int(min(y_) * H) - 10

                        x2 = int(max(x_) * W) - 10
                        y2 = int(max(y_) * H) - 10

                        prediction = model.predict([np.asarray(data_aux)])
                        predicted_character = labels_dict[int(prediction[0])]

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                                    cv2.LINE_AA)
                        if predicted_character == image_path[0]:
                            self.double += 1
                            if 33 > self.double > 0:
                                cv2.putText(frame, "HOLD FOR 3 SECONDS", (10, H - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                            elif 66 > self.double >= 33:
                                cv2.putText(frame, "HOLD FOR 2 SECONDS", (10, H - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                            else: 
                                cv2.putText(frame, "HOLD FOR 1 SECOND", (10, H - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

                            if self.double > 100:
                                
                                self.good_job_label.pack(side="left", padx=10, pady=0)
                                self.root.after(4000, self.hide_good_job)
                                check = True
                                self.double = 0
                        else:
                            self.double = 0
 
                    else:
                        cv2.putText(frame, "PLEASE USE ONE HAND", (10, H - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (400, 300))
                img_tk = ImageTk.PhotoImage(image=Image.fromarray(frame_resized))
                self.camera_frame_label.config(image=img_tk)
                self.camera_frame_label.image = img_tk
                if check:
                    cap.release()
                    cv2.destroyAllWindows()
                    if len(image_path) > 1:
                        self.display_next_image()
                    else:
                        self.random_next_image()
                    return
                self.root.after(1, update_camera_feed)  

            
        update_camera_feed() 

        self.root.mainloop()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    root.mainloop()