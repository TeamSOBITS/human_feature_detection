#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
# file_path = '/home/yochiai/catkin_ws/src/fashion_tagging/scripts/test_watch'
file_path = '/home/sobits/catkin_ws/src/amazon_recognition_for_fmm/imgs/trimming.jpg'
API_Key = 'DE7GaugVxa883rkfa8SQs4ySpgxkpldc4FJ4opVu'
timeout_times = 25 # 0 <= n <= 25 の範囲
label_lang = 'en'  #defaultは日本語; Englishは'en'で指定

# L_categ = [ #categoryの項目
#     'dress', 'tops',              #TOPS
#     'bottoms', 'leg_wear',        #BOTTOMS
#     'accessory', 'stole', 'hat', 'hair_accessory', 'glasses'      #ACCESSORIES
# ]

# L_**=[list] は要素数と順番は同じにすること！"ja"から"en"に戻す際に間違ったラベルが返されます
L_colors = [
    'ブラック', 'ホワイト', 'ベージュ', 'ブラウン', 'グレー', 'ブルー', 'ネイビー', 'シルバー',
    'ピンク', 'レッド', 'ゴールド', 'グリーン', 'イエロー', 'カーキ', 'キャメル',
    'インディゴブルー', 'ライトブルー', 'パープル', 'オレンジ', 'クリア', 'バイカラー',
    'アイボリー', 'グレージュ', 'ボルドー', 'ラベンダー', 'ミント', 'ライトグレー', 'オフホワイト',
    'ピンクベージュ', 'マスタード', 'イエローグリーン', 'マルチカラー', 'テラコッタ',
    'チャコールグレー', 'ライトグリーン', 'サックスブルー', 'ワインレッド', 'ターコイズ', 
    'モスグリーン', 'スカイブルー', 'モカ', 'パステルピンク', 'ライトピンク', 'メタリック',
    'ダークグレー', 'ショッキングピンク', 'ダークブラウン', 'ダスティピンク', 'ピンクゴールド',
    'ライトベージュ', 'ダークグリーン', 'ライトパープル', 'ダスティブルー', 'パステル',
    'グラデーション', 'サックス', 'ピスタチオグリーン', 'サーモンピンク', 'ブルーグレー',
    'パステルブルー', '配色', 'パステルイエロー', 'スモーキーピンク', 'ロイヤルブルー',
    'アイスグレー', 'クリーム'
]
L_en_colors = [
    'black', 'white', 'beige', 'brown', 'gray', 'blue', 'navy', 'silver',
    'pink', 'red', 'gold', 'green', 'yellow', 'khaki', 'camel',
    'indigo blue', 'light blue', 'purple', 'orange', 'clear', 'bicolor',
    'ivory', 'graige', 'bordeaux', 'lavender', 'mint', 'light gray', 'off-white',
    'pink beige', 'mustard', 'yellow green', 'multicolor', 'terracotta',
    'charcoal gray', 'light green', 'sax blue', 'wine red', 'turquoise',
    'moss green', 'sky blue', 'mocha', 'pastel pink', 'light pink', 'metallic',
    'dark gray', 'shocking pink', 'dark brown', 'dusty pink', 'pink gold',
    'light beige', 'dark green', 'light purple', 'dusty blue', 'pastel',
    'gradation', 'sax', 'pistachio green', 'salmon pink', 'blue gray',
    'pastel blue', 'color scheme', 'pastel yellow', 'smoky pink', 'royal blue',
    'ice gray', 'cream'
]
L_tops = [
    'コート', 'トレンチコート', 'マウンテンパーカー', 'ポンチョ', 'ダッフルコート',
    'コーディガン', 'ウィンドブレーカー', 'モッズコート', 'ガウンコート', 'スプリングコート',
    'フーデットコート', 'ライトアウター', 'チェスターコート', 'ロングカーディガン', 'Pコート',
    'ダウン', 'ガウン', 'ジャケット', 'ブルゾン', 'ライダースジャケット', 'テーラードジャケット',
    'ミリタリージャケット', 'シャツジャケット', 'MA-1', 'テーラード', 'スタジャン', 'ジャンパー',
    'CPO', 'ボレロ', 'カーディガン', 'プルオーバー', 'Tシャツ', 'ブラウス', 'シャツ', 'カットソー',
    'パーカー', 'タンクトップ', 'カシュクール', 'スキッパー', 'ワンショルダー', 'フランネルシャツ', 
    '開襟シャツ', 'ブラトップ', 'スキッパーシャツ', 'ダンガリーシャツ', 'チルデンニット',
    'キャミソール', 'セーター', 'ベスト', 'チュニック', 'チューブトップ', 'ポロシャツ', 'ワイシャツ',
    'ビスチェ', 'ワンピース', 'オールインワン', 'セットアップ', 'シャツワンピース', 'オーバーオール',
    'タイトワンピース', 'スーツ', 'サロペット', 'ドレス', 'ウエディングドレス', '浴衣', '着物'
]
L_en_tops = [
    'coat', 'trench coat', 'mountain parka', 'poncho', 'duffle coat', 
    'cordigan', 'windbreaker', 'mod coat', 'gown coat', 'spring coat', 
    'hooded coat', 'Light outerwear', 'chester coat', 'long cardigan', 'p coat', 
    'down', 'gown', 'jacket', 'blouson', 'rider\'s jacket', 'tailored jacket', 
    'military jacket', 'shirt jacket', 'ma-1', 'tailored', 'stadium jacket', 'jumper', 
    'cpO', 'bolero', 'cardigan', 'pullover', 't-shirt', 'blouse', 'shirt', 'cut sew', 
    'hoodie', 'tank top', 'cache-coeur', 'skipper', 'one shoulder', 'flannel shirt', 
    'open collar shirt', 'bra top', 'skipper shirt', 'dungaree shirt', 'tilden knit', 
    'camisole', 'sweater', 'vest', 'tunic', 'tube top', 'polo shirt', 'shirt', 
    'bustier', 'dress', 'all in one', 'setup', 'shirt dress', 'overall', 
    'tight dress', 'suit', 'salopette', 'dress', 'wedding dress', 'yukata', 'kimono','T-shirt','short-sleeve',
    'crew neck','long-sleeve'
]
L_bottoms = [
    'スカート', 'タイトスカート', 'フレアスカート', 'ギャザースカート', 'ジャンパースカート',
    'ラップスカート', 'ティアードスカート', 'サーキュラースカート', 'マーメイドスカート', 'パンツ',
    'ショートパンツ', 'ガウチョパンツ', 'フレアパンツ', 'ハーフパンツ', 'ボディバッグ', 'チノパンツ',
    'レギンスパンツ', 'スラックス', 'キュロット', 'クロップドパンツ', 'スポーツショーツ',
    'ベイカーパンツ', 'カーゴパンツ', 'カラーパンツ', 'バギーパンツ', 'イージーパンツ', 
    'トラックパンツ', 'サルエルパンツ', 'ジョガーパンツ', 'ボーイフレンド', 'タイツ', 'レギンス',
    'ストッキング', 'スポーツタイツ'
]
L_en_bottoms = [
    'skirt', 'tight skirt', 'flare skirt', 'dirndl skirt', 'jumper skirt', 
    'wrap skirt', 'tiered skirt', 'circular skirt', 'mermaid skirt', 'pants', 
    'shorts', 'gaucho pants', 'flare pants', 'half pants', 'body bag', 'chino pants', 
    'legging pants', 'slacks', 'culottes', 'cropped pants', 'sports shorts', 
    'baker pants', 'cargo pants', 'colored pants', 'baggy pants', 'easy pants', 
    'track pants', 'sarouel pants', 'jogger pants', 'boyfriend', 'tights', 'leggings', 
    'stockings', 'sports tights'
]
L_accessories = [
    'イヤリング', 'ネックレス', 'リング', 'チョーカー', 'フープ', 'ピンキーリング', 'ボディピアス',
    'イヤーカフ', 'フープピアス', 'ピアス', 'ブレスレット', 'バングル', 'サングラス', 'メガネ',
    'ストール', 'スカーフ', 'マフラー', 'スヌード', 'バンダナ', 'ボウタイ', 'ネクタイ', 'ヘアバンド',
    'ヘアピン', 'カチューシャ', 'ヘアゴム', 'ヘアアクセサリー', 'ヘアクリップ', 'バレッタ',
    'シュシュ', 'ターバン', 'ハット', 'キャップ', 'ベレー帽', 'ストローハット', '中折れ',
    'キャスケット', 'ニット帽', 'つば広ハット', 'バケットハット', 'カンカン帽',
    'ベースボールキャップ', 'マリンキャップ', 'サンバイザー', 'フェルトハット', 'フライトキャップ'
]
L_en_accessories = [
    'earrings', 'necklace', 'ring', 'choker', 'hoop', 'pinky ring', 'body piercing', 
    'ear cuffs', 'hoop earrings', 'earrings', 'bracelets', 'bangles', 'sunglasses', 'glasses', 
    'scarf', 'scarf', 'scarf', 'snood', 'bandana', 'bowtie', 'tie', 'headband', 
    'hairpin', 'headband', 'hair tie', 'hair accessory', 'hairclip', 'barrette', 
    'scrunchy', 'turban', 'hat', 'cap', 'beret', 'straw hat', 'broken', 
    'casquette', 'knitted hat', 'wide-brimmed hat', 'bucket hat', 'boarer hat', 
    'baseball cap', 'marine cap', 'sun visor', 'felt hat', 'flight cap'
]

