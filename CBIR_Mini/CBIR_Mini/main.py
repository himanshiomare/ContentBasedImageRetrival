import os
import time
import cv2
import numpy as np
import pandas as pd
from createFeatures import extract_features
import tkinter as tk
from tkinter import filedialog, Scrollbar, messagebox
from PIL import Image, ImageTk
from similarity import euclidean

df = pd.DataFrame([])
query_image = None
query_image_file_path = None
times = 1


def retrieve_similar_images():
    if query_image_file_path is None:
        return []

    # query image
    q_image_bgr = cv2.imread(query_image_file_path)
    q_lbp_features_vector_data, q_cm_features_vector_data = extract_features(q_image_bgr)

    q_feature_vector_combined = np.concatenate((q_lbp_features_vector_data, q_cm_features_vector_data), axis=0)

    all_images_similarity = []

    st_time = time.time()

    print("Length of df: ", len(df))
    print("Size of df: ", df.size)
    print("Shape of df: ", df.shape)

    for i in range(len(df)):
        db_image_lbp = df.iloc[i][1:257]
        db_image_cm = df.iloc[i][257:]
        db_cm = db_image_cm.values.reshape(3, 3)
        q_cm = np.array(q_cm_features_vector_data).reshape(3, 3)

        d_mom = 0

        # for j in range(3):
        #     d_mom += (abs(db_cm[j][0] - q_cm[j][0]) / (abs(db_cm[j][0]) + abs(q_cm[j][0])))  # added mean
        #     d_mom += (abs(db_cm[j][1] - q_cm[j][1]) / (
        #                 abs(db_cm[j][1]) + abs(q_cm[j][1])))  # added standard deviation
        #     d_mom += (abs(db_cm[j][2] - q_cm[j][2]) / (abs(db_cm[j][2]) + abs(q_cm[j][2])))  # added skewness

        # all_images_similarity.append([d_mom, df.iloc[i][0]])  # calculating only cm for now

        all_images_similarity.append(
            [euclidean(q_lbp_features_vector_data, db_image_lbp), df.iloc[i][0]])  # calculating only lbp for now, 213

        print("Done with : ", df.iloc[i][0], " with distance: ", all_images_similarity[i])
        # 157

    all_images_similarity.sort(key=lambda x: x[0])

    output_feature_vectors = all_images_similarity[:10]

    end_time = time.time()

    print(output_feature_vectors)
    print("Time taken ", end_time - st_time)

    return output_feature_vectors


def update_similar_images():
    if query_image is None:
        messagebox.showinfo("Error", "Please select an query image before fetching")
        return

    # Retrieve similar images for query image
    # Returned value is of the form [[dist1, 50.jpg], [dist2, 405.jpg], ....]
    similar_images = retrieve_similar_images()  # for example: 340.jpg

    query_canvas.delete('all')
    similar_canvas.delete('all')

    # Display query image in canvas
    query_canvas.create_image(0, 0, anchor='nw', image=query_image)
    # Display similar images in canvas
    image_size = (200, 200)
    spacing = 40

    similar_canvas.image_references = []  # Initialize list for image references

    for i, image in enumerate(similar_images):
        x = (i % 5) * (200 + spacing) + 20
        y = (i // 5) * (200 + spacing) + 20
        print(x, y)
        similar_image_name = str(image[1]).split('.')
        image = cv2.imread(os.path.join('images', f"{similar_image_name[0]}.jpg"))
        # Resize image for display
        image_resized = cv2.resize(image, image_size)
        # Convert image to PIL format
        image_pil = Image.fromarray(cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB))
        # Convert image to PhotoImage format
        image_tk = ImageTk.PhotoImage(image_pil)
        # Display image in canvas
        similar_canvas.create_image(x, y, anchor='nw', image=image_tk)

        similar_canvas.image_references.append(image_tk)


# Define function to update image in GUI window
def update_image(image_path):
    global query_image
    # Load image using OpenCV
    image = cv2.imread(image_path)
    # Resize image for display
    image_resized = cv2.resize(image, (200, 200))
    # Convert image to PIL format
    image_pil = Image.fromarray(cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB))
    # Convert image to PhotoImage format
    query_image = ImageTk.PhotoImage(image_pil)
    # Display image in GUI
    query_canvas.create_image(0, 0, anchor='nw', image=query_image)


