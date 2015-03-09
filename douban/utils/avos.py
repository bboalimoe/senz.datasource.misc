#!/usr/bin/env python
# encoding: utf-8

import requests
import json


class AVObject(object):
    base = r'https://leancloud.cn' #cn.avoscloud.com
    base_classes = base+r'/1.1/classes/'
    base_patch = base+r'/1.1/batch'
    Users = base+r'/1.1/users'
    app_settings = ['', '']

    def __init__(self):
        pass

    #private methods

    @classmethod
    def headers(cls):
        # Since properties only work on instances, need define headers property in meta class
        return {
            "X-AVOSCloud-Application-Id": cls.app_settings[0],
            "X-AVOSCloud-Application-Key": cls.app_settings[1],
            "Content-Type": "application/json"
        }

    @classmethod
    def _save_to_avos(cls, cls_name, data):
        if type(data) == list:
            #save many object
            patch_ob_list = [{"method": "POST",
                              "path": "/1.1/classes/"+cls_name,
                              "body": ob} for ob in data]
            return AVObject._patch_avos(
                patch_ob_list
            )
        else:
            #save single object
            return requests.post(
                AVObject.base_classes+cls_name,
                data=json.dumps(data),
                headers=cls.headers(),
                verify=False
            )

    @classmethod
    def _get_avos(cls, cls_name, ob_id=None, **kwargs):
        get_url = AVObject.base_classes+cls_name
        get_url = get_url + '/' + ob_id if ob_id else get_url

        #kpara = include, where, limit, order
        with_params = {}
        for kparam, vparam in kwargs.items():
            with_params[kparam] = json.dumps(vparam)

        return requests.get(
            get_url,
            headers=cls.headers(),
            params=with_params,
            verify=False
        )

    @classmethod
    def _update_avos(cls, cls_name, data, plus_ob={}):
        if type(data) == list:
            #update many object
            patch_ob_list = [{"method": "PUT",
                              "path": "/1.1/classes/"+cls_name+"/"+ob['objectId'],
                              "body": ob} for ob in data]
            return AVObject._patch_avos(
                patch_ob_list
            )

        elif type(data) == dict or type(data) == str:
            ob_id = data['objectId'] if type(data) == dict else data

            #check plus_ob
            if type(plus_ob) != dict:
                return None

            put_url = AVObject.base_classes + cls_name + '/' + ob_id
            return requests.put(
                put_url,
                data=json.dumps(plus_ob),
                headers=cls.headers(),
                verify=False
            )
        else:
            return None

    @classmethod
    def _remove_avos(cls, cls_name, data):

        if type(data) == list:#batch remove
            #remove many objects
            patch_ob_list = [{"method": "DELETE",
                              "path": "/1.1/classes/"+cls_name+"/"+ob['objectId']}
                             for ob in data]
            return AVObject._patch_avos(
                patch_ob_list
            )
        elif type(data) == dict or type(data) == str: #remove single one
            #remove single object
            ob_id = data['objectId'] if type(data) == dict else data
            remove_url = AVObject.base_classes + cls_name + '/' + ob_id
            return requests.delete(
                remove_url,
                headers=cls.headers(),
                verify=False
            )
        else:
            return None

    @classmethod
    def _patch_avos(cls, patch_ob_list):
        return requests.post(
            AVObject.base_patch,
            data=json.dumps({'requests': patch_ob_list}),
            headers=cls.headers(),
            verify=False
        )

    #utility function
    @staticmethod
    def pointer(ob, cls_name):
        if type(ob) == dict and ob.get('objectId', None) \
                and type(cls_name) == str:
            pt_ob = {
                "__type": "Pointer",
                "className": cls_name,
                "objectId": ob['objectId']
            }
            return pt_ob
        else:
            return None

    @staticmethod
    def in_query(where_ob, cls_name):
        if type(where_ob) == dict and type(cls_name) == str:
            in_query_ob = {"$inQuery": {"where": where_ob, "className": cls_name}}
            return in_query_ob
        else:
            return None

    @staticmethod
    def re_pointer(ob, cls_name, key_pt):
        if type(ob) == dict and type(cls_name) == str:
            return {
                "$relatedTo": {
                    "object": {
                        "__type": "Pointer",
                        "className": cls_name,
                        "objectId": ob['objectId']
                    },
                    "key": key_pt
                }
            }

    @staticmethod
    def or_query(where_ob_list):
        #`where={"$or":[{"wins":{"$gt":150}},{"wins":{"$lt":5}}]}`
        return {"$or": where_ob_list}

    #class methods
    @classmethod
    def save(cls, ob):
        """
        Save single object `ob` to `/classes/cls`
        :param ob:
        :return:
            `response` like { "createdAt": "...", "objectId": "..."}
        """
        return cls._save_to_avos(cls.__name__, ob)

    @classmethod
    def get(cls, ob_id=None, **kwargs):
        """
        :param ob_id:
            if None, get list of objects
            if ob_id is an object, automatically extract proper ob_id #todo
        :param kwargs:
            `include=post, post.author` result including a complete relation object
            `where=` filters
            `order=score,-name` descended order
            `limit=` limit default to 100, max to 1000
            `skip=N` skip first N result
            `count=1`  return `{"results": [], "count": 1337 }`
            `keys=score,playerName` only return fields
            `where={"arrayKey":2}` array contains value 2
            `where={"arrayKey":{"$all":[2,3,4]}}` matches all
            `where={"field_common": AVObject.pointer(ob, cls_name) }` pointer: point to
            `where={"field_common": AVObject.in_query(where_ob, cls_name) }` inQuery
            `where= AVObject.re_pointer(ob, cls_name, field_likes_arr)` reverse pointer: point from
            'where= AVObject.or_query(where_ob_list)
        :return:
            `RESPONSE.content.results` : list of results
        """
        return cls._get_avos(cls.__name__, ob_id, **kwargs)

    @classmethod
    def update(cls, ob, plus_ob):
        """
        Update single object
        :param ob: Object or list of objects containing `objectId` attribute
        :param plus_ob: -d json.dumps(plus_ob)
                        -d '{"score":73453}' \
                        -d '{"opponents":{"__op":"Delete"}}' \
                        -d '{"score":{"__op":"Increment","amount":1}}' \
                        -d '{"skills":{"__op":"AddUnique/ Add/ Remove","objects":["flying","kungfu"]}}' \
                        -d '{"opponents":{
                                "__op":"AddRelation/ RemoveRelation",
                                "objects":[{"__type":"Pointer","className":"Player","objectId":"51b0f0e851c16221"}]}
                            }' \
        :return: {"updatedAt":"...","objectId":"..."}
        """
        return cls._update_avos(cls.__name__, ob, plus_ob)

    @classmethod
    def remove(cls, ob):
        """
        Remove object from '/classes/cls'
        :param ob: Object or ob_id
        :return:
        """
        return cls._remove_avos(cls.__name__, ob)

    @classmethod
    def patch(cls, patch_ob_list):
        """
        Raw patch function. See also `save_all`, `update_all`, and `remove_all`
        :param patch_ob_list: Posted as `{"requests":patch_ob_list}`
        :return: List of separate response object containing `success` or `error` attr
        """
        return cls._patch_avos(patch_ob_list)

    @classmethod
    def save_all(cls, ob_list):
        return cls._save_to_avos(cls.__name__, ob_list)

    @classmethod
    def update_all(cls, ob_list):
        return cls._update_avos(cls.__name__, ob_list)

    @classmethod
    def remove_all(cls, ob_list):
        """
        :param ob_list:
        :return: return list of response object containing status `[{"success":{}}]`
        """
        return cls._remove_avos(cls.__name__, ob_list)


if __name__ == "__main__":

        pass
        #test

