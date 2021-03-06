'''
Tests camera accuracy for images stored in 'training_images'.
'''
from PIL import Image
from analyze_image import analyze_image
from test_images import test_images

correct = 0
incorrect = 0

false_positive = 0

for (img_path, actual) in test_images:
  result, _, splits = analyze_image(Image.open(img_path))

  printed = False  
  for r in range(len(result)):
    if actual[r] == result[r]:
      correct += 1
    else:
      if not printed:
        print img_path, actual, result
        #print splits
        printed = True
      if result[r]:
        false_positive += 1
      incorrect += 1


print "Tested {} slices. {} slices were correct. {}%".format(correct + incorrect, correct, float(correct*100) / (correct + incorrect))
print "False positives {}. {}%".format(false_positive, float(false_positive*100) / (incorrect))
