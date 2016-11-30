
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest

## Spider에서 InitSpider를 받는다.
class TestSpider(InitSpider):

    name = "test"
    allowed_domains = ["test.co.kr"]
    login_page = "http://local.test.co.kr/login"
    start_urls = "http://local.test.co.kr/"
  #Rule 객체를 이용해 크롤링 되는 사이트의 동작을 정의 한다.
    rules = (
        #Rule(SgmlLinkExtractor(allow=r'-\w+.html$'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=("local\.test\.co\.kr[^\s]*\/*$")), callback='parse_item', follow=True),
    )

  ## initRequest 메소드가 맨 처음 시작 됨.
    def init_request(self):
      ## 로그인 페이지와 callback 지정
        return Request(url=self.login_page, callback=self.login)

  ## FormRequest를 이용해서 해당 페이지에서 submit요청을 보낸다.
    def login(self, response):
        return FormRequest.from_response(response,
                    formdata={'id': '0000', 'password': '0000'},
                    callback=self.check_login_response)

  ## response된 html을 파싱해서 로그인 여부를 판단 한다.
    def check_login_response(self, response):
        //check login success
        if "/auth/logout" in response.body:
          ## 로그인이 성공하면 initialized를 실행해 파싱을 시작한다.
            return self.initialized()
        else
            return self.error()

    def initialized(self):
        return Request(url=self.start_urls, callback=self.parse_item)

    def parse_item(self, response):
        ## 중복처리를 위해 수집된 url을 불러옴.
        if self.isFirstLoop :
            self.tempUrls = self.getUrlSet()
            self.isFirstLoop = 0;
        site = "test"
        rank = "0"
        title = response.xpath('//title/text()').extract()
        req_url = response.request.url.replace('http://'+host, '', 1)
        res_url = response.url
        s  = re.search("<(!\s*doctype\s*.*?)>", response.body, re.IGNORECASE)
        doctype = s.group(1) if s else ""
        css = response.xpath('//link/@href').extract()
        js = response.xpath('//script/@src').extract()
        layout = response.xpath('//div[@class="debug_layout"]/text()').extract()
        sidebar = response.xpath('//div[@class="debug_side_layout"]/text()').extract()
        emulate = response.xpath('//meta[contains(@content, "IE")]/@content').extract()
        embed_style_cnt = len(response.xpath('//style').extract())
        embed_script_cnt = len(response.xpath('//script').extract()) - len(response.xpath('//script/@src').extract())
        # 호스트부분은 제거해 준다.
        ckurl = req_url.replace("http://local.test.co.kr", "")
        ckurl = req_url.replace("https://local.test.co.kr", "")
        if ckurl.find('?') > -1 :
            ckurl = ckurl.split('?')[0]
        elif len(ckurl.split('/')) > 4 :
            piece = ckurl.split('/')
            ckurl = piece[0]+'/'+piece[1]+'/'+piece[2]+'/'+piece[3]+'/'+piece[4]
                # 중복 확인.
        if ckurl in self.tempUrls:
            print ">>>>>>>>>>>>>>>[DropItem]:" + ckurl
            raise #DropItem("Duplicate url found: %s" % ckurl)
        else :
            req_url = ckurl
            self.tempUrls.add(req_url)
            if len(layout) > 0 :
                layout = layout[-1]
            else :
                layout = ",".join(layout)
            if len(sidebar) > 0 :
                sidebar = sidebar[-1]
            else :
                sidebar = ",".join(sidebar)
            item = SaraminWebItem()
            item["site"] = site
            item["rank"] = rank
            item["title"] = ",".join(title)
            item["req_url"] = req_url
            item["res_url"] = res_url
            item["doctype"] = doctype
            item["css"] = ",".join(css)
            item["js"] = ",".join(js)
            item["layout"] = layout
            item["sidebar"] = sidebar
            item["emulate"] = ",".join(emulate)
            item["embed_style_cnt"] = embed_style_cnt
            item["embed_script_cnt"] = embed_script_cnt
            # print(item);
            yield item
