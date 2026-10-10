from lxml import html

#读取html文件
with open("resources/img/tiobe.html","r",encoding="utf-8") as  f:
    html_text = f.read()

    #解析html文本
    document = html.fromstring(html_text)

    #解析表头-xpath语法
    th_list = document.xpath("//table/thead/tr/th/text()")
    print(th_list)

    #解析表格中的数据-xpath语法
    #获取第一行
    # td_list = document.xpath("//table/tbody/tr[1]/td/text()")
    # print(td_list)

    #获取所有行数据
    tr_list = document.xpath("//table/tbody/tr")
    for tr in tr_list:
        td_list = tr.xpath("./td/text()")
        print(td_list)