#post request用関数
def request_POST(file_path):
    end_point = 'https://api.scnnr.cubki.jp/v1/recognitions'
    ## リクエスト
    headers = {
        'Content-Type': 'application/octet-stream',
        'x-api-key': API_Key,
        'accept-language': label_lang
    }
    # ファイルオープン
    try:
        with open(file_path, 'rb') as f:
           data = f.read()
    except FileNotFoundError:
        print("指定のパスにファイルが見つかりません")
        return
    # クエリパラメータ
    params = {
        'timeout': timeout_times,
        'thirdparty': 'microsoft-face'
    }
    response = requests.post(end_point, headers=headers, data=data, params=params)
    # print(response)
    return response

#翻訳用関数
def translate(name): # google
    end_point = 'https://script.google.com/macros/s/AKfycbxVNA_euX-6z1sQGDkPyQut7p0SOy-BwCZIrt-PUS_iqTYVOU6a9VK5yw3HWFhcrn2_/exec'
    params = {
        'text': name,
        'source': 'ja',
        'target': 'en'
    }
    response = requests.get(end_point, params=params)
    a=response.json()
    name=a['text']
    return name

#参考: ラベル抽出関数: rabelから色labelを抽出、色のlabel分類はリストから参照 
# def pick_up_color(labels, max_label_len):
#     #L_colorsに載っている名前のlabelを, color_listに抽出
#     color_list =[]
#     for i in range(max_label_len):
#         if labels[i]['name'] in L_colors:
#             color_list.append(labels[i])
#     #.sort()でscoreの降順ソート
#     color_list.sort(key=lambda x: x['score'], reverse=True)
#     print(color_list, '\n*******')
#     if color_list[0]['name'] in L_colors: #スコア最大のラベルが日本語の場合に英語にする
#         color_list[0]['name'] = L_en_colors[L_colors.index(color_list[0]['name'])]
#     #return
#     return color_list[0]['name']
    
