#!/user/bin/python
# -*- coding:utf-8 -*-
import requests, xlrd,MySQLdb, time, sys
from xlutils import copy

def readExcel(file_path):
    '''''
    读取excel测试用例的函数
    :param file_path:传入一个excel文件，或者文件的绝对路径
    :return:返回这个excel第一个sheet页中的所有测试用例的list
    '''
    try:
        book = xlrd.open_workbook(file_path)  # 打开excel
    except Exception, e:
        # 如果路径不在或者excel不正确，返回报错信息
        print '路径不在或者excel不正确', e
        return e
    else:
        sheet = book.sheet_by_index(0)
        rows = sheet.nrows
        case_list = []
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
        if method.upper() == 'GET':
            if param == '':
                new_url = url  # 请求报文
                request_urls.append(new_url)
            else:
                new_url = url + '?' + urlParam(param)  # 请求报文
                request_urls.append(new_url)
            results = requests.get(new_url).text
            responses.append(results)
            res = readRes(results, res_check)
        else:
            headers={"Content-Type":"application/x-www-form-urlencoded"}
            print type(param)
            print  param
            data = eval(param)
            results = requests.post(url,data,headers=headers).text
            print results
            responses.append(results)
            request_urls.append(url)
            res = readRes(results, res_check)

        if 'pass' in res:
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
    res = res.replace('":"', "=").replace('":', "=")
    res_check = res_check.split(';')
    for s in res_check:
        if s in res:
            pass
        else:
            print '错误，返回参数和预期结果不一致' + str(s)
            return '错误，返回参数和预期结果不一致' + str(s)
    return 'pass'


def urlParam(param):
    return param.replace(';', '&')


def copy_excel(file_path, res_flags, request_urls, responses):
    '''''
    :param file_path: 测试用例的路径
    :param res_flags: 测试结果的list
    :param request_urls: 请求报文的list
    :param responses: 返回报文的list
    :return:
    '''
    book = xlrd.open_workbook(file_path)
    new_book = copy.copy(book)
    sheet = new_book.get_sheet(0)
    i = 1
    for request_url, response, flag in zip(request_urls, responses, res_flags):
        sheet.write(i, 8, u'%s' % request_url)
        sheet.write(i, 9, u'%s' % response)
        sheet.write(i, 11, u'%s' % flag)
        i += 1
        # 写完之后在当前目录下(可以自己指定一个目录)保存一个以当前时间命名的测试结果，time.strftime()是格式化日期
    new_book.save(u'%s_测试结果.xls' % time.strftime('%Y%m%d%H%M%S'))


# def writeBug(bug_id, interface_name, request, response, res_check):
#     '''''
#     这个函数用来连接数据库，往bugfree数据中插入bug，拼sql，执行sql即可
#     :param bug_id: bug序号
#     :param interface_name: 接口名称
#     :param request: 请求报文
#     :param response: 返回报文
#     :param res_check: 预期结果
#     :return:
#     '''
#     bug_id = bug_id.encode('utf-8')
#     interface_name = interface_name.encode('utf-8')
#     res_check = res_check.encode('utf-8')
#     response = response.encode('utf-8')
#     request = request.encode('utf-8')
#     '''''
#     因为上面几个字符串是从excel里面读出来的都是Unicode字符集编码的，
#     python的字符串上面指定了utf-8编码的，所以要把它的字符集改成utf-8，才能把sql拼起来
#     encode方法可以指定字符集
#     '''
#     # 取当前时间，作为提bug的时间
#     now = time.strftime("%Y-%m-%d %H:%M:%S")
#     # bug标题用bug编号加上接口名称然后加上_结果和预期不符，可以自己随便定义要什么样的bug标题
#     bug_title = bug_id + '_' + interface_name + '_结果和预期不符'
#     # 复现步骤就是请求报文+预期结果+返回报文
#     step = '[请求报文]<br />' + request + '<br/>' + '[预期结果]<br/>' + res_check + '<br/>' + '<br/>' + '[响应报文]<br />' + '<br/>' + response
#     # 拼sql，这里面的项目id，创建人，严重程度，指派给谁，都在sql里面写死，使用的时候可以根据项目和接口
#     # 来判断提bug的严重程度和提交给谁
#     sql = "INSERT INTO `bf_bug_info` (`created_at`, `created_by`, `updated_at`, `updated_by`, `bug_status`, `assign_to`, `title`, `mail_to`, `repeat_step`, `lock_version`, `resolved_at`, `resolved_by`, `closed_at`, `closed_by`, `related_bug`, `related_case`, `related_result`, " \
#           "`productmodule_id`, `modified_by`, `solution`, `duplicate_id`, `product_id`, " \
#           "`reopen_count`, `priority`, `severity`) VALUES ('%s', '1', '%s', '1', 'Active', '1', '%s', '系统管理员', '%s', '1', NULL , NULL, NULL, NULL, '', '', '', NULL, " \
#           "'1', NULL, NULL, '1', '0', '1', '1');" % (now, now, bug_title, step)
#     # 建立连接，使用MMySQLdb模块的connect方法连接mysql，传入账号、密码、数据库、端口、ip和字符集
#     coon = MySQLdb.connect(user='root', passwd='123456', db='bugfree', port=3306, host='127.0.0.1', charset='utf8')
#     # 建立游标
#     cursor = coon.cursor()
#     # 执行sql
#     cursor.execute(sql)
#     # 提交
#     coon.commit()
#     # 关闭游标
#     cursor.close()
#     # 关闭连接
#     coon.close()


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError, e:
        print 'Please enter a correct testcase! \n e.x: python gkk.py test_case.xls'
    else:
        readExcel(filename)
    print 'success!'