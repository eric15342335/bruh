# place under src/ for usage
import json
import utils

print(json.dumps(utils.versions, sort_keys=True, indent=4))

filevers = ["1, 3, 4, 0"]
filedesp = ["Spam Bot Command-Line Interface"]
prodname = ["Spam Bot CLI"]
prodver = [utils.getversion(utils.CLI)]
for i in range(1):
    print(
        rf"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({filevers[i]})
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'\0'),
        StringStruct(u'FileDescription', u'{filedesp[i]}'),
        StringStruct(u'FileVersion', u'{prodver[i]}'),
        StringStruct(u'InternalName', u'\0'),
        StringStruct(u'LegalCopyright', u'eric15342335'),
        StringStruct(u'OriginalFilename', u'\0'),
        StringStruct(u'ProductName', u'{prodname[i]}'),
        StringStruct(u'ProductVersion', u'{prodver[i]}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
    """
    )
