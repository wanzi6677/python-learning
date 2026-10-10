from lxml import html

#读取html文件
with open("resources/img/tiobe.html","r",encoding="utf-8") as  f:
    html_text = f.read()

    #解析html文本
    document = html.fromstring(html_text)

    #解析表头-xpath语法
    th_list = document.xpath("//table/thead/tr/th/text()")
    print(th_list)

    td_list = document.xpath("//table/tbody/tr[last()]/td/text()")
    print(td_list)

    #p[@color]:表示匹配class属性为p的标签
    p_list = document.xpath("//p[@color]/text()")
    print(p_list)

    tr_list = document.xpath("//thead/tr/*/text()")
    print(tr_list)