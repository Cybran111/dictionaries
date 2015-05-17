import code
from flask import Flask, render_template, request
from requests import get
from lxml import html, etree


app = Flask(__name__)

DICTIONARIES_URLS = {
    'macmillan': "http://www.macmillandictionary.com/dictionary/british/%s",
    'dictionary': "http://dictionary.reference.com/browse/%s",
    "thefree": "http://www.thefreedictionary.com/%s"
}

@app.route('/')
def hello_world():
    if 'query' in request.values:
        page = get(DICTIONARIES_URLS['macmillan'] % request.values['query'])
        tree = html.fromstring(page.text)

        macmillan_main = tree.xpath(r'//ol[@class="senses"]')

        macmillan_main = etree.tostring(macmillan_main[0], pretty_print=True).replace("\n", "")

        macmillan_related = tree.xpath(r'//div[@class="entrylist"]/ul/li/a/@href')

        dictionary_page = get(DICTIONARIES_URLS['dictionary'] % request.values["query"])
        dict_tree = html.fromstring(dictionary_page.text)

        dict_main = dict_tree.xpath(r'//div[@class="def-list"]')
        dict_main = etree.tostring(dict_main[0], pretty_print=True).replace("\n", "")

        free_page = get(DICTIONARIES_URLS['thefree'] % request.values["query"])
        free_tree = html.fromstring(free_page.text)

        free_main = free_tree.xpath(r'//div[@class="pseg"]')
        free_main = etree.tostring(free_main[0], pretty_print=True).replace("\n", "")

        return render_template('main.html',
                               macmillan=macmillan_main,
                               macmillan_related=macmillan_related,
                               dict_main=dict_main,
                               free_main=free_main


                               )
    else:
        return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
