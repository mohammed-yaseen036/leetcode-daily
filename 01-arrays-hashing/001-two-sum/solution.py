# 1. Two Sum
class Solution:
    def twoSum(self, nums, target):
        d={}
        for i,x in enumerate(nums):
            if (y:=target-x) in d: return [d[y],i]
            d[x]=i
