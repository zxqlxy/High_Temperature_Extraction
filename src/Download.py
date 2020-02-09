import requests


# data = response.text
years = ["2019"]
months = [str(i+ 1) for i in range(12)]
months = list(map(lambda i: '0'+ i if len(i) == 1 else i, months))
days = [str(i + 1) for i in range(31)]
days = list(map(lambda i: '0'+ i if len(i) == 1 else i, days))
urlBase = "http://jsoc.stanford.edu/data/aia/synoptic"
locPath = "/Users/lxy/Desktop/Rice/PHYS 491 & 493 Research/High Temperature Extraction/data/SDOAIA"

for yr in years:
    for mo in months:
        print(mo)
        for da in days:
            thisFile = "AIA"+ yr + mo + da + "_0000_0094.fits"
            thisPath = "/".join([yr,mo,da,"H0000"])
            print(thisFile)

            myUrl = "/".join([urlBase,thisPath,thisFile ])
            myDest = "/".join([locPath, thisFile])
            # print(myDest)
            print(myUrl)
            myBits = requests.get(myUrl)

            if len(myBits.content) > 500: # if files don't exist we get a short reply from the server: skip these
                myFile = open(myDest, "wb")
                myFile.write(myBits.content)
                myFile.close()
