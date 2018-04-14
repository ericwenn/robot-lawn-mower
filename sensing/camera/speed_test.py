from PIL import Image
from analyze_image import analyze_image
from test_images import test_images


# correct = 0
# incorrect = 0

# false_positive = 0

# for (img_path, actual) in test_images:
#   result, _ = analyze_image(Image.open(img_path), stitch = False)

#   printed = False  
#   for r in range(len(result)):
#     if actual[r] == result[r]:
#       correct += 1
#     else:
#       if not printed:
#         #print img_path, actual, result
#         printed = True
#       if result[r]:
#         false_positive += 1
#       incorrect += 1


# print "Tested {} slices. {} slices were correct. {}%".format(correct + incorrect, correct, float(correct*100) / (correct + incorrect))
# print "False positives {}. {}%".format(false_positive, float(false_positive*100) / (incorrect))

def test():
    imgs = []
    for (img_path, actual) in test_images[:10]:
      imgs.append(Image.open(img_path))

    print len(imgs)
    for img in imgs:
      result, _ = analyze_image(img, stitch = False)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("test()", setup="from __main__ import test", number=10))