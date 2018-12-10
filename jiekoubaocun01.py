#!/user/bin/python
# -*- coding:utf-8 -*-
import requests, xlrd,MySQLdb, time, sys,json
from xlutils import copy
import math
import random
from M2Crypto import RSA, BIO
import base64
def readExcel(file_path):
    try:
        book = xlrd.open_workbook(file_path)  # 打开excel
    except Exception, e:
        print '路径不在或者excel不正确', e
        return e
    else:
        sheet = book.sheet_by_index(0)  # 取第一个sheet页
        rows = sheet.nrows  # 取这个sheet页的所有行数
        case_list = []  # 保存每一条case
        for i in range(rows):
            if i != 0:
                # 把每一条测试用例添加到case_list中
                case_list.append(sheet.row_values(i))
        interfaceTest(case_list, file_path)


def interfaceTest(case_list, file_path):
    res_flags = []
    # 存测试结果的list
    request_urls = []
    # 存请求报文的list
    responses = []
    # 存返回报文的list
    for case in case_list:
        ''''' 
        先遍历excel中每一条case的值，然后根据对应的索引取到case中每个字段的值 
        '''
        try:
            # 项目，提bug的时候可以根据项目来提
            product = case[0]
            # 用例id，提bug的时候用
            case_id = case[1]
            # 接口名称，也是提bug的时候用
            interface_name = case[2]
            # 用例描述
            case_detail = case[3]
            # 请求方式
            method = case[4]
            # 请求url
            url = case[5]
            # 入参
            param = case[6]
            # 预期结果
            res_check = case[7]
            # 测试人员
            tester = case[10]
            beuzhu = case [12]
        except Exception, e:
            return '测试用例格式不正确！%s' % e
        print case_id
        #登录后获取login_token
        # headers={"Content-Type":"application/x-www-form-urlencoded"}
        data1={"username":"18042311448",
               "password":"lGvH3DTGDmrN6pYnCHFqc2uGwpJ6kl22LUSxDnuzdbtIe1HIpPeWOLnjRwpNQ0rl+uU6kX2Rze38jIlaVYpDfGDt6fLklLvsseKfMMBrXiDaMSOEzNW/RUoZwTYCPJe5ABKCZhRF1CtG9kIHwNvohkqJPYiC61L3Le0r+75hPp4=",
               "device_id":"Ap_1tfkRWS6uF1Ugd7jh64TaDeCVtxW3p5GvrwzR5ZF"}
        url1="http://jdshop.shopjian.cn/public/index.php/api/index/login/dologin"

        results = requests.post(url=url1, data=data1,).text
        print"results shouci %s" %results

        results_json=json.loads(results)
        print "zheshi results_json :%s" %results_json
        content=results_json.get("content")
        for i in content:
            if i=='login_token':
                login_token_en=(content['login_token'])
                private_key_str = file('rsa_private.pem', 'rb').read()
                private_key = RSA.load_key_string(private_key_str)
                login_token = base64.decodestring(login_token_en)
                de_data = private_key.private_decrypt(login_token, RSA.pkcs1_padding)
                print "zheshi de_data %s" %de_data
                login_token_tr="{"+'"'+"login_token"+'"'+ ":" +'"'+ (de_data)+'"'+"}"
                login_token_json=eval(login_token_tr)

                if  param:
                    print "is none"
                    param_json=eval(param)
                    data =dict(login_token_json.items()+param_json.items())
                else:
                    print "no none"
                    data =login_token_json
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                results2 = requests.post(url=url,data=data,headers=headers).text

                print results2
                if len(results2)>32767:
                    responses.append("SYSTEM ERROR:LONG  LENGTH")
                else:
                    responses.append(results2)
                request_urls.append(url)
                res = readRes(results2, res_check)
                if 'pass' in res:
                    ''''' 
                    判断测试结果，然后把通过或者失败插入到测试结果的list中 
                    '''
                    res_flags.append('pass')
                else:
                    res_flags.append('fail')


            # writeBug(case_id, interface_name, new_url, results, res_check)
    copy_excel(file_path, res_flags, request_urls, responses)

def readRes(res, res_check):
    '''''
    :param res: 返回报文
    :param res_check: 预期结果
    :return: 通过或者不通过，不通过的话会把哪个参数和预期不一致返回
    '''
    #返回报文和预期结果进行对比 返回结果
    res = res.replace('":"', "=").replace('":', "=")
    res_check = res_check.split(';')
    for s in res_check:
        if s in res:
            pass
        else:
            print '错误，返回参数和预期结果不一致' + str(s)
            return '错误，返回参数和预期结果不一致' + str(s)
    return 'pass'

def copy_excel(file_path, res_flags, request_urls, responses):
    '''''
    :param file_path: 测试用例的路径
    :param res_flags: 测试结果的list
    :param request_urls: 请求报文的list
    :param responses: 返回报文的list
    :return:
    '''
    # 打开原来的excel，获取到这个book对象
    book = xlrd.open_workbook(file_path)
    # 复制一个new_book
    new_book = copy.copy(book)
    # 然后获取到这个复制的excel的第一个sheet页
    sheet = new_book.get_sheet(0)
    i = 1
    for request_url, response, flag in zip(request_urls, responses, res_flags):
        sheet.write(i, 8, u'%s' % request_url)
        sheet.write(i, 9, u'%s' % response)
        sheet.write(i, 11, u'%s' % flag)
        i += 1
        # 写完之后在当前目录下(可以自己指定一个目录)保存一个以当前时间命名的测试结果，time.strftime()是格式化日期
    new_book.save(u'%s_测试结果会员.xls' % time.strftime('%Y%m%d%H%M%S'))

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError, e:
        print 'Please enter a correct testcase! \n e.x: python gkk.py test_case.xls'
    else:
        readExcel(filename)
    print 'success1!'
    # try:
    #     filename = sys.argv[2]
    # except IndexError, e:
    #     print 'Please enter a correct testcase! \n e.x: python gkk.py test_case.xls'
    # else:
    #     readExcel(filename)
    # print 'success2!'