import json
import execjs
import requests
from pprint import pprint
from random_word import random_word

# JS code from fanyi.baidu.com
# Core code is function e(r) which computes the word sign.
# One change has been made to replace window[l] into "320305.131321201" which represents window['gbk']
def get_sign(word):
    JsData = execjs.compile("""
    function a(r) {
        if (Array.isArray(r)) {
            for (var o = 0,
            t = Array(r.length); o < r.length; o++) t[o] = r[o];
            return t
        }
        return Array.from(r)
    }
    function n(r, o) {
        for (var t = 0; t < o.length - 2; t += 3) {
            var a = o.charAt(t + 2);
            a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
            a = "+" === o.charAt(t + 1) ? r >>> a: r << a,
            r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
        }
        return r
    }
    function e(r) {
        var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
        if (null === o) {
            var t = r.length;
            t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr( - 10, 10))
        } else {
            for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)"" !== e[C] && f.push.apply(f, a(e[C].split(""))),
            C !== h - 1 && f.push(o[C]);
            var g = f.length;
            g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice( - 10).join(""))
        }
        var u = void 0,
        l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
        u = null !== i ? i: (i = "320305.131321201" || "") || "";
        for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
            var A = r.charCodeAt(v);
            128 > A ? S[c++] = A: (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)), S[c++] = A >> 18 | 240, S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224, S[c++] = A >> 6 & 63 | 128), S[c++] = 63 & A | 128)
        }
        for (var p = m,
        F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++) p += S[b],
        p = n(p, F);
        return p = n(p, D),
        p ^= s,
        0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
        p.toString() + "." + (p ^ m)
    }
    var i = null;
    """.encode('utf-8', 'ignore').decode()).call("e", word)
    return JsData

# A legal header
headers = {
   'Accept': '*/*',
   'Accept-Encoding': 'gzip, deflate, br',
   'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3',
   'Cache-Control': 'max-age=0',
   'Content-Length': '105',
   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
   'Cookie': 'from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; FANYI_WORD_SWITCH=1; DOUBLE_LANG_SWITCH=1; SOUND_SPD_SWITCH=1; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; ZD_ENTRY=bing; delPer=0; H_PS_PSSID=1456_21126_29568_29221_22160; BAIDUID=8CF1134B0384C49FC42883861B095004:FG=1; BIDUPSID=8CF1134B0384C49FC42883861B095004; PSTM=1529043352; yjs_js_security_passport=f8c1acad087729606ba0115bcda8b27bf5d5302a_1574736663_js; MCITY=-%3A; __yjsv5_shitong=1.0_7_7f973d3692894b3577f17d1ae21971319458_300_1574737785347_103.254.68.231_2f34aaa5',
   'DNT': '1',
   'Host': 'fanyi.baidu.com',
   'Origin': 'https://fanyi.baidu.com',
   'Referer': 'https://fanyi.baidu.com/',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
   'X-Requested-With': 'XMLHttpRequest',
}


# Checkout the word online
def checkout_word(word):
    # URL of baidu fanyi api
    url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
    # Data for requesting word explains
    data = {
        'from': 'en',
        'query': word,
        'sign': get_sign(word),
        'simple_means_flag': '3',
        'to': 'zh',
        'token': 'fd4a3033d0f473dfeee1a4974482f799'
    }
    # Fetch raw response
    res = requests.post(url, headers=headers, data=data)
    # Load raw explain using json.loads
    explain = json.loads(res.content)
    # Return raw explain, a dict contains ['trans_result', 'dict_result', 'liju_result' , 'logid']
    return explain

# Dumps word explain, for each *_result entry in raw explain
def dumps_word_explain(explain):
    explain_dumps = dict()
    for result in explain:
        # Only interested in *_result entry
        if not result.endswith('_result'):
            continue
        # Dumps explain
        for name in explain[result]:
            explain_dumps['_'.join([result, name])] = json.dumps(explain[result][name])
    return explain_dumps

def parse_explain_dumps(explain_dumps):
    good_explain = explain_dumps.copy()
    for name in explain_dumps:
        print(name)
        if name in [
            'trans_result_from',
            'trans_result_status',
            'trans_result_to',
            'trans_result_type',
            ]:
            good_explain.pop(name)

        if name == 'dict_result_collins':
            mydict = json.loads(explain_dumps[name])
            # pprint(mydict)
            block = []
            block.append('<div style="border:1px solid red;"><ol>')
            for entry in mydict['entry']:
                print('-' * 80)
                pprint(entry)
                if entry['type'] == 'boxr':
                    block.append('<div style="border:1px solid blue">')
                    block.append('<p>{}</p>'.format(entry['value'][0]['boxr_value']))
                    block.append('</div>')
                if entry['type'] == 'mean':
                    block.append('<li>{}, {}</li>'.format(entry['value'][0]['posp'][0]['label'], entry['value'][0]['tran']))
                    block.append('<p>{}</p>'.format(entry['value'][0]['def']))
                    block.append('<ul>')
                    for example in entry['value'][0]['mean_type']:
                        example_dict = example['example'][0]
                        block.append('<li>{}</li><p>{}</p>'.format(example_dict['ex'], example_dict['tran']))
                    block.append('</ul>')
                if entry['type'] == 'rnon':
                    block.append('<div style="border:1px solid green"><ul>')
                    for mean in entry['value'][0]['mean']:
                        for mean_type_dict in mean['mean_type']:
                            example_dict = mean_type_dict['example'][0]
                            block.append('<li><b>{}</b></li><p>{}</p><p>{}</p>'.format(entry['value'][0]['head_word'], example_dict['ex'], example_dict['tran']))
                    block.append('</ul></div>')

            block.append('</ol></div>')
            good_explain[name] = '\n'.join(block)

        if name == 'trans_result_data':
            mydict = json.loads(explain_dumps[name])[0]
            # print(mydict)
            block = []
            block.append('<div style="border:1px solid red;">')
            block.append('{}, {}'.format(mydict['src'], mydict['dst']))
            block.append('</div>')
            good_explain[name] = '\n'.join(block)

        if name == 'trans_result_phonetic':
            mylist = json.loads(explain_dumps[name])
            # print(mylist)
            block = []
            block.append('<div style="border:1px solid red;">')
            block.append('<p>{}</p>'.format(' '.join([e['src_str'] for e in mylist])))
            block.append('<p>{}</p>'.format(' '.join([e['trg_str'] for e in mylist])))
            block.append('</div>')
            good_explain[name] = '\n'.join(block)


        if name == 'dict_result_edict':
            mydict = json.loads(explain_dumps[name])
            # print(mydict)
            block = []
            block.append('<div style="border:1px solid red;"><ol>')
            for entry in mydict['item'][0]['tr_group']:
                # tr
                block.append('<li>{}</li>'.format(entry['tr'][0]))
                # example
                block.append('<ul>')
                [block.append('<li>{}</li>'.format(e)) for e in entry['example']]
                block.append('</ul>')
                # similar_word
                if entry['similar_word']:
                    block.append('<p>Synonym: {}</p>'.format(', '.join(entry['similar_word'])))
            block.append('</ol></div>')
            good_explain[name] = '\n'.join(block)

    return good_explain

# Very backend explainer of the given word.
# Continuely improve.
def explain_word(word):
    return parse_explain_dumps(dumps_word_explain(checkout_word(word)))

if __name__ == '__main__':
    word = random_word()
    pprint(explain_word(word))