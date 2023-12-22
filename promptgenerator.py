import csv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def prompt_gen(feeling):

    prompt  = "幫我挑選以下合適的衣服搭配：\n"

    with open("data/clothes.csv", encoding="utf-8") as csvfile:
        clothes_list = csv.reader(csvfile)
        next(clothes_list)
        print("Successfully read csv file")
        for cloth in clothes_list:
            prompt += 'id: {0}, type: {1}, description: {2}\n'.format(cloth[0], cloth[2], cloth[3])

    prompt += "備註：{0}\n".format(feeling)

    prompt += "請從上述衣物以及備註內容推薦搭配，只能回答id數字，最多五項，以空格區隔\n"

    prompt += "“輸出範例：“2 4 3”"
        
    return prompt
