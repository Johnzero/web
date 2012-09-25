#!/usr/bin/env python
# encoding: utf-8
"""
fixture.py

Created by Daniel Yang on 2012-08-25.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

from fuguang.users.models import User
from fuguang.pages.models import Page
from fuguang.news.models import Category, News
from fuguang.reseller.models import Reseller, ResellerCategory
from fuguang.product.models import Tag, Product

import xlrd

def init_products(db):
    book = xlrd.open_workbook('products.xls')
    sh = book.sheet_by_index(0)
    
    product_list = dict()
    for row in range(sh.nrows):
        meterial = sh.cell(row, 0).value.strip()
        p_name = sh.cell(row, 1).value.strip()
        code = sh.cell(row, 2).value.strip()
        color = sh.cell(row, 3).value.strip()
        
        if not product_list.has_key(p_name):
            product = Product(name=p_name, model=code, brand='富光', description='')
            
            mt = Tag.query.filter_by(name=meterial, type='meterial').first()
            if mt:
                product.meterials.append( mt )
            else:
                print p_name, 'no meterial.'
            
            product_list[p_name] = product
        else:
            product = product_list.get(p_name)
        
        color = Tag.query.filter_by(name=color, type='color').first()
        if color:
            product.colors.append(color)
        else:
            print p_name, 'no color'
    
    for name in product_list:
        db.session.add(product_list.get(name))
 
    db.session.commit()

"""
富光
FGA
茶马士
拾喜