def pick_up_tops(labels, max_label_len):
    #L_colors, L_topsに載っている名前のlabelを color_list, tops_listに抽出
    color_list =[]
    tops_list =[]
    print("labels:",labels)
    print("max_label_len",max_label_len)
    
    # 分類分け
    for i in range(max_label_len):
        if labels[i]['name'] in L_colors or labels[i]['name'] in L_en_colors:
            color_list.append(labels[i])
        if labels[i]['name'] in L_tops or labels[i]['name'] in L_en_tops:
            tops_list.append(labels[i])
    
    #.sort()でscoreの降順ソート
    color_list.sort(key=lambda x: x['score'], reverse=True)
    tops_list.sort(key=lambda x: x['score'], reverse=True)

    print("color_list:",color_list)
    print("tops_list:",tops_list)
    
    # labelの翻訳: スコア最大のラベルが日本語の場合に英語にする
    if re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+',color_list[0]['name']):
        color_list[0]['name']=translate(color_list[0]['name'])
    if re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+',tops_list[0]['name']):
        tops_list[0]['name']=translate(tops_list[0]['name'])
    
    # 上の服の色、上の服の種類を返す
    return color_list[0]['name'], tops_list[0]['name']

def pick_up_bottoms(labels, max_label_len):
    #L_colors, L_bottomsに載っている名前のlabelを color_list, bottoms_listに抽出
    color_list =[]
    bottoms_list =[]
    
    #分類分け
    for i in range(max_label_len):
        if labels[i]['name'] in L_colors or labels[i]['name'] in L_en_colors:
            color_list.append(labels[i])
        if labels[i]['name'] in L_bottoms  or labels[i]['name'] in L_en_bottoms:
            bottoms_list.append(labels[i])
    
    #.sort()でscoreの降順ソート
    color_list.sort(key=lambda x: x['score'], reverse=True)
    bottoms_list.sort(key=lambda x: x['score'], reverse=True)
    
    # labelの翻訳: スコア最大のラベルが日本語の場合に英語にする
    if re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+',color_list[0]['name']):
        color_list[0]['name']=translate(color_list[0]['name'])
    if re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+',bottoms_list[0]['name']):
        bottoms_list[0]['name']=translate(bottoms_list[0]['name'])
    
    # 下の服の色、下の服の種類を返す
    return color_list[0]['name'], bottoms_list[0]['name']

