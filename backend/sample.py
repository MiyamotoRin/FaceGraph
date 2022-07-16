import sys
import json

data = sys.argv

image = data[1]

image = image.replace('data:image/png;base64,','')

result = {'resultImages':[]}
for i in range(3):
    result['resultImages'].append(image)

print(json.dumps(result))
