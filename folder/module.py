import random

async def GenerateNickname():
    Name = ''
    for i in range(6):
        Name = Name + str(random.randint(0,9))
    return Name

def votepercent(a, b):
    if a == b:
        return 50, 50

    if a > b:
        a1 = round(b/(b+a) * 100)
        a2 = 100 - a1
        return a1, a2
    else:
        a1 = round(a/(a+b) * 100)
        a2 = round(100 - a1)
        return a2, a1

import re

JOSA_PAIRD = {
    u"(이)가" : (u"이", u"가"),
    u"(와)과" : (u"과", u"와"),
    u"(을)를" : (u"을", u"를"),
    u"(은)는" : (u"은", u"는"),
    u"(으)로" : (u"으로", u"로"),
    u"(아)야" : (u"아", u"야"),
    u"(이)여" : (u"이여", u"여"),
    u"(이)라" : (u"이라", u"라"),
}

JOSA_REGEX = re.compile(u"\(이\)가|\(와\)과|\(을\)를|\(은\)는|\(아\)야|\(이\)여|\(으\)로|\(이\)라")


def choose_josa(prev_char, josa_key, josa_pair):
    """
    조사 선택
    :param prev_char 앞 글자
    :param josa_key 조사 키
    :param josas 조사 리스트
    """
    char_code = ord(prev_char)

    # 한글 코드 영역(가 ~ 힣) 아닌 경우 
    if char_code < 0xac00 or char_code > 0xD7A3: 
        return josa_pair[1]

    local_code = char_code - 0xac00 # '가' 이후 로컬 코드
    jong_code = local_code % 28

    # 종성이 없는 경우
    if jong_code == 0: 
        return josa_pair[1]
        
    # 종성이 있는 경우
    if josa_key == u"(으)로":
        if jong_code == 8: # ㄹ 종성인 경우
            return josa_pair[1]

    return josa_pair[0]

def josa(src):
    tokens = []
    base_index = 0
    for mo in JOSA_REGEX.finditer(src):
        prev_token = src[base_index:mo.start()]
        prev_char = prev_token[-1]
        tokens.append(prev_token)

        josa_key = mo.group()
        tokens.append(choose_josa(prev_char, josa_key, JOSA_PAIRD[josa_key]))

        base_index = mo.end()

    tokens.append(src[base_index:])
    return ''.join(tokens)

if __name__ == '__main__':
    pass

