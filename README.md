# horserace_python
競馬予想を行う機械学習プログラム(pytorch)
対象レースの過去レース、参考レースの情報を収集して、１着になる確率を出力する
# Requirements
Python3  
NVIDIA Graphics Board  
# how to use
・予想したいレースの馬idを入れる(src/scrape/config/racetable.py)  
・参考レースの馬idを入れる(src/scrape/config/scrape_config_racetable.py)  
# フォルダ構成
```
python_ci  
+-- .circleci  
   +-- config.yml  
+-- csv  
   +-- learning  
   +-- scrape  
      +-- horse_id  
      +-- race_id  
+-- src  
   +-- learning  
      +-- core  
      +-- config  
   +-- scrape  
      +-- core  
         +-- scrape_horseinfo_concat.py  
         +-- scrape_horserace_util.py  
         +-- scrape_jockeytable.py  
         +-- scrape_racetrack  
      +-- config  
+-- tests  
   +-- 
```
