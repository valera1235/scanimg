from doctr.models import ocr_predictor
model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn')
result = model(['document.jpg'])
print(result.export()['words'])  # Список распознанных слов/чисел
