# -*- encoding=utf-8 -*-
__author__ = 'zhanghengyang'

class Trans(object):

    def __init__(self):

        self.ac = activity_dict
        self.poi = poitype_dict


    def activity_trans(cls, name):

        if not isinstance(name, str) and not isinstance(name, unicode):

            raise Exception("name should be str or unicode")

        else:

            return cls.ac[name]


    def poitype_trans(cls, name):

        if not isinstance(name, str) and not isinstance(name, unicode):

            raise Exception("name should be str or unicode")

        else:

            return cls.poi[name]





activity_dict = {
    u"音乐" : "music",
    u"戏剧" : "opera",
    u"讲座" : "lecture",
    u"聚会" : "party",
    u"电影" : "film",
    u"展览" : "exhibition",
    u"运动" : "sport",
    u"公益" : "public",
    u"旅行" : "travel",
    u"其他" : "other",

}


poitype_dict = {

    u"休闲娱乐":"leisure",
    u"地产小区":"neighborhood",
    u"政府机构":"government",
    u"餐饮":"canteen",
    u"教育":"education",
    u"交通设施":"transportation",
    u"金融":"finance",
    u"行政地标":"landmark",
    u"旅游景点":"scene",
    u"其他":"other",
    u"房地产":"estate",
    u"other":"other",
    u"美食":"tasty",
    u"生活服务":"service",
    u"公司企业":"company",
    u"购物":"shopping",
    u"教育培训":"training",
    u"汽车服务":"car",
    u"医疗":"hospital",

}
