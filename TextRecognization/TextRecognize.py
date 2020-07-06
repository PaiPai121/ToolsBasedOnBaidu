from aip import AipOcr ## 引用OCR识别的api

class TextRecognition:
    def __init__(self,app_id,api_key,secret_key):
        ## 用自己申请到的app id等内容初始化AipOcr
        self.aipOcr = AipOcr(app_id,api_key,secret_key)

        """ 读取图片 """
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()


    def imageToText(self,path):
        ## 将path对应的图片转换为文字
        image = self.get_file_content(path)
        
        ### 可选参数
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"
        result = self.aipOcr.webImage(image, options)
        self.result = result
        return result
    
    def SplicingText(self):
        text = ""
        for res in self.result['words_result']:
            text += res['words']
        # print (text)
        return text

