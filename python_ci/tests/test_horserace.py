#自作ライブラリ
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
print(str(Path(__file__).resolve().parent.parent))

from src.learning.config.jbcclassic2023.learning_racelists import race_for_learing_lists_jbcclassic2023
from src.learning.config.jbcsprint2023.learning_racelists import race_for_learing_lists_jbcsprint2023

from src.learning.config.learning_table import Learning_Race,learning_race_eval_list
from src.scrape.config.scrape_table import Scrape_Race,scrape_race_eval_list


#learning側とscrape側でレースと紐付けたenumの値が正しいことの確認
def test_verify_race_enum():
    test_result = True

    assert(Learning_Race.JBCCLASSIC2023.value == Scrape_Race.JBCCLASSIC2023.value)
    assert(Learning_Race.JBCSPRINT2023.value == Scrape_Race.JBCSPRINT2023.value)
    assert(Learning_Race.JBCLADIESCLASSIC2023.value == Scrape_Race.JBCLADIESCLASSIC2023.value)

