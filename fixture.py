#!/usr/bin/env python
# encoding: utf-8
"""
fixture.py

Created by Daniel Yang on 2012-08-25.
Copyright (c) 2012 Fu Guang Industrial Co., Lmt.. All rights reserved.
"""

def process(command, db, Category, ResellerCategory, User, Page):
    if command == 'syncdb':
        sync_db(db)
    elif command == 'dropdb':
        drop_db(db)
    elif command == 'initdb':
        init_db(db, Category, ResellerCategory, User, Page)
    elif command == 'resetdb':
        reset_db(db, Category, ResellerCategory, User, Page)
    else:
        print 'unkown command. support sycndb, initdb, dropdb.'

def sync_db(db):
    db.create_all()

def drop_db(db):
    db.drop_all()

def init_db(db, Category, ResellerCategory, User, Page):
    db.session.add(User('admin','admin', 'admin', True))
    db.session.add(Category('新闻动态'))
    db.session.add(Category('公告'))
    db.session.add(Category('首页大图'))
    db.session.add(Category('对话设计师'))
    db.session.add(ResellerCategory('直营店'))
    db.session.add(ResellerCategory('批发'))
    db.session.add(ResellerCategory('FGA'))
    db.session.add(ResellerCategory('网络'))
    
    db.session.commit()
    #user_id, code, title, type, keyword, content
    db.session.add(Page(1, 'fuguang', '关于富光', 'about', '富光', """<font color="#595959"><blockquote>安徽省富光实业股份有限公司（原为安徽省富光塑胶有限公司），位于中国科教城合肥市国家AAAA级风景区—中国历史文化名镇三河，创建于1984年。最初名为肥西县三河塑料配件厂，1993年更名为合肥市三河富光塑胶有限公司，1998年正式更名为安徽省富光塑胶有限公司。2007年12月，公司更名为安徽省富光实业股份有限公司。经过二十多年的发展，已成为中国饮水口杯行业的生产制造基地。</blockquote></font>公司坚持以人为本的管理理念，注重加强内部员工培训与教育，与西安交通大学、合肥工业大学、浙江美术学院、中国科技大学等高校保持着密切的联系，以优越的办公条件和优厚的薪酬吸引高级人才的加盟，从而使富光产品的研发和技术创新能力始终走在业界的前列。<br><br>富光实业集研发、设计、制造及销售于一体，基础设施完善，技术力量雄厚。拥有国内最先进的注塑设备260多台套，工程技术人员200多名。公司在口杯用品生产领域具有较强的研制开发能力，取得各类专利技术28项（受理发明专利两项）。富光“泡茶师”和“塑玻双层杯”获2006年度安徽省省级新产品，2007年，富光技术中心被省经济委员会等7部门确定为省认定企业技术中心，科研水平在同行业中一直处于领先地位。富光实业现拥有五大事业部：塑胶事业部、真空杯事业部、玻璃杯事业部、安全帽事业部和外贸事业部。公司于2003年3月顺利通过ISO9001：2000国际质量管理体系认证，同年12月份取得进出口贸易自主经营权。根据国家质检总局市场准入制的要求，富光塑料口杯和安全帽产品均已通过“QS”质量安全认证，并取得国家质检总局颁发的“全国工业产品生产许可证”。<br><br>目前富光产品销售网络覆盖全国，口杯及安全帽已出口东南亚、美国、加拿大、欧盟等国际市场。富光饮水杯自2002年连续六年产销量稳居全国同行业第一，“富光”商标在2000年和2004年两度被认定为“安徽省著名商标”，富光饮水杯2003年和2006年也连续两度被认定为“安徽省名牌产品”。2008年3月，“富光”注册商标，被国家工商总局认定为“中国驰名商标”。同时，企业正在大力实施名牌战略，在申请认定“中国驰名商标”的同时，积极争创中国名牌。通过企业不懈努力，中国名牌战略推进委员会也正式公告，于2008年在饮水口杯行业设立“中国名牌”目录。“富光”品牌和“富光”商标已成为业界一面辉煌的旗帜，并成为中国口杯行业的排头兵和领头雁。<br><br>富光实业始终坚持以“一流的质量，优质的服务”为市场准则，坚持以“顾客满意至上”的营销理念，积极引导饮水杯消费潮流，最大限度地满足多样化、追求高质量产品的市场需求，扩大和完善营销网络，更好地树立“富光”的品牌形象，成为口杯行业的销售典范。<br><br>通过规范的内部管理，稳定的产品质量，健全的营销网络，富光实业和“富光”品牌产品获得了顾客、经销商、业界和社会各界的一致认可。富光实业先后被授予“安徽省百强民营企业”、“安徽省优秀民营企业”、“安徽省农业银行AAA级信用企业”、“安徽省出口创汇百强民营企业”、“安徽省质量管理先进企业”、“全国轻工业质量效益型先进企业”。由于“富光”饮水杯在全国口杯行业的知名度和影响力，富光实业被行业推选为中国轻工业联合会理事单位、中国日用杂品工业协会副理事长单位和中国口杯用品专业委员会主任单位，参与经国家发改委立项批准的《双层口杯》行业标准的起草和编制工作。<br><br>多年来，富光实业在不断发展壮大过程中，始终不忘作为一个发展中的企业应当履行的社会责任，努力回报社会。迄今为止，富光实业已向社会公益、社会慈善事业累计捐款捐物500多万元。憧憬未来，富光实业将继续发扬“敬业进取，团结奉献”的企业精神，坚持“一丝不苟，精益求精”的工作作风，开拓进取，努力奋斗，不断开创中国口杯行业的新纪元。<font color="#595959">精益求精”的工作作风，开拓进取，努力奋斗，不断开创中国口杯行业的新纪元。</font>"""))
    db.session.add(Page(1, 'history', '富光历史', 'about', '富光', 'history'))
    db.session.add(Page(1, 'philosophy', '富光理念', 'about', '富光','philosophy'))
    db.session.add(Page(1, 'honor', '富光荣誉', 'about', '富光', 'honor'))
    db.session.add(Page(1, 'service', '客户服务', 'service', '富光service', 'service'))
    db.session.add(Page(1, 'junzilan', '君子兰', 'about', '富光,君子兰', '君子兰实业简介'))
    
    db.session.add(Page(1, 'fg', '富光', 'brand', '富光', 'brand'))
    db.session.add(Page(1, 'fga', 'FGA', 'brand', '富光,FGA', 'brand'))
    db.session.add(Page(1, 'bestjoy', '拾喜', 'brand', '富光,拾喜', 'brand'))
    db.session.add(Page(1, 'teamaster', '茶马士', 'brand', '茶马士', 'brand'))
    db.session.commit()

def reset_db(db, Category, ResellerCategory, User, Page):
    drop_db(db)
    sync_db(db)
    init_db(db, Category, ResellerCategory, User, Page)