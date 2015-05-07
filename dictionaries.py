from flask import Flask, render_template, request
from requests import get
from lxml import html, etree


app = Flask(__name__)

DICTIONARIES_URLS = {
    'macmillan': "http://www.macmillandictionary.com/dictionary/british/%s"
}

@app.route('/')
def hello_world():
    if 'query' in request.values:
        page = get(DICTIONARIES_URLS['macmillan'] % request.values['query'])
        tree = html.fromstring(page.text)

        # text = tree.xpath(r'//ol[@class="senses"]/*[1]/*[1]/*[1]/span/*/text()')
        macmillan_main = tree.xpath(r'//ol[@class="senses"]')
        macmillan_main = etree.tostring(macmillan_main[0], pretty_print=True).replace("\n", "")

        related = tree.xpath(r'//div[@class="entrylist"]/ul/li/a/@href')
        print related

    return render_template('main.html', macmillan=macmillan_main, macmillan_related=related)


if __name__ == '__main__':
    app.run(debug=True)
