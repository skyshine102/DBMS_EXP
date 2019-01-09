# DBMS_EXP
This repository stores the code and data for the NTUEE DBMS Final Project, including scripts for graph DB systems study and Neo4j exemplar query.  
1.Files should be contain in EXP:  
  EXP/  
    >>jieba_dict/  
      >>>>dict.txt.big  
      >>>>stopwords.txt  
    >>emampler_query.py  
    >>word2vec.model  
    >>word2vec.model.trainables.syn1neg.npy  
    >>word2vec.model.wv.vectors.npy  

  Below are links for word2vec.model, word2vec.model.trainables.syn1neg.npy, word2vec.model.wv.vectors.npy  
  https://drive.google.com/file/d/1j8YQWZjYtc3yBTloVWkQo_t5fIAztPm4/view?usp=sharing  
  https://drive.google.com/file/d/1441KBAM3ZAKWxjggBoDHWiy4apzPXImU/view?usp=sharing  
  https://drive.google.com/file/d/1Tw0gyUYVm0bjazmucUvQ2Jou_TKjbbHU/view?usp=sharing  

2. example data loading(on Windows):   
  py py2neo.py  

3. execute program(On windows):  
  py exampler_query.py  

4. query example: If you want to type a word with whitespace, type "_" instead of whitespace.    
  * Query single nodes:  
    eg. 電腦網路導論  

  * Query multiple nodes with result sorted by distance:  
    eg. 電腦網路導論 購物  

  * Query multiple nodes with result sorted by distance:  
    eg. 電腦網路導論 購物 -s  

  * type quit to quit  programm  
