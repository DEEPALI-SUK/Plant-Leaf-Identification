import pickle
import numpy as np
import mahotas as mt
import pandas as pd
import os
import cv2
from sklearn.preprocessing import StandardScaler

__model = None


def feature_extract(file_list):
    attributes= ['area', 'perimeter', 'length', 'width', 'aspect_ratio', 'rectangularity', 'circularity', 'mean_r',
             'mean_g', 'mean_b', 'stdd_r', 'stdd_g', 'std_b', 'contrast', 'correlation', 'inverse_difference_moments',
             'entropy']
    dataframe = pd.DataFrame([], columns=attributes)
    for f_name in file_list:
        imgpath = './static/Uploads/'+f_name
        main_image = cv2.imread(imgpath)

        image = cv2.cvtColor(main_image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (25, 25), 0)
        ret_otsu, im_bw_otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((50, 50), np.uint8)
        closing = cv2.morphologyEx(im_bw_otsu, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        M = cv2.moments(cnt)
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        p, q, r, s = cv2.boundingRect(cnt)
        aspect_ratio = float(r) / s
        rectangularity = r * s / area
        circularity = ((perimeter) ** 2) / area

        red = image[:, :, 0]
        green = image[:, :, 1]
        blue = image[:, :, 2]
        blue[blue == 255] = 0
        green[green == 255] = 0
        red[red == 255] = 0

        mean_r = np.mean(red)
        mean_g = np.mean(green)
        mean_b = np.mean(blue)

        stdd_r = np.std(red)
        stdd_g = np.std(green)
        stdd_b = np.std(blue)

        texture = mt.features.haralick(gray)
        ht_mean = texture.mean(axis=0)
        contrast = ht_mean[1]
        correlation = ht_mean[2]
        inverse_diff_moments = ht_mean[4]
        entropy = ht_mean[8]


        vector = [area, perimeter, r, s, aspect_ratio, rectangularity, circularity, mean_r, mean_g, mean_b, stdd_r,
                  stdd_g, stdd_b, contrast, correlation, inverse_diff_moments, entropy]

        temp = pd.DataFrame([vector], columns=attributes)
        dataframe = dataframe.append(temp)
    return dataframe

def get_expense(file_list):
    img_list = feature_extract(file_list)
    std_scaler = StandardScaler()
    scaled_features = std_scaler.fit_transform(img_list)
    y_pred = __model.predict(scaled_features)
    names = ['pubescent bamboo', 'Chinese horse chestnut', 'Anhui Barberry', 'Chinese redbud', 'true indigo', 'Japanese maple', 'Nanmu', ' castor aralia', 'Chinese cinnamon', 'goldenrain tree', 'Big-fruited Holly', 'Japanese cheesewood', 'wintersweet', 'camphortree', 'Japan Arrowwood', 'sweet osmanthus', 'deodar','ginkgo, maidenhair tree', 'Crape myrtle, Crepe myrtle', 'oleander', 'yew plum pine', 'Japanese Flowering Cherry','Glossy Privet', 'Chinese Toon', 'peach', 'Ford Woodlotus', 'trident maple', 'Beales barberry', 'southern magnolia', 'Canadian poplar', 'Chinese tulip tree', 'tangerine']
    res=[]
    for i in y_pred:
        res.append(names[i])
    return res


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __model
    if __model is None:
        with open('./artifacts/Leaf_classification_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

if __name__ == '__main__':
    load_saved_artifacts()