def pick_up_accessories(labels, max_label_len):
    #L_colors, L_accessoriesに載っている名前のlabelを color_list, accessories_listに抽出
    color_list =[]
    accessories_list =[]
    
    #分類分け
    for i in range(max_label_len):
        if labels[i]['name'] in L_colors or labels[i]['name'] in L_en_colors:
            color_list.append(labels[i])
        if labels[i]['name'] in L_accessories or labels[i]['name'] in L_en_accessories:
            accessories_list.append(labels[i])
    
    #.sort()でscoreの降順ソート
    color_list.sort(key=lambda x: x['score'], reverse=True)
    accessories_list.sort(key=lambda x: x['score'], reverse=True)
    
    # labelの翻訳: スコア最大のラベルが日本語の場合に英語にする
    if re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+',color_list[0]['name']):
        color_list[0]['name']=translate(color_list[0]['name'])
    if re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+',accessories_list[0]['name']):
        accessories_list[0]['name']=translate(accessories_list[0]['name'])
    
    #アクセサリーの色、アクセサリーの種類を返す
    return color_list[0]['name'], accessories_list[0]['name']
    
def pick_up_hair_color(color_list):
    color_list.sort(key=lambda x: x['confidence'], reverse=True)
    return color_list[0]['color']

def make_list(object_list, hair_list):
    max_categ = len(object_list)
    
    categ = [] #category分類用リスト、json_dataと同順
    label_len = [] #ラベルの最大要素数のリスト、categ[]と同順
    rt_list = [None,None,None,None,None] #出力用のリスト, 上の服の色、上の服の種類、下の服の色、下の服の種類, 髪の色
    sub_list = [] # 使われていないカテゴリの名前リスト
    #例外処理、カテゴリ数が0
    if max_categ == 0:
        if(hair_list != None):
            rt_list[4] = pick_up_hair_color(hair_list)
        return rt_list[0], rt_list[1], rt_list[2], rt_list[3], rt_list[4]
    
    #各カテゴリからラベルの分類&抽出
    for i in range(max_categ):
        categ.append(object_list[i]['category'])
        label_len.append(len(object_list[i]['labels']))
        if('tops' in categ[i] or 'dress' in categ[i]):
            #print('TOPS')
            rt_list[0], rt_list[1] = pick_up_tops(object_list[i]['labels'], label_len[i])
        elif('bottoms' in categ[i] or 'leg_wear' in categ[i]):
            #print('BOTTOMS')
            rt_list[2], rt_list[3] = pick_up_bottoms(object_list[i]['labels'], label_len[i])
        elif('accessory' in categ[i] or 'stole' in categ[i] or 'hat' in categ[i] or
             'hair_accessory' in categ[i] or 'glasses' in categ[i]):
            #print('ACCESSORIES')
            sub_list.append(pick_up_accessories(object_list[i]['labels'], label_len[i]))
    
    if(hair_list != None):
        rt_list[4] = pick_up_hair_color(hair_list)
    
    #print('各categoryのリスト; ',categ)
    #print('各categoryの要素数; ',label_len)
    
    # returnされるラベルは、最もスコアの高いラベル
    #print(rt_list)
    return rt_list[0], rt_list[1], rt_list[2], rt_list[3], rt_list[4]
    # (例) jsonファイルから bounding_box の抽出
    # print(json_data["objects"][0]["bounding_box"])

def main(file_path):
    #CBK_scnnrにrequest
    response = request_POST(file_path)
    if(response == None):
        return None, None, None, None, None
    ## 出力
    #requestステータスを表示: 200(検出した場合) or 202(検出されなかった場合)
    # print('CBK_API: status:',response.status_code,';')
    # 例外処理 202(結果なしの場合)
    if response.status_code != 200:
        print("APIレスポンス; ステータスエラー")
        return None, None, None, None, None
    
    #jsonの読み込み
    json_data = response.json()
    ## 例外処理 Error
    if 'error' in json_data:
        print('CBK scnnrエラー;\t', json_data['error']['title'])
    if not json_data['objects']:
        print('オブジェクトが未検出')
        return None, None, None, None, None
    # print(json_data['objects'])#ここで各特徴の確率を全て表示している
    
    if (json_data['thirdparty']['microsoft_face']['faces']):
        if(json_data['thirdparty']['microsoft_face']['faces'][0]['faceAttributes']):
            if(json_data['thirdparty']['microsoft_face']['faces'][0]['faceAttributes']['hair']['hairColor']):
                hair_list=json_data['thirdparty']['microsoft_face']['faces'][0]['faceAttributes']['hair']['hairColor']
    else:
        print('顔認識失敗; hair_colorなし')
        hair_list = None
    
    #label名の導出(検出されなかった場合、Noneが返される)
    tops_color, tops_name, bottoms_color, bottoms_name, hair_color = make_list(json_data["objects"], hair_list)
    return tops_color, tops_name, bottoms_color, bottoms_name, hair_color

if __name__ == "__main__":
    a = main('/home/sobits/catkin_ws/src/amazon_recognition_for_fmm/imgs/trimming.jpg')
    print(a)