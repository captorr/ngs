"""
Author: Zhang Chengsheng, @2018.04.16
"""
import re
import requests
import execjs
from bs4 import BeautifulSoup as BS

class translate():
    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 
    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)
        self.google_website = 'https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&' #tk=803156.668870&q=
    def getTk(self, text):
        return self.ctx.call("TL", text)

    def string_modify(self,text):
        text = str(text)
        text = text.replace(' ', '%20')
        text = text.replace('\n', '%0A')
        text = text.replace(',', '%2C')
        return str(text)

    def get_url(self,text):
        addition = self.string_modify(text)
        tk = self.getTk(text)
        addition = 'tk=' + str(tk) + '&q=' + addition
        url = self.google_website + addition
        return str(url)

    def get_translation(self,url):
        rq = requests.get(url=url)
        res = BS(rq.content,'lxml')
        res_string = str(res.string)
        res_translate_list = re.findall('(\[.*?\])',res_string)
        text_line = []
        for i in res_translate_list:
            if i.startswith('[null,null'):
                break
            else:
                text = re.findall('"(.*?)"', i)
                text_line.append(text[0])
        translation = str(''.join(text_line))
        return translation

    def CN_translate(self,text):
        url = self.get_url(text)
        res = self.get_translation(url)
        return res


#foo = translate()
#test1 = 'I`m zhang. open reading frames (uORFs) are major gene expression regulatory elements. In many eukaryotic mRNAs, one or more uORFs precede the initiation codon of the main coding region.'
#bar = foo.CN_translate(test1)
#print(bar)







