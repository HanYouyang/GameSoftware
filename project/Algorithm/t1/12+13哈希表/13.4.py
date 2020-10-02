def interSect(nums1, nums2):
    return list(set(nums1) & set(nums2))

def interSect2(nums1, nums2):

    dict1 = dict()
    for i in nums1:
        if i not in dict1:
            dict1[i] == 1
        else:
            dict1[i] += 1
    
    ret = []
    for i in nums2:
        if i in dict1 and dict1[i] > 0:
            ret.append(i)
            dict1[i] -= 1

    return ret