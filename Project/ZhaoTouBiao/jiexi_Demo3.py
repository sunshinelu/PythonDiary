from lxml import etree


def run_123():
    parser = etree.HTMLParser(encoding="utf-8")
    html = etree.parse('123.txt', parser=parser)
    p_seletors = html.xpath('//*[@class="vF_detail_content"]/*')
    p_list = []
    for p_seletor in p_seletors:
        p_content = p_seletor.xpath('.//text()')
        p_content = map(lambda x: x.strip(), p_content)
        p_content = "".join(p_content)
        # print(p_content)
        p_list.append(p_content)
    file_content = '\n'.join(p_list)
    print(file_content)


def run_456():
    parser = etree.HTMLParser(encoding="utf-8")
    html = etree.parse('456.txt', parser=parser)
    table_seletors = html.xpath('//table//tr')
    p_list = []
    for table_seletor in table_seletors:
        p_content = table_seletor.xpath('.//text()')
        p_content = map(lambda x: x.strip(), p_content)
        p_content = "".join(p_content)
        p_list.append(p_content)
        #print(p_content)
    file_content = '\n'.join(p_list)
    print(file_content)


if __name__ == '__main__':
    run_123()
    # run_456()
