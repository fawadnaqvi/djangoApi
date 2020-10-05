from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# Create your views here.



img_height, img_width = 50,50
#with open('./models/labels.json', 'r') as l:
#    labelinfo = l.read()

#labelinfo = json.loads(labelinfo)



def index(request):
    context = {'a':1}
    return render(request, 'index.html', context)

def predictimage(request):
    print(request)
    fileobj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileobj.name, fileobj)
    filePathName = fs.url(filePathName)

    import numpy as np
    from keras.models import load_model
    import cv2

    model = load_model('./models/basic_cnn_model.h5')
    print(model.summary())
    test_image = './media'+filePathName
    print(test_image)
    test_image = cv2.imread(test_image, 0)
    test_image = cv2.resize(test_image,(50,50))
    test_image = np.reshape(test_image,[1,50,50,1])

    classes = model.predict_classes(test_image)
    print (classes)
    classes = classes[0, 0]
    if classes == 0:
        class_name = 'Benign'
    elif classes == 1:
        class_name = 'Malignant'

    predictedLabel = class_name

    context = {'filePathName':filePathName, 'predictedLabel':predictedLabel}
    return render(request, 'index.html', context)