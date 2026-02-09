from read_ad import read_pdf
from llm import output
from config import AD_DIR
import asyncio
import json
from config import JSON
import os

async def main():
    filenames=os.listdir(AD_DIR)
    outputs = {}
    po=[]
    for files in filenames:
        ad_objects={}
        

        if not files.endswith(".pdf"):
            continue
        
        data=read_pdf(AD_DIR,files)
        tasks = [output(tag, content) for tag, content in data.items()]
        results = await asyncio.gather(*tasks)
        for res in results:
            if "ad_number" in res:
                ad_objects["AD_number"]=res["ad_number"]["ad_id"]
                ad_objects["Date_AD"]=res["ad_number"]["effective_date"] 
            elif "applicability" in res:
                ad_objects["Applicability"]=res["applicability"]
            else:
                ad_objects["Reason"]=res["reason"]["reason"]  
        
        po.append(ad_objects)
            
    outputs["ruled_based"]=po
    
    return outputs 

if __name__ == "__main__":
    qw=asyncio.run(main())
    with open(JSON, "w", encoding="utf-8") as f:
        json.dump(qw, f, indent=2, ensure_ascii=False)