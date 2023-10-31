# horserace_python
競馬予想を行う機械学習プログラム(pytorch)
対象レースの過去レース、参考レースの情報を収集して、１着になる確率を出力する
# execution environment
Ubuntu 22.04
NVIDIA RTX 3090  
Python 3.10.02  
Pytorch 2.0.1  

# how to use
・スクレイピングを実行する(scrape_horseinfo_integration.py)  
・1着になる確率を出力する(learning_mlp_pytorch.py)
# how to configure
・予想したいレースの馬idを入れる(src/scrape/config/racetable.py)  
・参考レースの馬idを入れる(src/scrape/config/scrape_config_racetable.py)  
# folder organization
```
.circleci  
+-- config.yml  
python_ci   
+-- csv  
   +-- learning  
      +-- each race integration data csv for machine learning(*.csv)  
   +-- scrape  
      +-- horse_id  
         +-- each horse csv(*.csv)  
      +-- race_id
         +-- each race csv(*.csv)  
+-- src  
   +-- learning  
      +-- core  
         +-- __init__.py  
         +-- learning_mlp_pytorch.py  
      +-- config
         +-- learning_config_table.py
         +-- each object race folder(ex.jbcclassic2023)  
            +-- leaning_config_evallist.py  
            +-- leaning_config_racelists.py  
   +-- scrape  
      +-- core  
         +-- scrape_horseinfo_integration.py  
         +-- scrape_horserace_util.py  
         +-- scrape_jockeytable.py  
         +-- scrape_racetrack.py  
      +-- config  
         +-- scrape_config_racetable.py
+-- tests  
   +-- __init__.py  
   +-- test_horserace.py  
+Readme.md  
requirements.txt  
run-requirements.txt  
```
# limitation
参考レースについて、一部レースでうまくスクレイピングできない馬がある。
上記についてはスクレイピング対象から除外する。
