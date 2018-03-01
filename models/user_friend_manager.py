# -*- coding:utf-8 -*-

# importing defs
from models.models import UserRelation

from models.base_manager import SNBaseManager


# creating a manager for functions
class UserRelationManager(SNBaseManager):
    def __init__(self):
        class_model = UserRelation
        super(UserRelationManager, self).__init__(class_model)

# function for adding friends to friend list
    def addFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return
        if self.getFriend(user1, user2):
            return
        self.object.user1 = user1
        self.object.user2 = user2

        return self.save()

# function for deleting a user from friend list
    def delFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return

        return self.delete().And([('user1', '=', user1), ('user2', '=', user2)]) \
            .Or([('user1', '=', user2), ('user2', '=', user1)]).run()

# ???
    def getFriends(self, user):
        if not isinstance(user, int):
            return

        return self.select().And([('user1', '=', user)]).Or([('user2', '=', user)]).run()

# if a user is already a friend, you can no longer add him
    def getFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return

        return self.select().And([('user1', '=', user1), ('user2', '=', user2)]) \
            .Or([('user1', '=', user2), ('user2', '=', user1)]).run()

# a check if user is in the friend list
    def isFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return

        data = self.select().And([('user1', '=', user1), ('user2', '=', user2)]) \
            .Or([('user1', '=', user2), ('user2', '=', user1)]).run()

        if data:
            return True
        return False

# function for blocking users
    def blockFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return

        relation = self.getFriend(user1, user2)
        relation.object.block = 1
        relation.save()