玻璃
水晶玻璃
不锈钢
真空
食品级PC
食品级PP
生态骨瓷
生态紫砂
钛合金
塑胶
"""

taglist = {
'meterial':"""
玻璃
水晶玻璃
不锈钢
食品级PC
食品级PP
生态骨瓷
生态紫砂
钛合金
塑胶
安全帽
真空
""",
'scenario':"""
办公室
家用
旅游
校园
车用
""",
'applicable':"""
中小学生
大学生
白领
驴友
长辈
""",
'capacity':"""
100-200
200-400
400-600
600-1000
1000+
""",
'price':"""
10-49
50-99
100-149
150-200
200-300
300-400
400+
""",
'color':"""
兰
茶
兰
透明花瓶
黄
粉红
白
蓝绿
军绿
绿
紫
浅兰
黑紫
浅紫
蓝色
绿色
混
混装
兰色
淡黄色
黄色
粉红色
桔
粉色
紫色
玫红色
男生
女生
玫红
黄绿
蓝
黑紫色
混 
淡蓝
淡绿
灰色
白色
草绿
深灰色
透明蓝
桔色
咖啡色
黑色
灰白
橙色
青色
墨绿
墨紫
棕色
红色
橘红色
粉
深灰
海蓝
浅灰
黑
咖啡
茶色
字
圈
米灰色
灰兰色
杏灰
桔红
土黄
红
淡草绿
深蓝色
浅蓝色
浅咖啡
灰绿色
淡粉
米黄
米
闪蓝色
浅红色
闪黄色
闪灰色
钛金
本
葡萄紫
亮银咖啡
闪深灰
米金
紫砂
橘黄
本色
瓷白
中灰
果蔬绿
墨蓝
紫红
深绿
蓝灰
闪金
墨兰
炫红
陶瓷白
银铠甲
黑金刚
亮银兰
闪银
闪黑
闪紫红
亮银蓝
灰黑
珠光白
大红色
大红
浅亮兰
迷彩
米金色
透明红
海蓝
绿迷彩
淡黄
宝石纹
虎纹
珠光银
闪兰
珠光蓝
米黄色
闪蓝
闪绿
墨蓝色
闪银色
珠光紫
深海兰
果绿
黑底
白底
纳米
滤叶
亮银黑
宝兰
有滤网
富光白
橙
蓝绿色
"""
}

resellers = """
合肥长江路店
合肥国购店
合肥新亚恒丰店
合肥新都会家乐福店
马鞍山家乐福店
马鞍山大润发店
六安新都会店
六安西都店
南京大行宫家乐福店
南京大桥家乐福店
南京长虹家乐福店
淮南家乐福店
合肥大润发翡翠路店
合肥新都会店
"""


def init_db(db):
    for t in taglist:
        for tag in taglist.get(t).split('\n'):
            if tag:
                db.session.add(Tag(name=tag, type=t))
    
    db.session.add(Category(name='头条'))
    
    cate = Category(name='新闻动态')
    db.session.add(cate)
    db.session.add(Category(name='公告'))
    db.session.add(Category(name='对话设计师'))
    rc = ResellerCategory(name='直营店')
    db.session.add(rc)
    db.session.add(ResellerCategory(name='批发市场'))
    db.session.add(ResellerCategory(name='KA卖场'))
    db.session.add(ResellerCategory(name='网络平台'))
    
    for r in resellers.split('\n'):
        if r:
            db.session.add(Reseller(name=r, category=rc, certified=True, excerpt=r))
    
    user = User(username='admin',
                email='fg@fuguang.cn',
                password='admin',
                role=User.ADMIN)

    id = db.session.add(user)
    db.session.commit()
    
    #user_id, code, title, type, keyword, content
    db.session.add(Page(user_id=id, code='fuguang', title=u'关于富光', type='about', keyword=u'富光', content=u"""<font color="#595959"><blockquote>安徽省富光实业股份有限公司（原为安徽省富光塑胶有限公司），位于中国科教城合肥市国家AAAA级风景区—中国历史文化名镇三河，创建于1984年。最初名为肥西县三河塑料配件厂，1993年更名为合肥市三河富光塑胶有限公司，1998年正式更名为安徽省富光塑胶有限公司。2007年12月，公司更名为安徽省富光实业股份有限公司。经过二十多年的发展，已成为中国饮水口杯行业的生产制造基地。</blockquote></font>公司坚持以人为本的管理理念，注重加强内部员工培训与教育，与西安交通大学、合肥工业大学、浙江美术学院、中国科技大学等高校保持着密切的联系，以优越的办公条件和优厚的薪酬吸引高级人才的加盟，从而使富光产品的研发和技术创新能力始终走在业界的前列。<br><br>富光实业集研发、设计、制造及销售于一体，基础设施完善，技术力量雄厚。拥有国内最先进的注塑设备260多台套，工程技术人员200多名。公司在口杯用品生产领域具有较强的研制开发能力，取得各类专利技术28项（受理发明专利两项）。富光“泡茶师”和“塑玻双层杯”获2006年度安徽省省级新产品，2007年，富光技术中心被省经济委员会等7部门确定为省认定企业技术中心，科研水平在同行业中一直处于领先地位。富光实业现拥有五大事业部：塑胶事业部、真空杯事业部、玻璃杯事业部、安全帽事业部和外贸事业部。公司于2003年3月顺利通过ISO9001：2000国际质量管理体系认证，同年12月份取得进出口贸易自主经营权。根据国家质检总局市场准入制的要求，富光塑料口杯和安全帽产品均已通过“QS”质量安全认证，并取得国家质检总局颁发的“全国工业产品生产许可证”。<br><br>目前富光产品销售网络覆盖全国，口杯及安全帽已出口东南亚、美国、加拿大、欧盟等国际市场。富光饮水杯自2002年连续六年产销量稳居全国同行业第一，“富光”商标在2000年和2004年两度被认定为“安徽省著名商标”，富光饮水杯2003年和2006年也连续两度被认定为“安徽省名牌产品”。2008年3月，“富光”注册商标，被国家工商总局认定为“中国驰名商标”。同时，企业正在大力实施名牌战略，在申请认定“中国驰名商标”的同时，积极争创中国名牌。通过企业不懈努力，中国名牌战略推进委员会也正式公告，于2008年在饮水口杯行业设立“中国名牌”目录。“富光”品牌和“富光”商标已成为业界一面辉煌的旗帜，并成为中国口杯行业的排头兵和领头雁。<br><br>富光实业始终坚持以“一流的质量，优质的服务”为市场准则，坚持以“顾客满意至上”的营销理念，积极引导饮水杯消费潮流，最大限度地满足多样化、追求高质量产品的市场需求，扩大和完善营销网络，更好地树立“富光”的品牌形象，成为口杯行业的销售典范。<br><br>通过规范的内部管理，稳定的产品质量，健全的营销网络，富光实业和“富光”品牌产品获得了顾客、经销商、业界和社会各界的一致认可。富光实业先后被授予“安徽省百强民营企业”、“安徽省优秀民营企业”、“安徽省农业银行AAA级信用企业”、“安徽省出口创汇百强民营企业”、“安徽省质量管理先进企业”、“全国轻工业质量效益型先进企业”。由于“富光”饮水杯在全国口杯行业的知名度和影响力，富光实业被行业推选为中国轻工业联合会理事单位、中国日用杂品工业协会副理事长单位和中国口杯用品专业委员会主任单位，参与经国家发改委立项批准的《双层口杯》行业标准的起草和编制工作。<br><br>多年来，富光实业在不断发展壮大过程中，始终不忘作为一个发展中的企业应当履行的社会责任，努力回报社会。迄今为止，富光实业已向社会公益、社会慈善事业累计捐款捐物500多万元。憧憬未来，富光实业将继续发扬“敬业进取，团结奉献”的企业精神，坚持“一丝不苟，精益求精”的工作作风，开拓进取，努力奋斗，不断开创中国口杯行业的新纪元。<font color="#595959">精益求精”的工作作风，开拓进取，努力奋斗，不断开创中国口杯行业的新纪元。</font>"""))
    db.session.add(Page(user_id=id, code='history', title=u'富光历史', type='about', keyword=u'富光', content='history'))
    db.session.add(Page(user_id=id, code='philosophy', title=u'富光理念', type='about', keyword=u'富光',content='philosophy'))
    db.session.add(Page(user_id=id, code='honor', title=u'富光荣誉', type='about', keyword=u'富光', content='honor'))
    db.session.add(Page(user_id=id, code='service', title=u'客户服务', type='service', keyword=u'富光service', content='service'))
    db.session.add(Page(user_id=id, code='junzilan', title=u'君子兰', type='about', keyword=u'富光,君子兰', content=u'君子兰实业简介'))
    
    db.session.add(Page(user_id=id, code='fuguang', title=u'富光', type='brand', keyword=u'富光', content='brand'))
    db.session.add(Page(user_id=id, code='fga', title='FGA', type='brand', keyword=u'富光,FGA', content='brand'))
    db.session.add(Page(user_id=id, code='bestjoy', title=u'拾喜', type='brand', keyword=u'富光,拾喜', content='brand'))
    db.session.add(Page(user_id=id, code='teamaster', title=u'茶马士', type='brand', keyword='茶马士', content='brand'))
    
    db.session.add(News(user=user, title="“FGA-富光”招商盛会隆重召开", excerpt="""7月21至22日，以“大战略、大格局、大未来”为主题的“FGA-富光”招商盛会在合肥鸿瑞金陵大酒店隆重召开。""",
                        category= cate, content="""
                        7月21至22日，以“大战略、大格局、大未来”为主题的“FGA-富光”招商盛会在合肥鸿瑞金陵大酒店隆重召开。会上，富光实业君子兰公司总经理吴良伟同志及其营销管理团队，详细介绍了“FGA-富光”品牌的地位、发展方向及战略规划，并与参会的全国客商进行了深入探讨，达成广泛共识，形成了一揽子战略框架合作协议，此次招商盛会的召开，不仅开创了富光实业发展的新空间，更为消费者提供了更丰富的产品选择，也极大的满足了消费者的个性化需求，对完善和细化“FGA-富光”品牌建设，将产生深远和重要的指导意义。富光实业吴秀杰董事长及有关方面负责同志，应邀出席会议。
                        """))
    
    db.session.commit()
