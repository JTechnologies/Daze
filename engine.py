def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

def toHtml(input, outputPart="full"):
  head=input.split("$content")[0]
  body=input.split("$content")[1]
  head=split(["+!","+%","##"], head.strip("\n").replace("+%","+%~mv").replace("+!", "+!~v").replace("##","##~c"))
  for i in range(len(head)):
      head[i]=head[i].strip("\n")
  head.pop(0)
  print(head)
  variables={}
  metaVariables={}
  for i in range(len(head)):
    if head[i][0]=="~" and head[i][1]=="v":
      variables[head[i].split("=")[0][2::]]=head[i].split("=")[1]
    elif head[i][0]=="~" and head[i][1]=="m" and head[i][2]=="v":
      metaVariables[head[i].split("=")[0][3::]]=head[i].split("=")[1]
    elif head[i][0]=="~" and head[i][1]=="c":
      print(f"Comment at line {i+2}: '{head[i][2::]}'")
    else:
      print("!! Daze Syntax Error: Invalid Character in $variables")
  metahtml=""
  print(metaVariables)
  for i in range(len(metaVariables)):
      if list(metaVariables)[i]=="title":
          metahtml=metahtml+f'<title>{metaVariables[list(metaVariables)[i]][1:-1]}</title>\n'
      else:
          metahtml=metahtml+f'<meta name="{list(metaVariables)[i][1:-1]}" content="{metaVariables[i][1:-1]}">\n'
  
  body=body.strip("\n").split("(")
  body.pop(0)
  bodyhtml=""
  for i in range(len(body)):
      part=body[i].split(")")
      element=part[0].strip(" ").split(": ")
      contents=element[1]
      if contents[0]=='"' and contents[-1]=='"' or contents[0]=="'" and contents[-1]=="'":
          contents=contents[1:-1]
      for i in variables.keys():
        if variables[i][0]=="'"or variables[i][0]=='"':
          contents=contents.replace(f"!{i} ",variables[i][1:-1])
        else:
          contents=contents.replace(f"!{i} ",variables[i])
      attributes_unprocessed=part[1].strip("\n").split("+")
      attributes={}
      for i in range(len(attributes_unprocessed)):
        attributes_unprocessed[i]=attributes_unprocessed[i].strip("\n")
      attributes_unprocessed.pop(0)
      for i in range(len(attributes_unprocessed)):
        attributes[attributes_unprocessed[i].split("=")[0]]=attributes_unprocessed[i].split("=")[1]
      strAttributes=""
      for i in attributes.keys():
          strAttributes=strAttributes+f' {i}="{attributes[i][1:-1]}"'
      bodyhtml=bodyhtml+f'<{element[0]}{strAttributes}>{contents}</{element[0]}>\n'
  if outputPart=="full":
      return(f"""<!DOCTYPE html>
<html>

<!-- Site compiled from Daze -->

<head>

{metahtml}
</head>
<body>
{bodyhtml}
</body>
</html>""")
  elif outputPart=="head":
      return(f"""<head>
<!-- Part compiled from Daze -->
{metahtml}
</head>
""")
  elif outputPart=="body":
      return(f"""<body>
<!-- Part compiled from Daze -->
{bodyhtml}
</body>
""")

print(toHtml("""$variables
+%title="Daze Test"
+!lang="Daze"
## This is a test of Comments
$content
(h1: "Testing! This was written in !lang !")"""))