# Define function to handle button click event
def browse_image():
    # Open file dialog to select query image
    global query_image_file_path
    file_path = filedialog.askopenfilename()

    if file_path is None or len(file_path) == 0:
        return

    query_image_file_path = file_path
    update_image(file_path)


def load_database_features():
    s_time = time.time()
    global df
    df = pd.read_csv('database_features.csv')
    e_time = time.time()  # 10 minutes

    print(e_time - s_time)


# Define function to create GUI window
def create_window():
    # Create window
    window = tk.Tk()

    # Set window title and size
    window.title('Content-Based Image Retrieval')
    print(window.winfo_screenwidth(), window.winfo_screenheight())
    window.geometry('1000x1000')

    # Create a canvas widget
    canvas = tk.Canvas(window, width=1000, height=1000, bg="white")

    # Create a scrollbar widget
    scrollbar = Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)

    # Set the scrollbar to control the y-axis of the canvas
    canvas.config(yscrollcommand=scrollbar.set)

    # Create a frame to contain the contents of the canvas
    frame = tk.Frame(canvas, bg="white", width=1000, height=1000)

    # canvas.create_window((0, 0), window=frame, anchor='center', tags='frame')
    # Add canvas to display images
    global query_canvas, query_canvas_images, similar_canvas, similar_canvas_images

    heading_label = tk.Label(frame, text="CONTENT BASED IMAGE RETRIEVAL", bg="white", font=('Arial', 20))
    heading_label.pack(side=tk.TOP, pady=10)

    # Add button to browse for query image
    button_browse = tk.Button(frame, text='Browse image', command=browse_image, padx=10, pady=5)
    button_browse.pack(side=tk.TOP, padx=10, pady=10)

    query_image_label = tk.Label(frame, text="Query Image", bg="white", font=('Arial', 14))
    query_image_label.pack(side=tk.TOP)

    query_canvas = tk.Canvas(frame, width=200, height=200, bg="white", highlightthickness=0)
    query_canvas.pack(side=tk.TOP, padx=50, pady=10)

    button_fetch = tk.Button(frame, text='Fetch results', command=update_similar_images, padx=10, pady=5)
    button_fetch.pack(side=tk.TOP, padx=10, pady=10)

    similar_images_label = tk.Label(frame, text="Retrieved Similar Images", bg="white", font=('Arial', 18))
    similar_images_label.pack(side=tk.TOP, pady=10)

    similar_canvas = tk.Canvas(frame, width=window.winfo_screenwidth() - 200, height=window.winfo_screenheight() / 1.5,
                               bg="white", highlightthickness=0)
    similar_canvas.pack(side=tk.LEFT, padx=50)

    # Place the frame inside the canvas
    canvas.create_window((0, 0), window=frame, anchor='nw')

    # Configure the canvas to resize along with the window
    frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    # Pack the canvas and scrollbar widgets
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    global times
    if times == 1:
        load_database_features()
        times -= 1

    # Run main loop for GUI window
    window.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_window()

    # img = cv2.imread(os.path.join('images', '999.jpg'))
    # print(img.shape)

    # image_1_lbp = convert_img('340.jpg') # 1-D feature vector of image1
    # image_2_lbp = convert_img('603.jpg')

    # arr = np.asarray([[7, 8, 9], [5, 8, 9]])
    # pd.DataFrame(arr).to_csv('sample.csv')

    # 340 and 341 -> 2400 # Euclidean
    # 340 and 304 -> 6177
    # 340 and 16 -> 5988
    # 35 and 16 -> 2997

    # 340 and 341 -> 0.987678 # Cosine
    # 340 and 304 -> 0.956339
    # 340 and 16 -> 0.922068
    # 35 and 16 -> 0.979881

    # print(image_1_lbp)
    # print(image_2_lbp)

    # print("LBP Program is finished")

    # d = cosine(image_1_lbp, image_2_lbp)

    # img_1_bgr = cv2.imread('340.jpg')
    # img_2_bgr = cv2.imread('35.jpg')

    # 340 and 341 -> 0.4034117
    # 340 and 304 -> 0.626891
    # 340 and 16 -> 1.1522042
    # 35 and 16 -> 1.0758427

    # d = calculate_color_moment(img_1_bgr, img_2_bgr)
    #
    # print("Color Moment distance is: ", d)
    # print("Euclidean distance is: ", d)
