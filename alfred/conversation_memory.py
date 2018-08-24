#!/usr/bin/env python3

from alfred.memory import Memory
from bson.objectid import ObjectId
from collections import defaultdict


class ConversationMemory(Memory):
    """
    This class manages the conversation states and communicate with the mongo databases.
    """

    def __init__(self):
        self.mongo_client = super(ConversationMemory, self).get_mongo_client()
        self.conversation_db = self.mongo_client.alfred.conversations

    def decode_user_data_dict(self, user_data_dict):
        """
        Decode a telegram-user_data dict to a processable entity for json dump().
        :param user_data_dict:
        :return:
        """
        if not isinstance(user_data_dict, dict):
            raise ValueError("Expected dict object. Given " + str(type(user_data_dict)))

        ret = {str(k): v for k, v in user_data_dict.items() if isinstance(k, int)}

        return ret

    def encode_user_data_dict(self, user_data_dict_decoded):
        """
        Encode a decoded telegram-user_data dict to obtain the original file.
        :param user_data_dict:
        :return:
        """
        if not isinstance(user_data_dict_decoded, dict):
            raise ValueError("Expected defaultdict object. Given " + str(type(user_data_dict_decoded)))

        ret = {int(k): v for k, v in user_data_dict_decoded.items() if not "id" in k}

        return ret

    def decode_conversation_dict(self, conversation_dict):
        """
        Decode a telegram-conversation dict to a processable entity for json dump().
        :param conversation_dict:
        :return:
        """
        if not isinstance(conversation_dict, dict):
            raise ValueError("Expected dict object. Given " + str(type(conversation_dict)))

        ret = {str(k[0]): {"key": k, "value": v} for k, v in conversation_dict.items() if k != "id"}

        return ret

    def encode_conversation_dict(self, conversation_dict_decoded):
        """
        Encode a decoded telegram-conversation dict to obtain the original file.
        :param conversation_dict:
        :return:
        """
        if not isinstance(conversation_dict_decoded, dict):
            raise ValueError("Expected dict object. Given " + str(type(conversation_dict_decoded)))

        ret = {}

        for k, v in conversation_dict_decoded.items():
            if isinstance(k, str) and k.isnumeric():
                if isinstance(v, dict) and "key" in v and "value" in v:
                    ret[tuple(v["key"])] = v["value"]
        return ret

    def get_user_datas(self):
        """
        Returns the dict that is compatible for telegram.
        :return:
        """
        user_data_dict_decoded = self.conversation_db.find_one({"id": "user_data"})
        return defaultdict(dict, self.encode_user_data_dict(user_data_dict_decoded=user_data_dict_decoded))

    def get_conversations(self):
        """
        Returns the dict that is compatible for telegram.
        :return:
        """
        conversation_dict_decoded = self.conversation_db.find_one({"id": "conversation"})
        encoded = self.encode_conversation_dict(conversation_dict_decoded=conversation_dict_decoded)
        return encoded

    def upsert_user_data(self, user_data):
        """
        Stores the user_data from the dispatcher to mongo-db.
        :param user_data:
        :return:
        """
        if not isinstance(user_data, defaultdict):
            raise ValueError("Expected dict object. Given " + str(type(user_data)))

        # Decode
        user_data_decoded = self.decode_user_data_dict(user_data_dict=user_data)

        # Store
        key = {"id": "user_data"}
        data = {**user_data_decoded, **key}
        self.conversation_db.update(key, data, upsert=True)

    def upsert_conversation(self, conversation_dict):
        """
        Stores the decoded conversation-dict obtained by the conversation_handler to mongo-db.
        :param conversation_dict:
        :return:
        """
        if not isinstance(conversation_dict, dict):
            raise ValueError("Expected dict object. Given " + str(type(conversation_dict)))

        # Decode
        conversation_dict_decoded = self.decode_conversation_dict(conversation_dict=conversation_dict)

        # Store
        key = {"id": "conversation"}
        data = {**conversation_dict_decoded, **key}
        self.conversation_db.update(key, data, upsert=True)


if __name__ == "__main__":
    mem = ConversationMemory()
    dicti = {'_id': ObjectId('5b7ee2cbe86f8e6b4ed3ef05'), '120745084': {'key': [120745084, 120745084], 'value': 4},
             'id': 'conversation'}
    print(mem.encode_conversation_dict(dicti))
